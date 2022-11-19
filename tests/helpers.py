import tempfile


def get_temporary_file_path(**kwargs: object) -> str:
    """Generates a temporary file

    Returns:
        str: the path to the temporary file
    """
    ABSOLUTE_PATH: int = 1
    temporary_file = tempfile.mkstemp(**kwargs)

    return temporary_file[ABSOLUTE_PATH]
