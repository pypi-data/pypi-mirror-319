# Copyright 2024 - 2025 Avram Lubkin, All Rights Reserved

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
Imogen CLI module
"""

import argparse
import logging
import sys
from pathlib import Path
from typing import Sequence

from imogen.exceptions import ImogenError
from imogen.config import parse_config
from imogen.iso import ISO
from imogen.platform.aws import AWS


LOGGER = logging.getLogger('imogen')


def parse_args(args: Sequence[str] | None = None) -> argparse.Namespace:
    """
    Command line option parsing
    """

    parser = argparse.ArgumentParser(description='Imogen system image generator')

    parser.add_argument('-c', '--config', required=True, type=Path,
                        metavar='CONFIG_FILE', help='Path to YAML configuration file')

    parser.add_argument('-i', '--image', dest='image', type=Path, metavar='IMAGE_FILE',
                        help='Do not generate ISO, use provide file instead')

    providers = parser.add_argument_group('Providers', description='Providers to build image on')

    providers.add_argument('--aws', action='store_true', help='Build AMI on AWS')

    return parser.parse_args(args)


def run(args: Sequence[str] | None = None) -> None:
    """
    CLI entry point
    """

    try:

        cli_options = parse_args(args)
        config = parse_config(cli_options.config, cli_options)

        logging.basicConfig(
            level=getattr(logging, config.logging.level),
            datefmt=config.logging.timestamp_format,
            format=config.logging.format,
        )

        image = config.command_line.image or ISO(config=config).build()

        if config.command_line.aws:
            if ami_id := AWS(config).build(image):
                print(f'Created AMI {ami_id} on AWS')

    except ImogenError as e:
        LOGGER.error(e)
        sys.exit(42)

    print(config.timer)
