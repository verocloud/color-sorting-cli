from typing import List, Tuple

from harmony.constants import ColorFormat
from harmony.models import RGB, Color
from harmony.services import ColorSorter


class TestColorSorter:
    """Test for the color sorting service"""

    def test_sorting(self) -> None:
        """Test sorting colors"""
        arrangement = self._given_colors()
        result = self._when_sorter_is_called(arrangement)
        self._then_should_sort(result)

    def _given_colors(self) -> List[Color]:
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

        return [color1, color2, color3]

    def _when_sorter_is_called(self, arrangement: List[Color]) -> Tuple[Color]:
        sorter = ColorSorter()

        return sorter.sort(arrangement)

    def _then_should_sort(self, result: Tuple[Color]) -> None:
        expected_first_color = Color(
            rgb=RGB(75, 214, 47),
            hexcode="#4bd62f",
            original_format=ColorFormat.RGB,
            description="green",
        )
        actual_first_color = result[0]

        expected_second_color = Color(
            rgb=RGB(212, 104, 4),
            hexcode="#d46804",
            original_format=ColorFormat.HEXCODE,
            description="orange",
        )
        actual_second_color = result[1]

        assert expected_first_color == actual_first_color
        assert expected_second_color == actual_second_color
