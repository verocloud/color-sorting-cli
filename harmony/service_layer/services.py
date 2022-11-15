import re
from typing import Dict, Iterator, List, TextIO, Tuple, Type

from harmony.constants import ColorFormat, Directions, SortingStrategyName
from harmony.exceptions import InvalidColorException
from harmony.models import RGB, Color
from harmony.service_layer.sorting_strategies import (
    AlternatedStepSorting,
    HillbertSorting,
    HSLSorting,
    HSVSorting,
    LuminositySorting,
    RGBSorting,
    SortingStrategy,
    StepSorting,
)


def get_final_file_path(
    source_file: TextIO, sorting_strategy: SortingStrategyName, suffix: str
) -> str:
    """Return the path to the file with the processed data

    Args:
        source_file (TextIO): original file

    Returns:
        str: path to the processed data file
    """
    source_file_path = source_file.name
    index_of_extension = source_file_path.rfind(".")

    if index_of_extension >= 0:
        extension = source_file_path[index_of_extension:]
        return (
            f"{source_file_path[:index_of_extension]}_{sorting_strategy}{suffix}"
            + extension
        )

    return f"{source_file_path}_{sorting_strategy}"


class ColorReader:
    """Service for reading colors from file"""

    def extract_from_file(self, colors_file: TextIO) -> List[Color]:
        """Extracts a list of colors from a file

        Args:
            file_path (str): path to the file with the colors

        Returns:
            List[Color]: list of colors extracted
        """
        color_strings = colors_file.readlines()

        return list(self._make_colors_list(color_strings))

    def _make_colors_list(self, color_strings: List[str]) -> Iterator[Color]:

        for color_string in color_strings:
            color_string = color_string.replace("\n", "")
            yield self._make_color_from_string(color_string)

    def _make_color_from_string(self, color_string: str) -> Color:
        hexcode_pattern = re.compile("^[#][a-zA-Z0-9]{3}([a-zA-Z0-9]{3})?")
        rgb_pattern = re.compile(
            "^[(][0-2]?[0-9]{1,2}[,][\\s]?[0-2]?[0-9]{1,2}[,][\\s]?[0-2]?[0-9]{1,2}[)]"
        )

        if hexcode_pattern.match(color_string):
            return self._make_color_from_hexcode(color_string)

        if rgb_pattern.match(color_string):
            return self._make_color_from_rgb(color_string)

        raise InvalidColorException(f"{color_string} does not match any valid format")

    def _make_color_from_hexcode(self, hexcode: str) -> Color:
        index_of_whitespace = hexcode.index(" ")
        index_after_whitespace = index_of_whitespace + 1
        description = hexcode[index_after_whitespace:]
        description = description.strip()

        hexcode = hexcode[:index_of_whitespace]

        have_six_digits = len(hexcode) == 7

        if not have_six_digits:
            hexcode = hexcode + hexcode[1:]

        red = int(hexcode[1:3], 16)
        green = int(hexcode[3:5], 16)
        blue = int(hexcode[5:], 16)
        rgb = RGB(red=red, green=green, blue=blue)

        hexcode = hexcode.lower()

        return Color(
            rgb=rgb,
            hexcode=hexcode,
            original_format=ColorFormat.HEXCODE,
            description=description,
        )

    def _make_color_from_rgb(self, rgb_string: str) -> Color:
        index_after_closing_parenthesis = rgb_string.index(")") + 1

        description = rgb_string[index_after_closing_parenthesis:]
        description = description.strip()

        rgb_string = rgb_string[:index_after_closing_parenthesis].replace(" ", "")
        rgb_string = rgb_string.replace("(", "")
        rgb_string = rgb_string.replace(")", "")

        red_string, green_string, blue_string = rgb_string.split(",")

        red = int(red_string)
        green = int(green_string)
        blue = int(blue_string)

        for amount in (red, green, blue):
            self._check_rgb_amount(amount)

        rgb = RGB(red=red, green=green, blue=blue)

        hexcode = "%02x%02x%02x" % (red, green, blue)
        hexcode = f"#{hexcode.lower()}"

        return Color(
            rgb=rgb,
            hexcode=hexcode,
            original_format=ColorFormat.RGB,
            description=description,
        )

    def _check_rgb_amount(self, amount: int) -> None:
        """Raise exception if amount not between 0 and 255"""
        is_amount_greater_or_equal_to_zero = amount >= 0
        is_amount_less_or_equal_to_255 = amount <= 255
        is_amount_between_zero_and_255 = (
            is_amount_greater_or_equal_to_zero and is_amount_less_or_equal_to_255
        )

        if not is_amount_between_zero_and_255:
            raise InvalidColorException(
                "The amount of red, green and blue needs to be between 0 and 255, "
                + f"{amount} is invalid"
            )


class ColorSorter:
    """Service for sorting colors"""

    strategy: SortingStrategy

    def __init__(self, strategy_name: SortingStrategyName):
        strategy_dict: Dict[SortingStrategyName, Type[SortingStrategy]] = {
            SortingStrategyName.RGB: RGBSorting,
            SortingStrategyName.HSV: HSVSorting,
            SortingStrategyName.HSL: HSLSorting,
            SortingStrategyName.STEP: StepSorting,
            SortingStrategyName.ALTERNATED_STEP: AlternatedStepSorting,
            SortingStrategyName.LUMINOSITY: LuminositySorting,
            SortingStrategyName.HILLBERT: HillbertSorting,
        }

        self.strategy = strategy_dict[strategy_name]()

    def sort(
        self, colors_to_sort: List[Color], direction: Directions
    ) -> Tuple[Color, ...]:
        """Sort a list of colors

        Args:
            colors_to_sort (List[Color]): the colors to be sorted

        Returns:
            Tuple[Color]: sorted set of colors
        """
        direction_dict = {
            Directions.FORWARD: lambda: self.strategy.sort(colors_to_sort),
            Directions.BACKWARD: lambda: self._sort_backwards(colors_to_sort),
        }
        return direction_dict[direction]()

    def _sort_backwards(self, colors_to_sort: List[Color]) -> Tuple[Color, ...]:
        sorted_colors = self.strategy.sort(colors_to_sort)
        colors_sorted_backwards: List[Color] = []

        for color in reversed(sorted_colors):
            colors_sorted_backwards.append(color)

        return tuple(colors_sorted_backwards)


class ColorWriter:
    """Service for writing colors to file"""

    def __init__(self, color_format: ColorFormat = ColorFormat.SAME_AS_INPUT):
        color_string_getter_dict = {
            ColorFormat.HEXCODE: self._get_hexcode_string,
            ColorFormat.RGB: self._get_rgb_string,
            ColorFormat.SAME_AS_INPUT: self._get_color_as_input_format,
        }

        self._get_color_string = color_string_getter_dict[color_format]

    def write_colors_to_file(self, colors: Tuple[Color, ...], final_file_path: str):
        """Write colors to passed file

        Args:
            colors (Tuple[Color]): colors to be written
            final_file_path (str): path to the file where the colors will be passed
        """

        file_content: str = ""

        for color in colors:
            file_content += self._get_color_string(color)

        with open(final_file_path, "w", encoding="utf8") as final_file:
            final_file.write(file_content)

    def _get_color_as_input_format(self, color: Color) -> str:
        is_input_format_as_hexcode = color.original_format == ColorFormat.HEXCODE

        if is_input_format_as_hexcode:
            return self._get_hexcode_string(color)

        return self._get_rgb_string(color)

    def _get_hexcode_string(self, color: Color) -> str:
        return f"{color.hexcode} {color.description}\n"

    def _get_rgb_string(self, color: Color) -> str:
        rgb = color.rgb
        return f"({rgb.red}, {rgb.green}, {rgb.blue}) {color.description}\n"
