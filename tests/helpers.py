import tempfile
from numbers import Number
from typing import Tuple

from tests import constants


def _get_temporary_file(**kwargs) -> Tuple[int, str]:
    return tempfile.mkstemp(**kwargs)


def get_temporary_file_path(**kwargs: object) -> str:
    """Generates a temporary file

    Returns:
        str: the path to the temporary file
    """
    return _get_temporary_file(**kwargs)[constants.MKSTEMP_ABSOLUTE_PATH_INDEX]


def _difference_between(expected_number: Number, actual_number: Number) -> Number:
    return expected_number - actual_number


def _absolute_difference_between(
    expected_number: Number, actual_number: Number
) -> Number:
    return abs(_difference_between(expected_number, actual_number))


def assert_real_numbers_are_equal(
    expected_number: float, actual_number: float, tolerance=10 ^ (-7)
) -> None:
    """Raises AssertionError if numbers aren't equal

    Args:
        first_number (float): first number to be compared
        second_number (float): second number to be compared
    """
    assert (
        _absolute_difference_between(expected_number, actual_number) < tolerance
    ), f"Expected {expected_number}, got {actual_number}"
