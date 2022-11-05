from abc import ABC, abstractmethod
from dataclasses import dataclass
from functools import reduce
from math import acos, ceil, log, sqrt
from typing import List, Tuple, Union

from harmony.models import RGB, Color


class ColorFormatConverter(ABC):
    """Interface for color format converters"""

    def convert(self, rgb: RGB) -> Tuple[float, ...]:
        """Converts RGB to other color format"""


@dataclass
class HSVHueData:
    """Store the data to calculate the hue for the HSV format"""

    red: float
    green: float
    blue: float
    biggest_value: float
    difference_between_biggest_and_smallest: float

    @property
    def difference_of_red_from_biggest_value(self):
        """Return the difference from red to the biggest value"""
        return abs(self.red - self.biggest_value)

    @property
    def difference_of_green_from_biggest_value(self):
        """Return the difference from red to the biggest value"""
        return abs(self.green - self.biggest_value)

    @property
    def difference_of_blue_from_biggest_value(self):
        """Return the difference from red to the biggest value"""
        return abs(self.blue - self.biggest_value)

    @property
    def differences_from_biggest_value(self):
        """Return the differences from the values to the biggest value"""
        return (
            self.difference_of_red_from_biggest_value,
            self.difference_of_green_from_biggest_value,
            self.difference_of_blue_from_biggest_value,
        )


class RGBtoHSVConverter(ColorFormatConverter):
    """Converter to convert RGB to HSV"""

    def convert(self, rgb: RGB) -> Tuple[float, ...]:
        """Converts a RGB object into a tuple with its corresponding HSV values

        Args:
            rgb (RGB): RGB to be converted

        Returns:
            Tuple[float, float, float]: the HSV values
        """
        red = rgb.red / 255
        green = rgb.green / 255
        blue = rgb.blue / 255

        biggest_value = max(red, green, blue)
        smallest_value = min(red, green, blue)

        difference_between_biggest_and_smallest = biggest_value - smallest_value

        if difference_between_biggest_and_smallest == 0:
            difference_between_biggest_and_smallest += 10 ** (-7)

        hue_data = HSVHueData(
            red, green, blue, biggest_value, difference_between_biggest_and_smallest
        )
        hue = self._calculate_hue(hue_data)
        saturation = self._calculate_saturation(
            biggest_value, difference_between_biggest_and_smallest
        )
        value = biggest_value

        return (hue, saturation, value)

    def _calculate_hue(self, data: HSVHueData) -> float:
        hue: float = -1

        maximum_difference = 10 ** (-7)

        calculation_methods = (
            lambda: self._calculate_case1(
                data.green, data.blue, data.difference_between_biggest_and_smallest
            ),
            lambda: self._calculate_case2(
                data.red, data.blue, data.difference_between_biggest_and_smallest
            ),
            lambda: self._calculate_case3(
                data.red, data.green, data.difference_between_biggest_and_smallest
            ),
        )

        are_the_biggest_value = [
            difference < maximum_difference
            for difference in data.differences_from_biggest_value
        ]
        index_of_biggest = are_the_biggest_value.index(True)

        calculate_hue = calculation_methods[index_of_biggest]
        hue = calculate_hue()

        hue *= 60
        return hue

    def _calculate_case1(
        self, green: float, blue: float, difference_between_biggest_and_smallest: float
    ) -> float:
        difference_between_green_and_blue = green - blue
        quotient_of_the_differences = (
            difference_between_green_and_blue / difference_between_biggest_and_smallest
        )

        return quotient_of_the_differences % 6

    def _calculate_case2(
        self, red: float, blue: float, difference_between_biggest_and_smallest: float
    ) -> float:
        difference_between_blue_and_red = blue - red
        quotient_of_the_differences = (
            difference_between_blue_and_red / difference_between_biggest_and_smallest
        )

        return quotient_of_the_differences + 2

    def _calculate_case3(
        self, red: float, green: float, difference_between_biggest_and_smallest: float
    ) -> float:
        difference_between_red_and_green = red - green
        quotient_of_the_differences = (
            difference_between_red_and_green / difference_between_biggest_and_smallest
        )

        return quotient_of_the_differences + 4

    def _calculate_saturation(
        self, biggest_value: float, difference_between_biggest_and_smallest: float
    ) -> float:
        difference_from_zero = abs(biggest_value - 0)
        maximum_difference = 10 ** (-7)
        is_maximum_zero = difference_from_zero < maximum_difference

        if not is_maximum_zero:
            return difference_between_biggest_and_smallest / biggest_value

        return 0.0


class RGBToLuminosityConverter(ColorFormatConverter):
    """Converter to convert RGB to perceived luminosity"""

    def convert(self, rgb: RGB) -> Tuple[float, ...]:
        red_factor = 0.241 * rgb.red
        green_factor = 0.691 * rgb.green
        blue_factor = 0.068 * rgb.blue

        return (sqrt(red_factor + green_factor + blue_factor),)


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
        colors_to_sort.sort(key=self._get_rgb_values)
        return tuple(colors_to_sort)

    def _get_rgb_values(self, color: Color) -> Tuple[int, int, int]:
        rgb = color.rgb

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

        colors_to_sort.sort(key=self._get_hsv_values)
        return tuple(colors_to_sort)

    def _get_hsv_values(self, color: Color):
        rgb = color.rgb
        converter = RGBtoHSVConverter()

        return converter.convert(rgb)


class HSLSorting(SortingStrategy):
    """Sorting strategy based on HSL"""

    def sort(self, colors_to_sort: List[Color]) -> Tuple[Color, ...]:
        """Sort a list of colors based on their HSL

        Args:
            colors_to_sort (List[Color]): the colors to be sorted

        Returns:
            Tuple[Color]: sorted set of colors
        """
        colors_to_sort.sort(key=self._get_hsl_values)
        return tuple(colors_to_sort)

    def _get_hsl_values(self, color: Color) -> Tuple[float, float, float]:
        rgb = color.rgb
        biggest_value = max(rgb.red, rgb.green, rgb.blue)
        smallest_value = min(rgb.red, rgb.green, rgb.blue)

        luminosity = self._calculate_luminosity(biggest_value, smallest_value)
        saturation = self._calculate_saturation(
            biggest_value, smallest_value, luminosity
        )
        hue = self._calculate_hue(rgb.red, rgb.green, rgb.blue)

        return (hue, saturation, luminosity)

    def _calculate_luminosity(self, biggest_value: int, smallest_value: int) -> float:
        sum_of_biggest_and_smallest = biggest_value + smallest_value

        return sum_of_biggest_and_smallest / 510

    def _calculate_saturation(
        self, biggest_value: int, smallest_value: int, luminosity: float
    ) -> float:
        if luminosity > 0:
            difference_between_biggest_and_smallest = biggest_value - smallest_value
            difference_divided_by_255 = difference_between_biggest_and_smallest / 255
            doubled_luminosity_value = 2 * luminosity
            doubled_luminosity_value_minus_1 = doubled_luminosity_value - 1
            absolute_doubled_luminosity_value_minus_1 = abs(
                doubled_luminosity_value_minus_1
            )
            one_minus_absolute_doubled_luminosity_value_minus_1 = (
                1 - absolute_doubled_luminosity_value_minus_1
            )

            if one_minus_absolute_doubled_luminosity_value_minus_1 == 0:
                one_minus_absolute_doubled_luminosity_value_minus_1 += 10 ** (-7)

            return (
                difference_divided_by_255
                / one_minus_absolute_doubled_luminosity_value_minus_1
            )

        return 0.0

    def _calculate_hue(self, red: int, green: int, blue: int) -> float:
        half_green = green / 2
        half_blue = blue / 2
        difference_from_ref_to_halfs = red - half_green - half_blue

        squared_root_of_perfect_square = self._calculate_squared_root_of_perfect_square(
            red, green, blue
        )

        cosine = difference_from_ref_to_halfs / squared_root_of_perfect_square
        angle = acos(cosine)

        if green >= blue:
            return angle

        full_circle_minus_angle = 360 - angle
        return full_circle_minus_angle

    def _calculate_squared_root_of_perfect_square(
        self, red: int, green: int, blue: int
    ) -> float:
        red_squared = red**2
        green_squared = green**2
        blue_squared = blue**2
        red_times_green = red * green
        red_times_blue = red * blue
        green_times_blue = green * blue
        perfect_square = (
            red_squared
            + green_squared
            + blue_squared
            - red_times_green
            - red_times_blue
            - green_times_blue
        )

        return sqrt(perfect_square)


class LuminositySorting(SortingStrategy):
    """Sorting strategy based on perceived luminosity"""

    def sort(self, colors_to_sort: List[Color]) -> Tuple[Color, ...]:
        """Sort a list of colors based on their perceived luminosity

        Args:
            colors_to_sort (List[Color]): the colors to be sorted

        Returns:
            Tuple[Color]: sorted set of colors
        """
        colors_to_sort.sort(key=self._get_luminosity)
        return tuple(colors_to_sort)

    def _get_luminosity(self, color: Color) -> float:
        rgb = color.rgb
        converter = RGBToLuminosityConverter()

        return converter.convert(rgb)[0]


class StepSorting(SortingStrategy):
    """Step sorting strategy"""

    def sort(self, colors_to_sort: List[Color]) -> Tuple[Color, ...]:
        """Sort a list of colors based on their HSL and luminosity but splitting them by
        steps

        Args:
            colors_to_sort (List[Color]): the colors to be sorted

        Returns:
            Tuple[Color]: sorted set of colors
        """
        colors_to_sort.sort(key=self._get_stepped_hsv_and_luminosity_values)
        return tuple(colors_to_sort)

    def _get_stepped_hsv_and_luminosity_values(
        self, color: Color
    ) -> Tuple[int, float, int]:
        steps = 8

        rgb = color.rgb
        to_hsv_converter = RGBtoHSVConverter()
        to_luminosity_converter = RGBToLuminosityConverter()

        hue, _, value = to_hsv_converter.convert(rgb)
        (luminosity,) = to_luminosity_converter.convert(rgb)

        hue_as_percentage = hue / 360
        stepped_hue = round(hue_as_percentage * steps)
        stepped_value = round(value * steps)

        return (stepped_hue, luminosity, stepped_value)


class AlternatedStepSorting(SortingStrategy):
    """Alternated step sorting strategy"""

    def sort(self, colors_to_sort: List[Color]) -> Tuple[Color, ...]:
        """Sort a list of colors based on their HSL and luminosity but splitting them by
        steps

        Args:
            colors_to_sort (List[Color]): the colors to be sorted

        Returns:
            Tuple[Color]: sorted set of colors
        """
        colors_to_sort.sort(
            key=self._get_stepped_alternatively_hsv_and_luminosity_values
        )
        return tuple(colors_to_sort)

    def _get_stepped_alternatively_hsv_and_luminosity_values(
        self, color: Color
    ) -> Tuple[int, float, int]:
        steps = 8

        rgb = color.rgb
        to_hsv_converter = RGBtoHSVConverter()
        to_luminosity_converter = RGBToLuminosityConverter()

        hue, _, value = to_hsv_converter.convert(rgb)
        (luminosity,) = to_luminosity_converter.convert(rgb)

        hue_as_percentage = hue / 360
        stepped_hue = round(hue_as_percentage * steps)
        stepped_value = round(value * steps)

        if stepped_hue % 2 == 1:
            stepped_value = steps - stepped_value
            luminosity = steps - luminosity

        return (stepped_hue, luminosity, stepped_value)


class HillbertSorting(SortingStrategy):
    """Hillbert Curve sorting strategy"""

    def sort(self, colors_to_sort: List[Color]) -> Tuple[Color, ...]:
        """Sort a list of colors using the Hillbert Curve algorithm

        Args:
            colors_to_sort (List[Color]): the colors to be sorted

        Returns:
            Tuple[Color]: sorted set of colors
        """
        colors_to_sort.sort(key=self._get_hillbert_index)
        return tuple(colors_to_sort)

    def _get_hillbert_index(self, color: Color):
        rgb = color.rgb
        x_coodinate = rgb.red * 255
        y_coordinate = rgb.green * 255
        z_coordinate = rgb.blue * 255

        return self._get_int_from_hillbert_coordinates(
            [x_coodinate, y_coordinate, z_coordinate]
        )

    def _get_int_from_hillbert_coordinates(
        self, coordinates: List[Union[int, float]]
    ) -> int:
        number_of_coodinates = len(coordinates)

        coordinate_chunks = self._unpack_coordinates(coordinates)
        number_of_chunks = len(coordinate_chunks)

        start, end = self._get_start_and_end_indices(
            number_of_chunks, number_of_coodinates
        )

        chunks = [0] * number_of_chunks
        mask: int = 2**number_of_coodinates - 1

        for chunk_index in range(number_of_chunks):
            gray_bit = self._get_gray_decoded(
                start, mask, coordinate_chunks[chunk_index]
            )
            chunks[chunk_index] = gray_bit
            start, end = self._get_child_start_and_end_indices(
                start, end, mask, gray_bit
            )

        return self._pack_index(chunks, number_of_coodinates)

    def _unpack_coordinates(self, coords: List[Union[int, float]]) -> List[int]:
        biggest_coordinates = reduce(max, coords)
        log_of_coordinates_on_base_2 = log(biggest_coordinates + 1, 2)
        rounded_log_of_coordinates_on_base_2 = ceil(log_of_coordinates_on_base_2)
        max_of_bits = max(1, rounded_log_of_coordinates_on_base_2)

        return self._transpose_bits(coords, max_of_bits)

    def _transpose_bits(
        self, coordinates: List[Union[int, float]], max_of_bits: int
    ) -> List[int]:
        coordinates = list(coordinates)
        number_of_coodinates = len(coordinates)
        chunks = [0] * max_of_bits

        for chunk_index in range(max_of_bits - 1, -1, -1):
            chunks[chunk_index] = self._get_chunk(number_of_coodinates, coordinates)

        return chunks

    def _get_chunk(
        self, number_of_coodinates: int, coordinates: List[Union[int, float]]
    ) -> int:
        chunk = 0

        for coordinate_index in range(number_of_coodinates):
            chunk = chunk * 2 + int(coordinates[coordinate_index] % 2)
            coordinates[coordinate_index] /= 2

        return int(chunk)

    def _get_start_and_end_indices(
        self, number_of_chunks: int, number_of_coordinates: int
    ) -> Tuple[int, int]:

        return 0, int(2 ** ((-number_of_chunks - 1) % number_of_coordinates))

    def _get_gray_decoded(self, start: int, mask: int, coordinate_chunk: int) -> int:
        modulus = mask + 1
        encoded_gray = int((coordinate_chunk ^ start) * (modulus / 2))
        return self._decode_gray((encoded_gray | int(encoded_gray / modulus)) & mask)

    def _decode_gray(self, gray_code: int) -> int:
        decoding_constant = 1
        while True:
            div = gray_code >> decoding_constant
            gray_code ^= div
            if div <= 1:
                return gray_code

            decoding_constant <<= 1

    def _get_child_start_and_end_indices(
        self, parent_start: int, parent_end: int, mask: int, i: int
    ) -> Tuple[int, int]:
        start_i = max(0, (i - 1) & ~1)
        end_i = min(mask, (i + 1) | 1)
        child_start = self._get_gray_encoded(parent_start, parent_end, mask, start_i)
        child_end = self._get_gray_encoded(parent_start, parent_end, mask, end_i)
        return child_start, child_end

    def _get_gray_encoded(self, start, end, mask, index) -> int:
        travel_bit: int = start ^ end
        modulus: int = mask + 1
        encoded_gray: int = int(self._encode_gray(index) * (travel_bit * 2))
        return ((encoded_gray | int(encoded_gray / modulus)) & mask) ^ start

    def _encode_gray(self, index):
        assert index >= 0
        assert isinstance(index, int)

        return index ^ int(index / 2)

    def _pack_index(self, chunks: List[int], number_of_coodinates: int):
        pack = 2**number_of_coodinates
        return reduce(lambda n, chunk: n * pack + chunk, chunks)
