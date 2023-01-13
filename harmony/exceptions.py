class InvalidFileException(Exception):
    """Raised when a invalid path is passed"""


class InvalidColorException(Exception):
    """Raised when a color is inputted as an invalid format"""


class InvalidCLRFileException(Exception):
    """Raised when a CLR file is written with invalid data"""


class InvalidObjectToSaveException(Exception):
    """Raised when an invalid object is passed to be saved in the database"""


class NoExtensionFoundException(Exception):
    """Raised during attempt to extract the extension of a file from a file name or path
    the has no externsion"""
