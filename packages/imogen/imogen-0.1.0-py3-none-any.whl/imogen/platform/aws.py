# Copyright 2024 - 2025 Avram Lubkin, All Rights Reserved

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
Imogen AWS interface
"""

import concurrent
import logging
import os
import time
from base64 import b64encode
from hashlib import sha256
from pathlib import Path
from math import ceil
from types import TracebackType
from typing import Optional, Container, Self, Type

import boto3
import botocore.config

from imogen.config import Config
from imogen.exceptions import ImogenAWSError, ImogenConfigError

LOGGER = logging.getLogger(__name__)

BLOCKSIZE = 512 * 1024  # Snapshots use 512-KiB sectors
WORKERS = max(64, min(16, os.cpu_count() or 1 * 2))  # 64 or more workers


class VPC:
    """
    VPC operations interface
    """

    def __init__(self, config: Config, session: boto3.Session) -> None:

        # Validate we have an AWS configuration and use an attribute so the type checker knows
        if config.aws is None:
            raise ImogenConfigError('No AWS configuration defined')

        self.config = config
        self.aws_config = config.aws
        self.ec2 = session.client('ec2')
        self.vpc_id = None
        self.internet_gateway_id = None
        self.subnet_id = None
        self.security_group_id = None

    def __enter__(self) -> Self:

        try:
            self.create()
            return self
        except:  # noqa
            self.destroy()
            raise

    def __exit__(self, exc_type: Optional[Type[BaseException]], exc_value: Optional[BaseException],
                 traceback: Optional[TracebackType]) -> None:
        self.destroy()

    def create(self) -> None:
        """
        Create a VPC with subnet, internet gateway, routing table, and security group
        """

        LOGGER.info('Creating VPC %s', self.aws_config.vpc_name)
        timer = self.config.timer.start('Configure VPC', 'AWS')

        # Create VPC
        self.vpc_id = vpc_id = self.ec2.create_vpc(
            CidrBlock=self.aws_config.vpc_subnet,
            TagSpecifications=[{
                'ResourceType': 'vpc',
                'Tags': [{'Key': 'Name', 'Value': self.aws_config.vpc_name}],
            }],
        )['Vpc']['VpcId']

        # Wait for VPC to be available
        self.ec2.get_waiter('vpc_available').wait(
            VpcIds=[vpc_id], WaiterConfig={'Delay': 1, 'MaxAttempts': 600}
        )

        # Create subnet
        self.subnet_id = self.ec2.create_subnet(
            VpcId=vpc_id,
            CidrBlock=self.aws_config.vpc_subnet,
            TagSpecifications=[{
                'ResourceType': 'subnet',
                'Tags': [{'Key': 'Name', 'Value': self.aws_config.vpc_name}],
            }],
        )['Subnet']['SubnetId']

        # Create Internet gateway
        self.internet_gateway_id = self.ec2.create_internet_gateway(
            TagSpecifications=[{
                'ResourceType': 'internet-gateway',
                'Tags': [{'Key': 'Name', 'Value': self.aws_config.vpc_name}],
            }],
        )['InternetGateway']['InternetGatewayId']

        # Attach Internet gateway to VPC
        self.ec2.attach_internet_gateway(
            InternetGatewayId=self.internet_gateway_id, VpcId=vpc_id
        )

        # Create security group
        self.security_group_id = self.ec2.create_security_group(
            Description=f'Security Group for {self.aws_config.vpc_name}',
            GroupName=self.aws_config.vpc_name,
            VpcId=vpc_id,
        )['GroupId']

        # Get default routing table
        route_table_id = self.ec2.describe_route_tables(
            Filters=[
                {'Name': 'vpc-id', 'Values': [vpc_id]},
                {'Name': 'association.main', 'Values': ['true']}]
        )['RouteTables'][0]['RouteTableId']

        # Add default route to Internet gateway
        self.ec2.create_route(
            RouteTableId=route_table_id,
            DestinationCidrBlock='0.0.0.0/0',
            GatewayId=self.internet_gateway_id
        )

        timer.stop()
        LOGGER.info('VPC %s (%s) created and configured', self.aws_config.vpc_name, vpc_id)

    def destroy(self) -> None:
        """
        Destroy the components of the VPC in order
        """

        if self.security_group_id:
            self.ec2.delete_security_group(GroupId=self.security_group_id)

        if self.subnet_id:
            self.ec2.delete_subnet(SubnetId=self.subnet_id)

        if self.internet_gateway_id:
            self.ec2.detach_internet_gateway(
                InternetGatewayId=self.internet_gateway_id, VpcId=self.vpc_id
            )
            self.ec2.delete_internet_gateway(InternetGatewayId=self.internet_gateway_id)

        if self.vpc_id:
            self.ec2.delete_vpc(VpcId=self.vpc_id)

        LOGGER.info('VPC %s (%s) destroyed', self.aws_config.vpc_name, self.vpc_id)


class AWS:
    """
    AWS operations interface
    """

    def __init__(self, config: Config) -> None:

        # Validate we have an AWS configuration and use an attribute so the type checker knows
        if config.aws is None:
            raise ImogenConfigError('No AWS configuration defined')
        self.aws_config = config.aws

        self.config = config
        self.session = boto3.Session(region_name=config.aws.region, profile_name=config.aws.profile)
        self.ec2 = self.session.client('ec2')

    def instance_stopped_manually(self, instance_id: str) -> Optional[dict]:
        """
        Check CloudTrail logs to try to determine if an instance was stopped manually

        This is very basic, only looking for the last StopInstances event and returning it
        """

        cloudtrail = self.session.client('cloudtrail')
        for event in cloudtrail.lookup_events(
            LookupAttributes=[{'AttributeKey': 'ResourceName', 'AttributeValue': instance_id},],
            MaxResults=10,
        )['Events']:
            if event['EventName'] == 'StopInstances':
                return event

        return None

    def build(self, image: Path) -> Optional[str]:
        """
        Main entry point for AWS operations

        A VPC is created and an the image is launched as an instance in it
        The instance is expected to power off when complete and that state is waited for
        The instance is expected to install a system to the second disk
        The second disk is converted to an AMI

        The ID of the new AMI is returned or None if an AMI isn't created
        """

        ami_id = None

        # Upload the build image as an AMI
        with self.config.timer.start('Import build image', 'AWS'):
            build_ami_id, build_snapshot_id = self.import_image(image)

        # Create a temporary VPC to perform the build
        with VPC(self.config, self.session) as vpc:

            # Launch the build instance with the build AMI
            with self.config.timer.start('Launch build instance', 'AWS'):
                instance_id = self.run_build_instance(build_ami_id, build_snapshot_id, vpc)

            timer = self.config.timer.start('Perform build', 'AWS')
            try:
                # Get volume_id for second disk. Not available until running
                volume_id = self.get_volume_id(instance_id, '/dev/sdb')

                # The kickstart build should shutdown the image when it's complete
                # Wait for the image to stop. Check every 5 seconds for 20 minutes
                LOGGER.info('Waiting for build on instance %s to complete', instance_id)
                self.ec2.get_waiter('instance_stopped').wait(
                        InstanceIds=[instance_id], WaiterConfig={'Delay': 5, 'MaxAttempts': 240}
                    )
                timer.stop()

                if last_stop_event := self.instance_stopped_manually(instance_id):
                    LOGGER.error(
                        'Instance %s was shutdown manually by %s, skipping AMI creation',
                        instance_id, last_stop_event['Username']
                    )
                elif volume_id:
                    # Convert the second disk to an AMI
                    with self.config.timer.start('Convert volume to AMI', 'AWS'):
                        ami_id = self.volume_to_ami(volume_id)

            finally:
                with self.config.timer.start('Build cleanup', 'AWS'):
                    self.terminate_instance(instance_id)
                    LOGGER.info('Removing build AMI %s', build_ami_id)
                    self.ec2.deregister_image(ImageId=build_ami_id)
                    self.ec2.delete_snapshot(SnapshotId=build_snapshot_id)

        if ami_id:
            with self.config.timer.start('Remove old AMIs', 'AWS'):
                self.remove_old_amis(ignore={ami_id})

        return ami_id

    def remove_old_amis(self, ignore: Optional[Container[str]] = None) -> None:
        """
        Removes old AMIS

        The number to keep is specified as config.aws.ami_max
        ignore is a set of AMI IDs that are never removed
        The short_name tag must match name value at root of configuration
        The architecture must match aws_config.arch
        """

        # Query for AMIs matching short name and arch
        images = self.ec2.describe_images(
            Owners=['self'],
            Filters=[
                {'Name': 'architecture', 'Values': [self.aws_config.arch]},
                {'Name': 'tag:short_name', 'Values': [self.config.name]},
            ],
        )['Images']

        if len(images) <= self.aws_config.ami_max:
            return

        LOGGER.info('Found %d AMIs with the short name %s, keeping %s',
                    len(images), self.config.name, self.aws_config.ami_max)

        # Iterate through all the returned images except the newest {ami_max} AMIs
        for image in sorted(images, key=lambda x: x['CreationDate'])[:-self.aws_config.ami_max]:

            if ignore and image['ImageId'] in ignore:
                continue

            LOGGER.info('Removing old AMI %s (%s)', image['Name'], image['ImageId'])
            self.ec2.deregister_image(ImageId=image['ImageId'])
            self.ec2.delete_snapshot(
                SnapshotId=image['BlockDeviceMappings'][0]['Ebs']['SnapshotId']
            )

    def run_build_instance(self, ami_id: str, snapshot_id: str, vpc: VPC) -> str:
        """
        Launches an instance with the AMI and waits for the running state

        Returns the instance ID
        """

        LOGGER.info('Launching build instance with AMI %s', ami_id)
        instance_id = self.ec2.run_instances(
            BlockDeviceMappings=[
                {
                    'Ebs': {
                        'DeleteOnTermination': True,
                        'SnapshotId': snapshot_id,
                        'VolumeType': 'gp3',
                    },
                    'DeviceName': '/dev/sda1',
                },
                {
                    'Ebs': {
                        'DeleteOnTermination': True,
                        'VolumeSize': self.aws_config.ami_volume_size,
                        'VolumeType': 'gp3',
                    },
                    'DeviceName': '/dev/sdb',
                },
            ],
            ImageId=ami_id,
            InstanceType=self.aws_config.instance_type,
            MaxCount=1,
            MinCount=1,
            Monitoring={'Enabled': False},
            TagSpecifications=[{
                'ResourceType': 'instance',
                'Tags': [{'Key': 'Name', 'Value': self.aws_config.vpc_name}],
            }],
            NetworkInterfaces=[{
                'AssociatePublicIpAddress': True,
                'DeleteOnTermination': True,
                'Description': 'string',
                'DeviceIndex': 0,
                'Groups': [vpc.security_group_id],
                'SubnetId': vpc.subnet_id,
            }],
        )['Instances'][0]['InstanceId']

        # Wait for the instance to start, check every 5 seconds for 10 minutes
        LOGGER.info('Waiting on build instance %s', instance_id)
        self.ec2.get_waiter('instance_running').wait(
            InstanceIds=[instance_id], WaiterConfig={'Delay': 5, 'MaxAttempts': 120}
        )

        LOGGER.info('Build instance %s running', instance_id)
        return instance_id

    def get_volume_id(self, instance_id: str, device_name: str) -> Optional[str]:
        """
        Try to get the volume ID for an instance disk device

        Returns None if it can't be found
        """

        response = self.ec2.describe_instances(InstanceIds=[instance_id])
        return next(
            (
                entry['Ebs']['VolumeId']
                for entry in response['Reservations'][0]['Instances'][0]['BlockDeviceMappings']
                if entry['DeviceName'] == device_name
            ),
            None,
        )

    def wait_on_snapshot(
        self, snapshot_id: str, delay: float = 2.0, max_attempts: int = 300
    ) -> None:
        """
        Waits for a snapshot to be complete and logs progress to a progress bar

        This is really only useful for very large volumes because AWS doesn't present percentages
        granularly, usually only jumping from 0 to 100 in a single step.
        """

        pbar = self.config.enlighten_manager.counter(total=100, desc=snapshot_id, leave=False)

        for _ in range(max_attempts):
            time.sleep(delay)
            snapshot = self.ec2.describe_snapshots(SnapshotIds=[snapshot_id])['Snapshots'][0]
            if progress := snapshot.get('Progress'):
                pbar.count = int(progress[:-1])  # Remove percent sign and convert to int
                pbar.refresh()

            if snapshot['State'] == 'completed':
                pbar.close(clear=True)
                return

            if snapshot['State'] == 'error':
                pbar.close(clear=True)
                raise ImogenAWSError(f"Snapshot {snapshot_id} has a status value of 'error'")

    def volume_to_ami(self, volume_id: str) -> str:
        """
        Convert a volume to an AMI

        The volume is first converted to a snapshot which can take some time
        Then the snapshot is registered as an AMI

        Returns the ID for the new AMI
        """

        LOGGER.info('Converting volume %s to ami %s', volume_id, self.aws_config.ami_name)

        # Take a snapshot of volume
        snapshot_id = self.ec2.create_snapshot(
            VolumeId=volume_id,
            Description='Backing snapshot for AMI',
            TagSpecifications=[{
                'ResourceType': 'snapshot',
                'Tags': [{'Key': 'Name', 'Value': self.aws_config.ami_name}]
                }],
        )['SnapshotId']

        # Wait for snapshot to complete. Check every 2 seconds for 10 minutes
        LOGGER.info('Waiting on snapshot %s to be complete', snapshot_id)
        self.ec2.get_waiter('snapshot_completed').wait(
            SnapshotIds=[snapshot_id], WaiterConfig={'Delay': 2, 'MaxAttempts': 300}
        )

        image_id = self.ec2.register_image(
            Architecture=self.aws_config.arch,
            BlockDeviceMappings=[{
                'DeviceName': '/dev/sda1',
                'Ebs': {'SnapshotId': snapshot_id, 'VolumeType': 'gp3'},
            }],
            Name=self.aws_config.ami_name,
            TagSpecifications=[{
                'ResourceType': 'image',
                'Tags': [
                    {'Key': 'short_name', 'Value': self.config.name},
                ],
            }],
            RootDeviceName='/dev/sda1',
            SriovNetSupport='simple',
            VirtualizationType='hvm'
        )['ImageId']

        # Wait for image to be available. Check every 2 seconds for 10 minutes
        self.ec2.get_waiter('image_available').wait(
            ImageIds=[image_id], WaiterConfig={'Delay': 2, 'MaxAttempts': 300}
        )

        LOGGER.info('AMI %s is now available', image_id)

        return image_id

    def terminate_instance(self, instance_id: str) -> None:
        """
        Terminates an image and then waits for the state to reflect termination
        """

        LOGGER.info('Terminating instance %s', instance_id)

        self.ec2.terminate_instances(InstanceIds=[instance_id])

        # Wait for the image to terminate. Check every 2 seconds for 10 minutes
        self.ec2.get_waiter('instance_terminated').wait(
                InstanceIds=[instance_id], WaiterConfig={'Delay': 2, 'MaxAttempts': 300}
        )

    def import_image(self, image: Path) -> tuple[str, str]:
        """
        Import an image as an AMI
        """

        waiter_config = {'Delay': 1, 'MaxAttempts': 600}  # Check every second for 10 minutes
        snapshot_id = self.upload_snapshot(image)

        LOGGER.info('Finalizing snapshot %s', snapshot_id)
        self.ec2.get_waiter('snapshot_completed').wait(
            SnapshotIds=[snapshot_id], WaiterConfig=waiter_config
        )

        LOGGER.info(
            'Registering snapshot %s Build AMI %s', snapshot_id,  self.aws_config.build_ami_name
        )
        image_id = self.ec2.register_image(
            Architecture=self.aws_config.arch,
            BlockDeviceMappings=[{
                'DeviceName': '/dev/sda1',
                'Ebs': {
                    'SnapshotId': snapshot_id,
                    'VolumeType': 'gp3',
                },
            }],
            EnaSupport=True,
            Name=self.aws_config.build_ami_name,
            TagSpecifications=[{
                'ResourceType': 'image',
                'Tags': [{'Key': 'architecture', 'Value': self.aws_config.arch}],
            }],
            RootDeviceName='/dev/sda1',
            SriovNetSupport='simple',
            VirtualizationType='hvm'
        )['ImageId']

        self.ec2.get_waiter('image_available').wait(ImageIds=[image_id], WaiterConfig=waiter_config)

        return image_id, snapshot_id

    def upload_snapshot(self, image: Path) -> str:
        """
        Create an EBS snapshot of a local image
        """

        LOGGER.info('Uploading image %s to snapshot in AWS region %s',
                    image, self.aws_config.region)

        # Set the max pool to thread size so image uploads aren't stalled
        client = self.session.client(
            'ebs', config=botocore.config.Config(max_pool_connections=WORKERS)
        )
        image_size = os.path.getsize(image)
        snapshot_id = client.start_snapshot(
            VolumeSize=ceil(image_size / 2**30), Description=self.aws_config.build_ami_name
        )['SnapshotId']

        pbar = self.config.enlighten_manager.counter(
            total=ceil(image_size / BLOCKSIZE),
            desc='Uploading build AMI',
            unit='blocks',
            leave=False,
        )

        block_num = 0

        try:
            # Run upload in threads to speed it up
            with concurrent.futures.ThreadPoolExecutor(max_workers=WORKERS) as executor:
                futures = []
                with image.open('rb') as source:

                    while True:
                        data = source.read(BLOCKSIZE)
                        if not data:
                            break
                        data = data.ljust(BLOCKSIZE, b'\0')  # Fill last block with null
                        checksum = b64encode(sha256(data).digest()).decode()

                        futures.append(
                            executor.submit(
                                client.put_snapshot_block,
                                SnapshotId=snapshot_id,
                                BlockIndex=block_num,
                                BlockData=data,
                                DataLength=BLOCKSIZE,
                                Checksum=checksum,
                                ChecksumAlgorithm='SHA256'
                            )
                        )
                        block_num += 1

                for future in concurrent.futures.as_completed(futures):
                    if exception := future.exception():
                        raise exception
                    pbar.update()
        except:  # noqa
            self.ec2.delete_snapshot(SnapshotId=snapshot_id)
            raise

        pbar.close(clear=True)
        client.complete_snapshot(SnapshotId=snapshot_id, ChangedBlocksCount=block_num)

        return snapshot_id
