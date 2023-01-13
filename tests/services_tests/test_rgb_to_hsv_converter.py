from typing import Tuple

from harmony.models import RGB
from harmony.service_layer.converters import RGBtoHSVConverter
from tests.helpers import assert_real_numbers_are_equal


class TestRGBtoHSLConverter:
    """Tests for the HSL to RGB converter"""

    def test_converting(self) -> None:
        """Test converting a valid RGB to HSL"""
        arrangement = self._given_rgb()
        result = self._when_converted(arrangement)
        self._then_should_get_hsl(result)

    def _given_rgb(self) -> RGB:
        red, green, blue = 255, 191, 0

        return RGB(red, green, blue)

    def _when_converted(self, arrangement: RGB) -> Tuple[float, float, float]:
        converter = RGBtoHSVConverter()

        return converter.convert(arrangement)[:3]

    def _then_should_get_hsl(self, result: Tuple[float, float, float]) -> None:
        expected_hue, expected_saturation, expected_value = 45.0, 1.0, 1.0
        actual_hue, actual_saturation, actual_value = result

        assert_real_numbers_are_equal(expected_hue, actual_hue, 0.1)
        assert_real_numbers_are_equal(expected_saturation, actual_saturation, 0.01)
        assert_real_numbers_are_equal(expected_value, actual_value, 0.01)
