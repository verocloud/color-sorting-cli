import os

from harmony.exceptions import NotAValidFileException


def check_for_file_path(path: str) -> None:
    if not os.path.exists(path):
        raise NotAValidFileException(f"{path} does not exists or is not a valid file")


def get_final_file_path(source_file_path: str) -> str:
    index_of_extension = source_file_path.rfind(".")

    if index_of_extension >= 0:
        extension = source_file_path[index_of_extension:]
        return f"{source_file_path[:index_of_extension]}_sorted{extension}"

    return f"{source_file_path}_sorted"
