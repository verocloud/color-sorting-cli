from harmony.models import RGB, HueData
from harmony.service_layer.converters import HueCalculator
from tests.helpers import assert_real_numbers_are_equal


class TestHueCalculator:
    """Tests for the Hue calculator"""

    def test_calculate(self) -> None:
        """Test calculating hue"""
        arrangement = self._given_hue_data()
        result = self._when_calculated(arrangement)
        self._then_should_get_hue(result)

    def _given_hue_data(self) -> HueData:
        return HueData.from_rgb(RGB(5, 0, 165))

    def _when_calculated(self, arrangement: HueData) -> float:
        calculator = HueCalculator()

        return calculator.calculate(arrangement)

    def _then_should_get_hue(self, result: float) -> None:
        expected_hue = 242.0

        assert_real_numbers_are_equal(expected_hue, result, tolerance=0.2)
