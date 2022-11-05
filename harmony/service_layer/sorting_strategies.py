from abc import ABC, abstractmethod
from functools import reduce
from math import acos, ceil, log, sqrt
from typing import List, Tuple, Union

from harmony.models import Color


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
        """Sort a list of colors based on their RGB value

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


class HSLSorting(SortingStrategy):
    """Sorting strategy based on HSL"""

    def sort(self, colors_to_sort: List[Color]) -> Tuple[Color, ...]:
        """Sort a list of colors based on their HSL value

        Args:
            colors_to_sort (List[Color]): the colors to be sorted

        Returns:
            Tuple[Color]: sorted set of colors
        """
        colors_to_sort.sort(key=self._get_hsl_values)
        return tuple(colors_to_sort)

    def _get_hsl_values(self, color: Color) -> Tuple[int, int, int]:
        rgb = color.rgb
        biggest_value = max(rgb.red, rgb.green, rgb.blue)
        smallest_value = min(rgb.red, rgb.green, rgb.blue)

        luminosity = self._calculate_luminosity(biggest_value, smallest_value)
        saturation = self._calculate_saturation(
            biggest_value, smallest_value, luminosity
        )
        hue = self._calculate_hue(rgb.red, rgb.green, rgb.blue)

        return (hue, saturation, luminosity)

    def _calculate_luminosity(self, biggest_value: int, smallest_value: int) -> int:
        sum_of_biggest_and_smallest = biggest_value + smallest_value

        return round(sum_of_biggest_and_smallest / 510)

    def _calculate_saturation(
        self, biggest_value: int, smallest_value: int, luminosity: float
    ) -> int:
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

            return round(
                difference_divided_by_255
                / one_minus_absolute_doubled_luminosity_value_minus_1
            )

        return 0

    def _calculate_hue(self, red: int, green: int, blue: int) -> int:
        half_green = green / 2
        half_blue = blue / 2
        difference_from_ref_to_halfs = red - half_green - half_blue

        squared_root_of_perfect_square = self._calculate_squared_root_of_perfect_square(
            red, green, blue
        )

        cosine = difference_from_ref_to_halfs / squared_root_of_perfect_square
        angle = acos(cosine)

        if green >= blue:
            return round(angle)

        full_circle_minus_angle = 360 - angle
        return round(full_circle_minus_angle)

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
