from abc import ABC, abstractmethod
from typing import Tuple

from harmony.constants import ColorFormat
from harmony.models import Color


class WritingStrategy(ABC):
    """Interface for output file writting strategies"""

    EXTENSION: str = ""

    @abstractmethod
    def write(self, colors: Tuple[Color, ...], final_file_path: str):
        """Write the sorted colors to a new file

        Args:
            colors (Tuple[Color, ...]): colors to written
            final_file_path (str): path to the new file
        """


class DefaultWriting(WritingStrategy):
    """Writting strategy that results in a simple text file"""

    def __init__(self, color_format):
        color_string_getter_dict = {
            ColorFormat.HEXCODE: self._get_hexcode_string,
            ColorFormat.RGB: self._get_rgb_string,
            ColorFormat.SAME_AS_INPUT: self._get_color_as_input_format,
        }

        self._get_color_string = color_string_getter_dict[color_format]

    def write(self, colors: Tuple[Color, ...], final_file_path: str):
        """Write colors to a text file

        Args:
            colors (Tuple[Color, ...]): colors to be written
            final_file_path (str): path to the file where the colors will be passed
        """
        with open(final_file_path, "w", encoding="utf8") as final_file:
            final_file.write(self._get_file_content(colors))

    def _get_file_content(self, colors: Tuple[Color, ...]) -> str:
        file_content: str = ""

        for color in colors:
            file_content += self._get_color_string(color)

        return file_content

    def _get_color_as_input_format(self, color: Color) -> str:
        if self._is_input_format_as_hexcode(color):
            return self._get_hexcode_string(color)

        return self._get_rgb_string(color)

    @staticmethod
    def _is_input_format_as_hexcode(color: Color) -> bool:
        return color.original_format == ColorFormat.HEXCODE

    def _get_hexcode_string(self, color: Color) -> str:
        return f"{color.hexcode} {color.description}\n"

    def _get_rgb_string(self, color: Color) -> str:
        return (
            f"({color.rgb_red}, {color.rgb_green}, {color.rgb_blue}) "
            + f"{color.description}\n"
        )
