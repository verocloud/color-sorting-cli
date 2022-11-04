import os
from typing import Tuple

from harmony.constants import ColorFormat
from harmony.models import RGB, Color
from harmony.service_layer.services import ColorWriter
from tests.helpers import get_temporary_file_path


class TestColorsWriter:
    """Tests for the colors writer"""

    def test_write_colors_as_rgb(self) -> None:
        """Test writing colors to file"""
        arrangement = self._given_colors()
        result = self._when_colors_are_passed_writing_as_rgb(arrangement)
        self._then_should_write_to_new_file_as_rgb(result)

    def _when_colors_are_passed_writing_as_rgb(self, arrangement: Tuple[Color]) -> str:
        temporary_file = get_temporary_file_path()
        writer = ColorWriter(ColorFormat.RGB)

        writer.write_colors_to_file(arrangement, temporary_file)

        colors_file_content: str

        with open(temporary_file, "r", encoding="utf8") as colors_file:
            colors_file_content = colors_file.read()

        os.remove(temporary_file)

        return colors_file_content

    def _then_should_write_to_new_file_as_rgb(self, result: str) -> None:
        expected_color_string = "(75, 214, 47)"
        unexpected_color_string = "#4bd62f"

        assert expected_color_string in result
        assert unexpected_color_string not in result

    def test_write_colors_as_hexcode(self) -> None:
        """Test writing colors to file"""
        arrangement = self._given_colors()
        result = self._when_colors_are_passed_writing_as_hexcode(arrangement)
        self._then_should_write_to_new_file_as_hexcode(result)

    def _when_colors_are_passed_writing_as_hexcode(
        self, arrangement: Tuple[Color]
    ) -> str:
        temporary_file = get_temporary_file_path()
        writer = ColorWriter(ColorFormat.HEXCODE)

        writer.write_colors_to_file(arrangement, temporary_file)

        colors_file_content: str

        with open(temporary_file, "r", encoding="utf8") as colors_file:
            colors_file_content = colors_file.read()

        os.remove(temporary_file)

        return colors_file_content

    def _then_should_write_to_new_file_as_hexcode(self, result: str) -> None:
        expected_color_string = "#4bd62f"
        unexpected_color_string = "(75, 214, 47)"

        assert expected_color_string in result
        assert unexpected_color_string not in result

    def test_write_colors_as_same_as_input(self) -> None:
        """Test writing colors to file"""
        arrangement = self._given_colors()
        result = self._when_colors_are_passed_writing_as_same_as_input(arrangement)
        self._then_should_write_to_new_file_as_same_as_input(result)

    def _when_colors_are_passed_writing_as_same_as_input(
        self, arrangement: Tuple[Color]
    ) -> str:
        temporary_file = get_temporary_file_path()
        writer = ColorWriter(ColorFormat.SAME_AS_INPUT)

        writer.write_colors_to_file(arrangement, temporary_file)

        colors_file_content: str

        with open(temporary_file, "r", encoding="utf8") as colors_file:
            colors_file_content = colors_file.read()

        os.remove(temporary_file)

        return colors_file_content

    def _then_should_write_to_new_file_as_same_as_input(self, result: str) -> None:
        expected_color_string1 = "#eb3d34"
        unexpected_color_string1 = "(235, 61, 52)"

        expected_color_string2 = "(75, 214, 47)"
        unexpected_color_string2 = "#4bd62f"

        assert expected_color_string1 in result
        assert unexpected_color_string1 not in result

        assert expected_color_string2 in result
        assert unexpected_color_string2 not in result

    def _given_colors(self) -> Tuple[Color]:
        rgb1 = RGB(235, 61, 52)
        hexcode1 = "#eb3d34"
        color1 = Color(
            rgb=rgb1,
            hexcode=hexcode1,
            original_format=ColorFormat.HEXCODE,
            description="red",
        )

        rgb2 = RGB(75, 214, 47)
        hexcode2 = "#4bd62f"
        color2 = Color(
            rgb=rgb2,
            hexcode=hexcode2,
            original_format=ColorFormat.RGB,
            description="green",
        )

        rgb3 = RGB(212, 104, 4)
        hexcode3 = "#d46804"
        color3 = Color(
            rgb=rgb3,
            hexcode=hexcode3,
            original_format=ColorFormat.HEXCODE,
            description="orange",
        )

        return (color1, color2, color3)