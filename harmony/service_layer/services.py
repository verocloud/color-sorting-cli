import re
from typing import Dict, List, TextIO, Tuple, Type

from harmony.constants import Directions, SortingStrategyName
from harmony.data_access import ColorNamesStorage
from harmony.exceptions import InvalidColorException
from harmony.models import RGB, Color
from harmony.service_layer.converters import RGBToHSLConverter
from harmony.service_layer.reading_strategies import (
    HexcodeReading,
    ReadingStrategy,
    RGBReading,
)
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
from harmony.service_layer.writting_strategies import WritingStrategy
from harmony.utils import (
    does_file_name_have_extension,
    extract_extension_from_file_path,
    get_extension_from_file_path,
)


def get_final_file_path(
    source_file: TextIO,
    sorting_strategy: SortingStrategyName,
    suffix: str,
) -> str:
    """Return the path to the file with the processed data

    Args:
        source_file (TextIO): original file

    Returns:
        str: path to the processed data file
    """
    if does_file_name_have_extension(source_file.name):
        return (
            f"{extract_extension_from_file_path(source_file.name)}"
            + f"_{sorting_strategy}{suffix}"
            + f"{get_extension_from_file_path(source_file.name)}"
        )

    return f"{source_file.name}_{sorting_strategy}"


def get_path_with_extension(source_file: TextIO, extension: str) -> str:
    """Return the path to file with the given extension

    Args:
        source_file (TextIO): original file

    Returns:
        str: path to the converted file
    """
    if does_file_name_have_extension(source_file.name):
        return f"{extract_extension_from_file_path(source_file.name)}.{extension}"

    return f"{source_file.name}.{extension}"


class ColorReader:
    """Service for reading colors from file"""

    def __init__(self, must_generate_color_names: bool = True) -> None:
        self._must_generate_color_names = must_generate_color_names

    def extract_from_file(self, colors_file: TextIO) -> List[Color]:
        """Extracts a list of colors from a file

        Args:
            file_path (str): path to the file with the colors

        Returns:
            List[Color]: list of colors extracted
        """
        return self._make_colors_list(colors_file.readlines())

    def _make_colors_list(self, color_strings: List[str]) -> List[Color]:
        colors_list: List[Color] = []

        for color_string in color_strings:
            colors_list.append(self._make_color_from_raw_string(color_string))

        return colors_list

    def _make_color_from_raw_string(self, raw_string: str) -> Color:
        return self._make_color_from_string(raw_string.replace("\n", ""))

    def _make_color_from_string(self, color_string: str) -> Color:
        for pattern, strategy in self._get_color_factory_mapping().items():
            if re.compile(pattern).match(color_string):
                return self._make_color(color_string, strategy())

        raise InvalidColorException(
            color_string.replace("\n", "") + " does not match any valid format"
        )

    def _get_color_factory_mapping(self) -> Dict[str, Type[ReadingStrategy]]:
        return {
            self._get_hexcode_pattern(): HexcodeReading,
            self._get_rgb_pattern(): RGBReading,
        }

    @staticmethod
    def _get_hexcode_pattern() -> str:
        return "^[#][a-zA-Z0-9]{3}([a-zA-Z0-9]{3})?"

    @staticmethod
    def _get_rgb_pattern() -> str:
        return (
            "^[(][0-2]?[0-9]{1,2}[,][\\s]?[0-2]?[0-9]{1,2}[,][\\s]?[0-2]?"
            + "[0-9]{1,2}[)]"
        )

    def _make_color(
        self,
        color_string: str,
        strategy: ReadingStrategy,
    ):
        new_color = strategy.read(color_string)

        if self._must_generate_name(new_color):
            new_color.description = self._generate_color_name(new_color.rgb)

        return new_color

    def _must_generate_name(self, color: Color) -> bool:
        return (
            self._must_generate_color_names
            and not self._does_color_already_have_name(color)
        )

    @staticmethod
    def _does_color_already_have_name(color: Color):
        return len(color.description) > 0

    def _generate_color_name(self, rgb_values: RGB):
        with ColorNamesStorage() as storage:
            return storage.get_color_name_by_hsl(
                RGBToHSLConverter().make_hsl_from_rgb(rgb_values)
            )


class ColorSorter:
    """Service for sorting colors"""

    STRATEGY_MAPPING: Dict[SortingStrategyName, Type[SortingStrategy]] = {
        SortingStrategyName.RGB: RGBSorting,
        SortingStrategyName.HSV: HSVSorting,
        SortingStrategyName.HSL: HSLSorting,
        SortingStrategyName.STEP: StepSorting,
        SortingStrategyName.ALTERNATED_STEP: AlternatedStepSorting,
        SortingStrategyName.LUMINOSITY: LuminositySorting,
        SortingStrategyName.HILLBERT: HillbertSorting,
    }

    def __init__(self, strategy_name: SortingStrategyName):
        self.strategy: SortingStrategy = self.STRATEGY_MAPPING[strategy_name]()

    def sort(
        self, colors_to_sort: List[Color], direction: Directions
    ) -> Tuple[Color, ...]:
        """Sort a list of colors

        Args:
            colors_to_sort (List[Color]): the colors to be sorted

        Returns:
            Tuple[Color]: sorted set of colors
        """
        return {
            Directions.FORWARD: lambda: self.strategy.sort(colors_to_sort),
            Directions.BACKWARD: lambda: self._sort_backwards(colors_to_sort),
        }[direction]()

    def _sort_backwards(self, colors_to_sort: List[Color]) -> Tuple[Color, ...]:
        colors_sorted_backwards: List[Color] = []

        for color in reversed(self.strategy.sort(colors_to_sort)):
            colors_sorted_backwards.append(color)

        return tuple(colors_sorted_backwards)


class ColorWriter:
    """Service for writing colors to file"""

    def __init__(self, strategy: WritingStrategy):
        self._strategy = strategy

    def write(self, colors: Tuple[Color, ...], final_file_path: str):
        """Write colors to passed file

        Args:
            colors (Tuple[Color, ...]): colors to be written
            final_file_path (str): path to the file where the colors will be passed
        """

        self._strategy.write(colors, final_file_path)
