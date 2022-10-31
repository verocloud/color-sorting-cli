import os
import pytest
from typing import Callable, List
from harmony.exceptions import InvalidFileException
from harmony.models import RGB, Color
from harmony.services import ColorExtractor
from tests.helpers import get_temporary_file_path


class TestColorsExtractor:
    """Tests for the extractor of colors from the file"""

    def test_extract_from_file(self):
        """Test extracting the colors from a valid file"""
        arrangements = self._given_file_path()
        result = self._when_file_is_passed(arrangements)
        self._then_should_extract_colors(result)

        os.remove(arrangements)

    def _given_file_path(self) -> str:
        temporary_file_path = get_temporary_file_path()

        with open(temporary_file_path, "w", encoding="utf8") as colors_file:
            colors_file.write("#165cc4\n" + "196, 22, 190")

        return temporary_file_path

    def _then_should_extract_colors(self, colors: List[Color]) -> None:
        expected_rgb_for_the_first_color = RGB(red=22, blue=92, green=196)
        actual_rgb_for_the_first_color = colors[0].rgb

        expected_hexcode_for_the_second_color = "#c416be"
        actual_hexcode_for_the_second_color = colors[1].hexcode

        assert expected_rgb_for_the_first_color == actual_rgb_for_the_first_color
        assert (
            expected_hexcode_for_the_second_color == actual_hexcode_for_the_second_color
        )

    def test_extracting_colors_from_invalid_file(self):
        """Test extracting colors from invalid file"""

        def result():
            self._when_file_is_passed("not-a-file")

        self._then_should_raise_invalid_file(result)

    def _when_file_is_passed(self, file_path: str) -> List[Color]:
        extractor = ColorExtractor()
        return extractor.extract_from_file(file_path)

    def _then_should_raise_invalid_file(self, result: Callable[[], None]) -> None:
        with pytest.raises(Exception):
            result()
