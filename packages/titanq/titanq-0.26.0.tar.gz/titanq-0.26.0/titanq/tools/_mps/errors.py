# Copyright (c) 2024, InfinityQ Technology, Inc.
from titanq.errors import TitanqError


class MpsParsingError(TitanqError):
    """Base class for any error related to the MPS files parsing module"""

class MpsConfiguredModelError(MpsParsingError):
    """Passed model is pre-configured"""

class MpsMissingValueError(MpsParsingError):
    """A required value is missing"""

class MpsMissingSectionError(MpsParsingError):
    """A required section is missing"""

class MpsMalformedFileError(MpsParsingError):
    """The file is malformed"""

class MpsUnexpectedValueError(MpsParsingError):
    """Found an unexpected value"""

class MpsUnsupportedError(MpsParsingError):
    """Found an unsupported value"""
