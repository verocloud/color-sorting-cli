import logging
from functools import reduce
from math import ceil, log
from typing import List, Tuple, Union

from harmony.models import RGB, HueData, SaturationData
from harmony.utils import are_almost_equal, difference_between, quotient_between


class HueCalculator:
    """Provide method calculating the hue"""

    def __init__(self):
        self._logger = logging.getLogger(self.__class__.__name__)

    def calculate(self, data: HueData) -> float:
        """Calculate the hue for a color from the data passed

        Args:
            data (HueData): data to calculate hue

        Returns:
            float: hue value
        """
        if are_almost_equal(data.difference_between_biggest_and_smallest, 0):
            self._logger.info(  # pylint: disable=logging-not-lazy
                "Hue is zero because the difference between the biggest and the "
                + "smallest is zero"
            )
            return 0

        return self._calculate_hue(data) * 60

    def _calculate_hue(self, data: HueData) -> float:
        return (
            lambda: self._calculate_case1(data),
            lambda: self._calculate_case2(data),
            lambda: self._calculate_case3(data),
        )[self._get_index_of_the_biggest_value(data)]()

    def _get_index_of_the_biggest_value(self, data: HueData) -> int:
        return [
            are_almost_equal(difference, 0)
            for difference in data.differences_from_biggest_value
        ].index(True)

    def _calculate_case1(self, data: HueData) -> float:
        self._logger.info("Calculating case 1, cause red value is the biggest")

        return (
            quotient_between(
                difference_between(data.green_as_percentage, data.blue_as_percentage),
                data.difference_between_biggest_and_smallest,
            )
            % 6
        )

    def _calculate_case2(self, data: HueData) -> float:
        self._logger.info("Calculating case 2, cause green value is the biggest")

        return (
            quotient_between(
                difference_between(data.blue_as_percentage, data.red_as_percentage),
                data.difference_between_biggest_and_smallest,
            )
            + 2
        )

    def _calculate_case3(self, data: HueData) -> float:
        self._logger.info("Calculating case 3, cause blue value is the biggest")

        return (
            quotient_between(
                difference_between(data.red_as_percentage, data.green_as_percentage),
                data.difference_between_biggest_and_smallest,
            )
            + 4
        )


class SaturationCalculator:
    """Provide method for calculating the color saturation"""

    def calculate(self, data: SaturationData) -> float:
        """Calculate the saturation value for a color

        Args:
            data (SaturationData): data to calculate saturation

        Returns:
            float: saturation value
        """
        if not are_almost_equal(data.biggest_value, 0):
            return data.difference_between_biggest_and_smallest / data.biggest_value

        return 0.0


class HillbertIndexCalculator:
    """Provide method for calculating the hillbert index of the color"""

    # pylint: disable=too-many-locals,too-many-arguments

    def calculate(self, rgb: RGB) -> int:
        """Calculate the Hillbert Curve index for the color passed

        Args:
            rgb (RGB): RGB data for the color to calculate

        Returns:
            int: Hillbert Curve index
        """

        x_coodinate = rgb.red * 255
        y_coordinate = rgb.green * 255
        z_coordinate = rgb.blue * 255

        return self._get_int_from_hillbert_coordinates(
            [x_coodinate, y_coordinate, z_coordinate]
        )

    def _get_int_from_hillbert_coordinates(
        self, coordinates: List[Union[int, float]]
    ) -> int:
        coordinate_chunks = self._unpack_coordinates(coordinates)

        start, end = self._get_start_and_end_indices(
            len(coordinate_chunks), len(coordinates)
        )

        chunks = [0] * len(coordinate_chunks)
        mask: int = 2 ** len(coordinates) - 1

        for chunk_index, current_chunk in enumerate(coordinate_chunks):
            gray_bit = self._get_gray_decoded(start, mask, current_chunk)
            chunks[chunk_index] = gray_bit
            start, end = self._get_child_start_and_end_indices(
                start, end, mask, gray_bit
            )

        return self._pack_index(chunks, len(coordinates))

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
