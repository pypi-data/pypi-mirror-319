# Copyright 2024 - 2025 Avram Lubkin, All Rights Reserved

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
Imogen Configuration Module
"""

import argparse
import warnings
from datetime import datetime
from enum import Enum
from functools import cached_property
from ipaddress import IPv4Network
from pathlib import Path
from typing import Annotated, Optional, Self, Type

import enlighten

from ruamel.yaml import YAML
from ruamel.yaml.error import YAMLError
from pydantic import (
    BaseModel, AnyUrl, field_validator, ValidationError, model_validator, computed_field, Field
)

from pykickstart.constants import KS_SHUTDOWN
from pykickstart.errors import KickstartError, KickstartWarning, KickstartVersionError
import pykickstart.version
from pykickstart.parser import KickstartParser, preprocessKickstart

from imogen.exceptions import ImogenConfigError
from imogen.util import Checksum, EventTimer


class AWSArch(str, Enum):  # In 3.11+ we could use StrEnum
    """
    Enumeration for AWS architectures

    https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_RegisterImage.html#API_RegisterImage_RequestParameters
    """

    # pylint: disable=invalid-name
    i386 = 'i386'
    x86_64 = 'x86_64'
    arm64 = 'arm64'
    x86_64_mac = 'x86_64_mac'
    arm64_mac = 'arm64_mac'


class LogLevel(str, Enum):
    """
    Enumeration for log levels

    https://docs.python.org/3/library/logging.html#logging-levels
    """

    DEBUG = 'DEBUG'
    INFO = 'INFO'
    WARNING = 'WARNING'
    ERROR = 'ERROR'
    CRITICAL = 'CRITICAL'

    @classmethod
    def _missing_(cls: Type['LogLevel'], value: str) -> 'LogLevel':  # type: ignore[override]
        if rtn := next((member for member in cls if member.value == value.upper()), None):
            return rtn

        raise ValueError("Unknown log level '{value}'")


class Source(BaseModel):
    """
    Model for 'source' section of configuration

    This defines the source ISO the build image is based on
    """

    # Download even when we have a local copy
    always_download: bool = False

    # URL for ISO
    url: str

    # Checksum value (usually unset and determined dynamically)
    checksum: Optional[Checksum] = None

    # URL for checksum file. Usually determined dynamically
    # Expected file should have a line in the format HASH_ALGORITHM (FILENAME) = CHECKSUM
    checksum_url: Optional[str] = None

    @field_validator('url', 'checksum_url')
    @classmethod
    def check_url(cls, value: str) -> str:
        """
        Validate a URL.
        This allows us to use Pydantic's validation and keep strings
        We could use Pydantic's AnyUrl directly, but it has a couple issues:
            - It will sometimes append a slash to an address (#7186)
            - It's not easy to create a new object based on an old object
        """

        AnyUrl(value)
        return value


class BuildImage(BaseModel):
    """
    Model for 'build_image' section of configuration

    This defines the new build image
    """

    source: Source

    # Search in grub.conf, grub.cfg, and isolinux.cfg  # pylint: disable=wrong-spelling-in-comment
    # Uses the same pattern and replacement behavior as re.sub
    config_substitutions: dict[str, str] = {}

    # Timeout for GRUB and ISOLinux menus
    config_timeout: Optional[int] = None

    # Path to implantisomd5 executable. Looks in path if not provided
    implantisomd5_path: Optional[Path] = None

    # Additional files or directories to add to image. They get added to the image root
    include: tuple[Path, ...] = ()

    # Path to kickstart file that gets injected into image
    kickstart: Path

    # Check syntax for this kickstart release. Corresponds to Fedora and RHEL releases
    kickstart_version: str = 'RHEL9'

    # Overwrite the file if it exist. Errors if false, and file exists.
    overwrite: bool = False

    # Local path to write the build image to
    path: Optional[Path] = None

    # Path to xorriso executable. Looks in path if not provided
    xorriso_path: Optional[Path] = None

    @field_validator('kickstart')
    @classmethod
    def check_is_file(cls, value: Path) -> Path:
        """
        Checks to make sure file exists and is a regular file
        """

        if not value.is_file():
            raise ValueError('File not found')
        return value

    @field_validator('kickstart_version', mode='before')
    @classmethod
    def check_kickstart_version(cls, value: str) -> str:
        """
        Validates the kickstart version is one supported by the pykickstart library
        """

        if not isinstance(value, str):
            raise TypeError(f'Must be a string, received {type(value)}')

        try:
            # This is inefficient, but keeps things human-readable
            return pykickstart.version.versionToString(pykickstart.version.stringToVersion(value))
        except KickstartVersionError as e:
            raise ValueError(
                f'Invalid kickstart version specified. Must be one of: {', '.join(pykickstart.version.versionMap)}'
            ) from e

    @model_validator(mode='after')
    def check_kickstart(self) -> Self:
        """
        Checks to make sure file exists and is a regular file

        Inspired by https://github.com/pykickstart/pykickstart/blob/master/tools/ksvalidator.py
        """

        with warnings.catch_warnings(action='error', category=KickstartWarning):

            try:
                processed_file = preprocessKickstart(str(self.kickstart))
                if processed_file is None:
                    raise ValueError('File is empty')

                parser = KickstartParser(
                    handler=pykickstart.version.makeVersion(self.kickstart_version),
                    followIncludes=False,
                )
                parser.readKickstart(processed_file)

            except (KickstartError, KickstartWarning) as e:
                raise ValueError(
                    f'Error parsing kickstart file [{e.__class__.__name__}]: {e}'
                ) from e

            # Make sure machine will shutdown if successful
            if parser.handler.commands['poweroff'].action is not KS_SHUTDOWN:
                raise ValueError(
                    "Kickstart file must contain either the 'poweroff' or 'shutdown' commands"
                )

        return self


class AWS(BaseModel, use_enum_values=True):
    """
    Model for AWS section of configuration

    This defines parameters for AWS to build an AMI
    """

    # Name for AMI. If not set, will default to image date {name} {%Y-%m-%d_%H%M} (arch)
    ami_name: Optional[str] = None

    # Number of AMIs to keep at one time, must be greater than 0
    ami_max: Annotated[int, Field(gt=0)] = 3

    # Size of target AMI volume in GiB
    ami_volume_size: int = 20

    # Architecture to use for instances
    arch: AWSArch = AWSArch.x86_64

    # Name for the temporary AMI use to do the build. By default is based on image name
    build_ami_name: Optional[str] = None

    # Instance type to use for build
    instance_type: str = 't3.small'

    # AWS profile to use. If not specified, the default profile is used
    profile: Optional[str] = None

    # AWS region to perform operations in. If unset, it will use the region for the default profile
    region: Optional[str] = None

    # CIDR for VPC subnet
    vpc_subnet: str = '10.9.8.0/24'

    # VPC name for building AMI
    vpc_name: Optional[str] = None

    @field_validator('vpc_subnet')
    @classmethod
    def check_kickstart_version(cls, value: str) -> str:
        """Check CIDR value. It will error if it's not a valid CIDR"""

        IPv4Network(value, strict=True)
        return value


class Logging(BaseModel):
    """
    Model for 'logging' section of configuration

    Logging options
    """

    # Log level
    level: LogLevel = LogLevel.INFO

    # Message format, see https://docs.python.org/3/library/logging.html#logrecord-attributes
    format: str = '%(asctime)s %(levelname)s [%(name)s] %(message)s'

    # Format of timestamp, see time.strftime() for details
    timestamp_format: str = '%Y-%m-%d %H:%M:%S'


class CommandLine(BaseModel):
    """
    Model for CLI arguments
    """

    image: Optional[Path]
    aws: bool = False


class Config(BaseModel, arbitrary_types_allowed=True):
    """
    Main configuration object

    All other models are children
    """

    # General name for build. Used to generate default values
    name: str = 'image'

    # Working directory. Defaults to current directory
    working_dir: Path = Path()

    command_line: CommandLine
    logging: Logging
    build_image: Optional[BuildImage] = None
    aws: Optional[AWS] = None

    @computed_field(repr=False)  # type: ignore[prop-decorator]
    @cached_property
    def enlighten_manager(self) -> enlighten.Manager:
        """Common Enlighten manager instance for generating progress bars"""
        return enlighten.get_manager()

    @computed_field(repr=False)  # type: ignore[prop-decorator]
    @cached_property
    def start_time(self) -> datetime:
        """Program start time"""
        return datetime.now()

    @computed_field(repr=False)  # type: ignore[prop-decorator]
    @cached_property
    def timer(self) -> EventTimer:
        """Program event timer"""
        return EventTimer()

    @model_validator(mode='after')
    def apply_defaults(self) -> Self:
        """
        Sets values that can not be interpreted in the initial run
        """

        if self.build_image and not self.build_image.path:
            self.build_image.path = self.working_dir / f'{self.name}-build.iso'

        if self.aws:
            if not self.aws.ami_name:
                self.aws.ami_name = f'{self.name} {self.start_time:%Y-%m-%d_%H%M} ({self.aws.arch})'

            if not self.aws.build_ami_name:
                build_image = self.command_line.image or getattr(self.build_image, 'path', None)
                if build_image is None:
                    raise ImogenConfigError('No image specified and image build disabled')

                self.aws.build_ami_name = (
                    f'{build_image.stem} {self.start_time:%Y-%m-%d_%H%M} ({self.aws.arch})'
                )

            if not self.aws.vpc_name:
                self.aws.vpc_name = f'{self.name} image build'

        return self


def parse_config(filepath: Path, cli_options: argparse.Namespace) -> Config:
    """
    Parse a YAML configuration file

    Keys passed in skip_sections are removed before validation
    Returns configuration object
    """

    if not filepath.is_file():
        raise ImogenConfigError(f'Configuration file can not be found at {filepath}')

    # Parse the configuration file
    try:
        with filepath.open() as config:
            parsed = YAML().load(config)
    except (YAMLError) as e:
        raise ImogenConfigError(
            f'An error occurred parsing config file at {filepath}:\n{e}'
        ) from e

    # Add the command_line options so they get included in the configuration
    parsed['command_line'] = parsed.get('command_line', {}) | (vars(cli_options))

    # Remove unused sections so they won't be incomplete
    if parsed['command_line'].get('image'):
        parsed.pop('build_image', None)

    if not parsed['command_line'].get('aws'):
        parsed.pop('aws', None)

    # Generate configuration object
    try:
        return Config.model_validate(parsed)
    except (ValidationError) as e:
        raise ImogenConfigError(
            f'An error occurred validating config file at {filepath}:\n{e}'
        ) from e
