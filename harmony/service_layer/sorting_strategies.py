from abc import ABC, abstractmethod
from functools import reduce
from math import ceil, log
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


class HillbertSorting(SortingStrategy):
    """Hillbert Curve sorting strategy"""

    def sort(self, colors_to_sort: List[Color]) -> Tuple[Color, ...]:
        """Sorts a list of colors using the Hillbert Curve algorithm

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
