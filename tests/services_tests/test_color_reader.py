import os
from typing import Callable, List

import pytest

from harmony.exceptions import InvalidColorException
from harmony.models import RGB, Color
from harmony.service_layer.services import ColorReader
from tests.helpers import get_temporary_file_path


class TestColorReader:
    """Tests for the reader of color files"""

    def test_extract_from_file(self) -> None:
        """Test extracting the colors from a valid file"""
        arrangements = self._given_file_path()

        try:
            result = self._when_file_is_passed(arrangements)
            self._then_should_extract_colors(result)

        finally:
            os.remove(arrangements)

    def _given_file_path(self) -> str:
        temporary_file_path = get_temporary_file_path()

        with open(temporary_file_path, "w", encoding="utf8") as colors_file:
            colors_file.write("#165cc4 Blue\n" + "(196, 22, 190) Magenta")

        return temporary_file_path

    def _then_should_extract_colors(self, colors: List[Color]) -> None:
        expected_rgb_for_the_first_color = RGB(red=22, green=92, blue=196)
        actual_rgb_for_the_first_color = colors[0].rgb

        expected_hexcode_for_the_second_color = "#c416be"
        actual_hexcode_for_the_second_color = colors[1].hexcode

        expected_description_for_first_color = "Blue"
        actual_description_for_first_color = colors[0].description

        expected_description_for_second_color = "Magenta"
        actual_description_for_second_color = colors[1].description

        assert expected_rgb_for_the_first_color == actual_rgb_for_the_first_color
        assert (
            expected_hexcode_for_the_second_color == actual_hexcode_for_the_second_color
        )
        assert (
            expected_description_for_first_color == actual_description_for_first_color
        )
        assert (
            expected_description_for_second_color == actual_description_for_second_color
        )

    def test_extracting_colors_from_invalid_format(self) -> None:
        arrangements = self._given_file_with_invalid_formats()

        try:

            def results() -> None:
                self._when_file_is_passed(arrangements)

            self._then_should_raise_invalid_color(results)

        finally:
            os.remove(arrangements)

    def _given_file_with_invalid_formats(self) -> str:
        temporary_file_path = get_temporary_file_path()

        with open(temporary_file_path, "w", encoding="utf8") as colors_file:
            colors_file.write("adasdkajlsdka\n" + "djaisdljaksa")

        return temporary_file_path

    def _when_file_is_passed(self, file_path: str) -> List[Color]:
        extractor = ColorReader()
        with open(file_path) as file:
            return extractor.extract_from_file(file)

    def _then_should_raise_invalid_color(self, result: Callable[[], None]):
        with pytest.raises(InvalidColorException):
            result()

    def test_extract_from_file_without_color_names(self) -> None:
        """Test generating names for the colors in a file"""
        arrangement = self._given_file_without_color_names()
        result = self._when_file_is_passed(arrangement)
        self._then_should_give_names_to_colors(result)

    def _given_file_without_color_names(self) -> str:
        temporary_file_path = get_temporary_file_path()

        with open(temporary_file_path, "w", encoding="utf8") as colors_file:
            colors_file.write("(255, 0, 0)\n" + "#0500A5\n" + "(219, 0, 76)")

        return temporary_file_path

    def _then_should_give_names_to_colors(self, result: List[Color]) -> None:
        expected_color_names = ["Red", "New Midnight Blue", "Razzmatazz"]
        actual_color_names = [color.description for color in result]

        for expected_name in expected_color_names:
            assert expected_name in actual_color_names
