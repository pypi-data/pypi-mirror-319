# Copyright 2024 - 2025 Avram Lubkin, All Rights Reserved

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
Imogen exceptions module
"""


class ImogenError(Exception):
    """Base class for errors"""


class ImogenAWSError(Exception):
    """Errors related to AWS"""


class ImogenConfigError(ImogenError):
    """Exception class for configuration errors"""


class ImogenChecksumError(ImogenError):
    """Exception class for checksum errors"""


class ImogenImportError(ImogenError):
    """Exception class for import errors"""


class ImogenBuildImageError(ImogenError):
    """Exception class for errors creating the build image"""


class ImogenExternalCommandError(ImogenError):
    """Exception class for errors related to external commands"""


class ImogenXorrisoError(ImogenExternalCommandError):
    """Exception class for errors related to xorriso operations"""


class ImogenImplantisomd5Error(ImogenExternalCommandError):
    """Exception class for errors related to implantisomd5 operations"""
