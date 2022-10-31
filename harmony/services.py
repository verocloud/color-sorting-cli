import os
import re
from typing import Iterator, List
from harmony.exceptions import InvalidColorException, InvalidFileException
from harmony.models import RGB, Color


def check_for_file_path(path: str) -> None:
    """Raise exception if file does not exist

    Args:
        path (str): path to file to be verified

    Raises:
        InvalidFileException: when the file does not exists
    """
    if not os.path.exists(path):
        raise InvalidFileException(f"{path} does not exists")


def get_final_file_path(source_file_path: str) -> str:
    """Return the path to the file with the processed data

    Args:
        source_file_path (str): path to the original file

    Returns:
        str: path to the processed data file
    """
    index_of_extension = source_file_path.rfind(".")

    check_for_file_path(source_file_path)

    if index_of_extension >= 0:
        extension = source_file_path[index_of_extension:]
        return f"{source_file_path[:index_of_extension]}_sorted{extension}"

    return f"{source_file_path}_sorted"


class ColorExtractor:
    """Extractor of colors"""

    def extract_from_file(self, file_path: str) -> List[Color]:
        """Extracts a list of colors from a file

        Args:
            file_path (str): path to the file with the colors

        Returns:
            List[Color]: list of colors extracted
        """

        with open(file_path, "r", encoding="utf8") as colors_file:
            color_strings = colors_file.readlines()

        return [color for color in self._make_colors_list(color_strings)]

    def _make_colors_list(self, color_strings: List[str]) -> Iterator[Color]:

        for color_string in color_strings:
            color_string = color_string.replace("\n", "")
            yield self._make_color_from_string(color_string)

    def _make_color_from_string(self, color_string: str) -> Color:
        color_string = color_string.replace(" ", "")
        hexcode_pattern = re.compile("^[#][a-zA-Z0-9]{3}([a-zA-Z0-9]{3})?$")
        rgb_pattern = re.compile(
            "^[0-2]?[0-9]{1,2}[,][0-2]?[0-9]{1,2}[,][0-2]?[0-9]{1,2}$"
        )

        if hexcode_pattern.match(color_string):
            return self._make_color_from_hexcode(color_string)

        elif rgb_pattern.match(color_string):
            return self._make_color_from_rgb(color_string)

        raise InvalidColorException(f"{color_string} does not match any valid format")

    def _make_color_from_hexcode(self, hexcode: str) -> Color:
        have_six_digits = len(hexcode) == 7

        if not have_six_digits:
            hexcode = hexcode + hexcode[1:]

        red = int(hexcode[1:3], 16)
        blue = int(hexcode[3:5], 16)
        green = int(hexcode[5:], 16)
        rgb = RGB(red=red, blue=blue, green=green)

        hexcode = hexcode.lower()

        return Color(rgb=rgb, hexcode=hexcode)

    def _make_color_from_rgb(self, rgb_string: str) -> Color:
        red_string, blue_string, green_string = rgb_string.split(",")

        red = int(red_string)
        blue = int(blue_string)
        green = int(green_string)
        rgb = RGB(red=red, blue=blue, green=green)

        hexcode = ("#{:X}{:X}{:X}").format(rgb.red, rgb.blue, rgb.green)
        hexcode = hexcode.lower()

        return Color(rgb=rgb, hexcode=hexcode)
