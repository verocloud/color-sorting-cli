import os
import struct

from harmony.constants import ByteOrder, FloatComparisonTolerance
from harmony.exceptions import NoExtensionFoundException
from harmony.typing import Number


def float_to_bytes(value: float, byte_order: ByteOrder) -> bytes:
    """Convert a float into bytes

    Args:
        value (float): float to be converted

    Returns:
        bytes: float as an IEEE 754 binary representation
    """
    return struct.pack(f"{_get_byte_order_char(byte_order)}f", value)


def _get_byte_order_char(byte_order: ByteOrder) -> str:
    return {
        ByteOrder.LITTLE: "<",
        ByteOrder.BIG: ">",
    }[byte_order]


def _get_current_directory_path() -> str:
    return os.path.abspath(os.path.dirname(__file__))


def _get_resources_directory_path() -> str:
    return os.path.join(_get_current_directory_path(), "resources")


def get_resource(path: str) -> str:
    """Return the absolute path to the resource passed

    Args:
        path (str): path to the resource relative to the resources directory

    Returns:
        str: absolute path to the resourse
    """
    return os.path.join(_get_resources_directory_path(), path)


def difference_between(first_number: Number, second_number: Number) -> Number:
    """Return the result of the difference between both numbers passed"""
    return first_number - second_number


def quotient_between(first_number: Number, second_number: Number) -> Number:
    """Return the quotient of the division between both numbers passed"""
    return first_number / second_number


def absolute_difference_between(first_number: Number, second_number: Number) -> Number:
    """Return the absolute result of the difference between both numbers passed"""
    return abs(difference_between(first_number, second_number))


def are_almost_equal(
    first_number: float,
    second_number: float,
    tolerance: FloatComparisonTolerance = FloatComparisonTolerance.SEVEN_DECIMAL_PLACES,
) -> bool:
    """Return `True` if the difference between `first_number` and `second_number` is
    less than the `tolerance`"""
    return absolute_difference_between(first_number, second_number) < tolerance.value


def get_index_for_the_file_extension(file_path: str) -> int:
    """Return the index of the `.`(dot) separating the file name from the extension. If
    no extension is found, returns -1

    Args:
        file_path (str): path-like string

    Returns:
        int: index to the `.` separating extension and file name or -1
    """
    return file_path.rfind(".")


def does_file_name_have_extension(file_path: str) -> bool:
    """Return `True` if passed path-like string have extension"""
    return get_index_for_the_file_extension(file_path) >= 0


def get_extension_from_file_path(file_path: str) -> str:
    """Get extension from path-like string

    Args:
        file_path (str): path-like string

    Raises:
        NoExtensionFoundException: when string has no extension

    Returns:
        str: extension got
    """
    if does_file_name_have_extension(file_path):
        return file_path[get_index_for_the_file_extension(file_path) :]

    raise NoExtensionFoundException(f"The file path '{file_path}' has no extension")


def extract_extension_from_file_path(file_path: str) -> str:
    """Remove extension from path-like string

    Args:
        file_path (str): path-like string

    Raises:
        NoExtensionFoundException: when the file has no extension

    Returns:
        str: path-like string without extension
    """
    if does_file_name_have_extension(file_path):
        return file_path[: get_index_for_the_file_extension(file_path)]

    raise NoExtensionFoundException(f"The file path '{file_path}' has no extension")


def _does_hexcode_have_not_7_digits(string_to_count) -> bool:
    return len(string_to_count) != 7


def convert_hexcode_from_3_to_6_chars_form(hexcode: str) -> str:
    """Convert a hexcode string in 3 chars format to 6 chars format"""
    if _does_hexcode_have_not_7_digits(hexcode):
        hexcode = f"{hexcode}{hexcode[1:]}"

    return hexcode
