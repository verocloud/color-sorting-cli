from abc import ABC, abstractmethod
from typing import List, Tuple

from harmony import constants
from harmony.models import RGB, Color, HueData
from harmony.service_layer.calculators import HillbertIndexCalculator
from harmony.service_layer.converters import (
    HueCalculator,
    RGBToHSLConverter,
    RGBtoHSVConverter,
    RGBToLuminosityConverter,
)
from harmony.utils import quotient_between


class SortingStrategy(ABC):
    """Interface for sorting strategies"""

    @abstractmethod
    def sort(self, colors_to_sort: List[Color]) -> Tuple[Color, ...]:
        """Sort a list of colors

        Args:
            colors_to_sort (List[Color]): the colors to be sorted

        Returns:
            Tuple[Color]: sorted set of colors
        """


class RGBSorting(SortingStrategy):
    """Sorting strategy based on RGB values"""

    def sort(self, colors_to_sort: List[Color]) -> Tuple[Color, ...]:
        """Sort a list of colors based on their RGB

        Args:
            colors_to_sort (List[Color]): the colors to be sorted

        Returns:
            Tuple[Color]: sorted set of colors
        """
        colors_to_sort.sort(key=lambda color: self._get_rgb_values(color.rgb))
        return tuple(colors_to_sort)

    def _get_rgb_values(self, rgb: RGB) -> Tuple[int, int, int]:
        return (rgb.red, rgb.green, rgb.blue)


class HSVSorting(SortingStrategy):
    """Sorting strategy based on HSV"""

    def sort(self, colors_to_sort: List[Color]) -> Tuple[Color, ...]:
        """Sort a list of colors based on their HSV

        Args:
            colors_to_sort (List[Color]): the colors to be sorted

        Returns:
            Tuple[Color]: sorted set of colors
        """
        RGBtoHSVConverter()

        colors_to_sort.sort(key=lambda color: self._get_hsv_values(color.rgb))
        return tuple(colors_to_sort)

    def _get_hsv_values(self, rgb: RGB):
        return RGBtoHSVConverter().convert(rgb)


class HSLSorting(SortingStrategy):
    """Sorting strategy based on HSL"""

    def sort(self, colors_to_sort: List[Color]) -> Tuple[Color, ...]:
        """Sort a list of colors based on their HSL

        Args:
            colors_to_sort (List[Color]): the colors to be sorted

        Returns:
            Tuple[Color]: sorted set of colors
        """
        colors_to_sort.sort(key=lambda color: self._get_hsl_values(color.rgb))
        return tuple(colors_to_sort)

    def _get_hsl_values(self, rgb: RGB) -> Tuple[float, ...]:
        return RGBToHSLConverter().convert(rgb)[:3]


class LuminositySorting(SortingStrategy):
    """Sorting strategy based on perceived luminosity"""

    def sort(self, colors_to_sort: List[Color]) -> Tuple[Color, ...]:
        """Sort a list of colors based on their perceived luminosity

        Args:
            colors_to_sort (List[Color]): the colors to be sorted

        Returns:
            Tuple[Color]: sorted set of colors
        """
        colors_to_sort.sort(key=lambda color: self._get_luminosity(color.rgb))
        return tuple(colors_to_sort)

    def _get_luminosity(self, rgb: RGB) -> float:
        return RGBToLuminosityConverter().convert(rgb)[0]


class StepSorting(SortingStrategy):
    """Step sorting strategy"""

    STEPS = 8

    def sort(self, colors_to_sort: List[Color]) -> Tuple[Color, ...]:
        """Sort a list of colors based on their HSL and luminosity but splitting them by
        steps

        Args:
            colors_to_sort (List[Color]): the colors to be sorted

        Returns:
            Tuple[Color]: sorted set of colors
        """
        colors_to_sort.sort(
            key=lambda color: self._get_stepped_hsv_and_luminosity_values(color.rgb)
        )
        return tuple(colors_to_sort)

    def _get_stepped_hsv_and_luminosity_values(self, rgb: RGB) -> Tuple[float, ...]:
        hue, _, value = RGBtoHSVConverter().convert(rgb)

        return (
            round(quotient_between(hue, constants.MAXIMUM_HUE_VALUE) * self.STEPS),
            *RGBToLuminosityConverter().convert(rgb),
            round(value * self.STEPS),
        )


class AlternatedStepSorting(SortingStrategy):
    """Alternated step sorting strategy"""

    STEPS = 8

    def sort(self, colors_to_sort: List[Color]) -> Tuple[Color, ...]:
        """Sort a list of colors based on their HSL and luminosity but splitting them by
        steps

        Args:
            colors_to_sort (List[Color]): the colors to be sorted

        Returns:
            Tuple[Color]: sorted set of colors
        """
        colors_to_sort.sort(
            key=lambda color: self._get_stepped_alternatively_hsv_and_luminosity_values(
                color.rgb
            )
        )
        return tuple(colors_to_sort)

    def _get_stepped_alternatively_hsv_and_luminosity_values(
        self, rgb: RGB
    ) -> Tuple[int, float, int]:
        (luminosity,) = RGBToLuminosityConverter().convert(rgb)
        stepped_value = self._get_stepped_value(rgb)

        if self._is_stepped_hue_odd(rgb):
            stepped_value = self.STEPS - stepped_value
            luminosity = self.STEPS - luminosity

        return (self._get_stepped_hue(rgb), luminosity, stepped_value)

    def _is_stepped_hue_odd(self, rgb: RGB) -> bool:
        return self._get_stepped_hue(rgb) % 2 == 1

    def _get_stepped_hue(self, rgb: RGB) -> int:
        return round(self._get_hue_as_decimal_times_steps(self._get_hue(rgb)))

    def _get_hue(self, rgb: RGB) -> float:
        return HueCalculator().calculate(HueData.from_rgb(rgb))

    def _get_hue_as_decimal_times_steps(self, hue) -> float:
        return quotient_between(hue, constants.MAXIMUM_HUE_VALUE) * self.STEPS

    def _get_stepped_value(self, rgb: RGB) -> int:
        return round(self._get_value_times_steps(rgb))

    def _get_value_times_steps(self, rgb: RGB) -> float:
        return RGBtoHSVConverter().calculate_value_from_rgb(rgb) * self.STEPS


class HillbertSorting(SortingStrategy):
    """Hillbert Curve sorting strategy"""

    def sort(self, colors_to_sort: List[Color]) -> Tuple[Color, ...]:
        """Sort a list of colors using the Hillbert Curve algorithm

        Args:
            colors_to_sort (List[Color]): the colors to be sorted

        Returns:
            Tuple[Color]: sorted set of colors
        """
        colors_to_sort.sort(key=lambda color: self._get_hillbert_index(color.rgb))
        return tuple(colors_to_sort)

    def _get_hillbert_index(self, rgb: RGB):
        return HillbertIndexCalculator().calculate(rgb)
