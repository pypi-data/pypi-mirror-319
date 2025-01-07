# Copyright 2024 - 2025 Avram Lubkin, All Rights Reserved

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
Imogen ISO Module
"""

import os
import logging
import re
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Optional, Sequence, Protocol
from urllib.parse import urlparse

import requests

from imogen.exceptions import (
    ImogenChecksumError, ImogenImportError, ImogenBuildImageError, ImogenConfigError,
    ImogenImplantisomd5Error,
)
from imogen.config import Config, BuildImage
from imogen.util import Checksum, Downloader, import_from_file, get_command, Xorriso


# This is usually in /usr/bin, not a path we can import from
if mkksiso_path := shutil.which('mkksiso'):
    try:
        mkksiso = import_from_file('mkksiso', mkksiso_path)
    except (TypeError, ValueError, AttributeError) as e:
        raise ImogenImportError('Unable to import mkksiso. Is it installed?') from e
else:
    raise ImogenImportError('Unable to import mkksiso. Is it installed?')

LOGGER = logging.getLogger(__name__)

# format: HASH_ALGORITHM (FILENAME) = CHECKSUM
RE_CHECKSUM = re.compile(r'^(\w+) \((\S+)\) = (\w+)$')


class ISO:  # pylint: disable=too-many-instance-attributes
    """
    CLI operations interface
    """

    def __init__(self, config: Config) -> None:

        # Validate we have an configuration section and use an attribute so the type checker knows
        if config.build_image is None:
            raise ImogenConfigError('No Build Image configuration defined')
        self.build_image_config: BuildImage = config.build_image
        self.source_config = config.build_image.source

        # We have to check this here because it's potentially dynamic
        if config.build_image.path is None:
            raise ImogenConfigError('No path specified for build image')
        self.path: Path = config.build_image.path

        self.config = config
        self.session = requests.Session()

        parsed_url = urlparse(self.source_config.url)
        self.source_iso_path: Path = self.config.working_dir / os.path.basename(parsed_url.path)

        self.xorriso = Xorriso(config.build_image.xorriso_path)
        self.implantisomd5 = get_command('implantisomd5', config.build_image.implantisomd5_path)

    def build(self) -> Path:
        """
        Main entry point for building ISO
        """

        with self.config.timer.start('Download source', 'Build ISO'):
            self.download()
        with self.config.timer.start('Prepare ISO', 'Build ISO'):
            self.generate_iso()

        return self.path

    def get_url_checksum(self) -> Checksum | None:
        """
        Based on the URL, attempts to find the checksum from common locations
        """

        if self.source_config.checksum:
            LOGGER.debug(
                'Found %s checksum in config: %s',
                self.source_config.checksum.algorithm.upper(), self.source_config.checksum.value
            )
            return self.source_config.checksum

        parsed_url = urlparse(self.source_config.url)

        # Get list of possible checksums
        if self.source_config.checksum_url:
            candidates: tuple[str, ...] = (self.source_config.checksum_url,)
        else:
            candidates = (
                # Append .CHECKSUM to file name
                parsed_url._replace(path=f'{parsed_url.path}.CHECKSUM').geturl(),
                # File named CHECKSUM in same directory
                parsed_url._replace(path=f'{os.path.dirname(parsed_url.path)}/CHECKSUM').geturl(),
            )

        contents = ''
        for candidate in candidates:
            response = self.session.get(candidate, timeout=30)
            LOGGER.debug(
                'Received %d response looking for checksum at url: %s',
                response.status_code, candidate
            )

            if response.status_code == 200:
                contents = response.text
                break
        else:
            LOGGER.debug('No checksum file found for url: %s', self.source_config.url)
            return None

        checksum_found = False
        file_name = os.path.basename(parsed_url.path)
        for line in contents.splitlines():
            if match := RE_CHECKSUM.match(line):
                checksum_found = True
                if match[2] == file_name:
                    LOGGER.debug(
                        "Found %s checksum '%s' in file at url: %s", match[1], match[3], candidate
                    )
                    return Checksum(match[3], match[1])

        if checksum_found:
            LOGGER.debug(
                "Found valid checksums but none matching '%s' at url: %s", file_name, candidate
            )
        else:
            LOGGER.debug('Unable to find checksum in file at url: %s', candidate)

        return None

    def download(self) -> None:
        """
        Download ISO and verify checksum
        """

        # See if we can locate a checksum for the remote file
        LOGGER.info('Locating checksum for source image')
        checksum = self.get_url_checksum()

        if checksum is None:
            raise ImogenChecksumError('Unable to retrieve valid checksum')

        # Check local file and skip downloading if it matches
        if (
            not self.build_image_config.source.always_download
            and checksum.check_file(self.source_iso_path)
        ):
            LOGGER.info('Using cached source image at %s', self.source_iso_path)
            return

        # Download file
        LOGGER.info('Downloading source image from %s', self.source_config.url)
        Downloader(self.config, self.source_config.url, self.source_iso_path).threaded_download()

        # Verify download
        if not checksum.check_file(self.source_iso_path):
            raise ImogenChecksumError('Checksum mismatch for {file_path}')

    def inject_checksum(self, path: Path | str) -> None:
        """
        Use implantisomd5 to inject checksum into ISO
        """

        try:
            subprocess.check_output((self.implantisomd5, path), stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as e:
            raise ImogenImplantisomd5Error(
                f"Failure running {self.implantisomd5} {path}: {e.output.decode('utf-8').strip()}"
            ) from e

    def generate_iso(self) -> None:
        """
        Creates new ISO based on the source ISO
        """

        LOGGER.info('Processing files for build image')
        # Check to see if the output file exists
        if self.path.exists():
            # If overwrite is set, delete it
            if self.build_image_config.overwrite:
                self.path.unlink()
            # Otherwise raise an error
            else:
                raise ImogenBuildImageError(
                    f'Unable to create new build image because file exists: {self.path}'
                )

        volume_id, files = self.xorriso.get_iso_details(self.source_iso_path)
        read_args: list[str | Path] = [
            '-osirrox', 'on:o_excl_off:auto_chmod_on', '-indev', self.source_iso_path, '--'
        ]
        write_args: list[str | Path] = [
            '-indev', self.source_iso_path, '-outdev', self.path, 'boot_image', 'any', 'replay'
        ]
        to_modify: dict[str, tuple[ModifyProtocol, list[str]]] = {
            'isolinux.cfg': (modify_isolinux, []),
            'grub.conf': (modify_grub1, []),
            'grub.cfg': (modify_grub2, []),
        }

        with tempfile.TemporaryDirectory(prefix='imogen-') as temp_dir:

            # Get a list of files to extract
            for file_ in files:
                basename = os.path.basename(file_)

                if basename in to_modify:
                    tmp_path = os.path.join(temp_dir, file_)
                    to_modify[basename][1].append(tmp_path)
                    read_args.extend(('-extract', file_, tmp_path))
                    write_args.extend(('-update', tmp_path, file_))

            # Extract files
            self.xorriso.run(*read_args)

            # Modify configuration files
            for func, files in to_modify.values():
                for tmp_path in files:
                    func(
                        path=tmp_path,
                        substitutions=self.build_image_config.config_substitutions,
                        kernel_args=(
                            f'inst.ks=hd:LABEL={volume_id}:/{self.build_image_config.kickstart.name}',
                        ),
                        timeout=self.build_image_config.config_timeout,
                    )

            # Add additional files to ISO
            write_args.extend(('-map', self.build_image_config.kickstart, self.build_image_config.kickstart.name))
            for file_path in self.build_image_config.include:
                write_args.extend(('-map', file_path, file_path.name))

            # Create new ISO
            LOGGER.info('Creating build image at %s', self.path)
            self.xorriso.run(*write_args)

            LOGGER.info('Injecting checksum into build image')
            self.inject_checksum(self.path)


class ConfigFileProcessor:  # pylint: disable=too-few-public-methods
    """
    Generic processor intended to be customized for specific configuration files
    """

    def __init__(self, re_kernel: re.Pattern, re_timeout: re.Pattern, tmpl_timeout: str):
        self.re_kernel = re_kernel
        self.re_timeout = re_timeout
        self.tmpl_timeout = tmpl_timeout

    def modify(
        self, path: Path | str, substitutions: dict[str, str],
        kernel_args: Sequence[str], timeout: Optional[int] = None
    ) -> None:
        """
        Modify file in place

        Performs any substitutions before appending kernel arguments and setting timeout
        """

        original_file = Path(path)
        new_file = original_file.with_suffix('.new')

        with original_file.open('r', encoding='utf-8') as original:
            with new_file.open('w', encoding='utf-8') as new:

                # Walk through original file line by line
                for line in original:

                    # Process any replacements
                    for pattern, replacement in substitutions.items():
                        line = re.sub(pattern, replacement, line)

                    # Add any new kernel arguments
                    if kernel_args and self.re_kernel.match(line):
                        line = f"{line.rstrip()} {' '.join(kernel_args)}\n"

                    # Set timeout, if given
                    elif timeout is not None and self.re_timeout.match(line):
                        line = self.tmpl_timeout.format(timeout=timeout)
                        timeout = None

                    # Write line to new file
                    new.write(line)

                # If we haven't set the timeout, add it at the end
                if timeout is not None:
                    new.write(self.tmpl_timeout.format(timeout=timeout))

        # Replace the original file
        new_file.replace(original_file)


class ModifyProtocol(Protocol):  # pylint: disable=too-few-public-methods
    """Typing protocol for ConfigFileProcessor.modify"""
    def __call__(
        self, path: Path | str, substitutions: dict[str, str],
        kernel_args: Sequence[str], timeout: Optional[int] = None
    ) -> None: ...


modify_isolinux = ConfigFileProcessor(
    re_kernel=re.compile(r'^\s*append(?!.*inst\.rescue).*$'),
    re_timeout=re.compile(r'timeout\s+\d+'),
    tmpl_timeout='timeout {timeout}\n',
).modify

modify_grub1 = ConfigFileProcessor(
    re_kernel=re.compile(r'^\s*kernel?(?!.*inst\.rescue).*$'),
    re_timeout=re.compile(r'timeout\s+\d+'),
    tmpl_timeout='timeout {timeout}\n',
).modify

modify_grub2 = ConfigFileProcessor(
    re_kernel=re.compile(r'^\s*linux(efi)?(?!.*inst\.rescue).*$'),
    re_timeout=re.compile(r'set timeout=\d+'),
    tmpl_timeout='set timeout={timeout}\n',
).modify
