import tempfile


def get_temporary_file_path() -> str:
    """Generates a temporary file

    Returns:
        str: the path to the temporary file
    """
    ABSOLUTE_PATH: int = 1
    temporary_file = tempfile.mkstemp()

    return temporary_file[ABSOLUTE_PATH]
