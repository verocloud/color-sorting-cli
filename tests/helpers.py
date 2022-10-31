import tempfile


def get_temporary_file_path():
    ABSOLUTE_PATH: int = 1
    temporary_file = tempfile.mkstemp()

    return temporary_file[ABSOLUTE_PATH]
