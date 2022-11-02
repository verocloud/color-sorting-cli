import os
import re
from functools import reduce
from math import ceil, log
from typing import Iterator, List, Tuple, Union

from harmony.constants import ColorFormat
from harmony.exceptions import InvalidColorException, InvalidFileException
from harmony.models import RGB, Color


def get_final_file_path(source_file_path: str) -> str:
    """Return the path to the file with the processed data

    Args:
        source_file_path (str): path to the original file

    Returns:
        str: path to the processed data file
    """
    index_of_extension = source_file_path.rfind(".")

    if index_of_extension >= 0:
        extension = source_file_path[index_of_extension:]
        return f"{source_file_path[:index_of_extension]}_sorted{extension}"

    return f"{source_file_path}_sorted"


class ColorExtractor:
    """Extractor of colors"""

    def extract_from_file(self, file_path: str) -> List[Color]:
        """Extracts a list of colors from a file

        Args:
            file_path (str): path to the file with the colors

        Returns:
            List[Color]: list of colors extracted
        """
        self._check_for_file_path(file_path)

        with open(file_path, "r", encoding="utf8") as colors_file:
            color_strings = colors_file.readlines()

        return [color for color in self._make_colors_list(color_strings)]

    def _check_for_file_path(self, path: str) -> None:
        if not os.path.exists(path):
            raise InvalidFileException(f"{path} does not exists")

    def _make_colors_list(self, color_strings: List[str]) -> Iterator[Color]:

        for color_string in color_strings:
            color_string = color_string.replace("\n", "")
            yield self._make_color_from_string(color_string)

    def _make_color_from_string(self, color_string: str) -> Color:
        hexcode_pattern = re.compile("^[#][a-zA-Z0-9]{3}([a-zA-Z0-9]{3})?")
        rgb_pattern = re.compile(
            "^[(][0-2]?[0-9]{1,2}[,][\\s]?[0-2]?[0-9]{1,2}[,][\\s]?[0-2]?[0-9]{1,2}[)]"
        )

        if hexcode_pattern.match(color_string):
            return self._make_color_from_hexcode(color_string)

        elif rgb_pattern.match(color_string):
            return self._make_color_from_rgb(color_string)

        raise InvalidColorException(f"{color_string} does not match any valid format")

    def _make_color_from_hexcode(self, hexcode: str) -> Color:
        index_of_whitespace = hexcode.index(" ")
        index_after_whitespace = index_of_whitespace + 1
        description = hexcode[index_after_whitespace:]
        description = description.strip()

        hexcode = hexcode[:index_of_whitespace]

        have_six_digits = len(hexcode) == 7

        if not have_six_digits:
            hexcode = hexcode + hexcode[1:]

        red = int(hexcode[1:3], 16)
        green = int(hexcode[5:], 16)
        blue = int(hexcode[3:5], 16)
        rgb = RGB(red=red, green=green, blue=blue)

        hexcode = hexcode.lower()

        return Color(
            rgb=rgb,
            hexcode=hexcode,
            original_format=ColorFormat.HEXCODE,
            description=description,
        )

    def _make_color_from_rgb(self, rgb_string: str) -> Color:
        index_after_closing_parenthesis = rgb_string.index(")") + 1

        description = rgb_string[index_after_closing_parenthesis:]
        description = description.strip()

        rgb_string = rgb_string[:index_after_closing_parenthesis].replace(" ", "")
        rgb_string = rgb_string.replace("(", "")
        rgb_string = rgb_string.replace(")", "")

        red_string, green_string, blue_string = rgb_string.split(",")

        red = int(red_string)
        green = int(green_string)
        blue = int(blue_string)
        rgb = RGB(red=red, green=green, blue=blue)

        hexcode = ("#{:X}{:X}{:X}").format(rgb.red, rgb.green, rgb.blue)
        hexcode = hexcode.lower()

        return Color(
            rgb=rgb,
            hexcode=hexcode,
            original_format=ColorFormat.RGB,
            description=description,
        )


class ColorSorter:
    """Service for sorting colors"""

    def sort(self, colors_to_sort: List[Color]) -> Tuple[Color, ...]:
        """Sorts a list of colors

        Args:
            colors_to_sort (List[Color]): the colors to be sorted

        Returns:
            Tuple[Color]: sorted set of colors
        """
        colors_to_sort.sort(key=self._get_hillbert_index)
        return tuple(colors_to_sort)

    def _get_hillbert_index(self, color: Color):
        """Return the hillbert index for the color RGB"""
        rgb = color.rgb
        x = rgb.red * 255
        y = rgb.green * 255
        z = rgb.blue * 255

        return self._get_int_from_hillbert_coordinates([x, y, z])

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
                start, end, mask, coordinate_chunks[chunk_index]
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
        coordinates = list(coordinates)  # Make a copy we can modify safely.
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
            doubled_chunk = chunk * 2
            modulus_from_halfed_coordinate: int = round(
                coordinates[coordinate_index] % 2
            )
            chunk = doubled_chunk + modulus_from_halfed_coordinate
            coordinates[coordinate_index] /= 2

        return round(chunk)

    def _get_start_and_end_indices(
        self, number_of_chunks: int, number_of_coordinates: int
    ) -> Tuple[int, int]:

        return 0, round(2 ** ((-number_of_chunks - 1) % number_of_coordinates))

    def _get_gray_decoded(
        self, start: int, end: int, mask: int, coordinate_chunk: int
    ) -> int:
        modulus = mask + 1
        rg = round((coordinate_chunk ^ start) * (modulus / 2))
        return self._decode_gray((rg | round(rg / modulus)) & mask)

    def _decode_gray(self, n: int) -> int:
        sh = 1
        while True:
            div = n >> sh
            n ^= div
            if div <= 1:
                return n

            sh <<= 1

    def _get_child_start_and_end_indices(
        self, parent_start: int, parent_end: int, mask: int, i: int
    ) -> Tuple[int, int]:
        start_i = max(0, (i - 1) & ~1)
        end_i = min(mask, (i + 1) | 1)
        child_start = self._get_gray_encoded(parent_start, parent_end, mask, start_i)
        child_end = self._get_gray_encoded(parent_start, parent_end, mask, end_i)
        return child_start, child_end

    def _get_gray_encoded(self, start, end, mask, i) -> int:
        travel_bit: int = start ^ end
        modulus: int = mask + 1
        g: int = round(self._encode_gray(i) * (travel_bit * 2))
        return ((g | round(g / modulus)) & mask) ^ start

    def _encode_gray(self, bn):
        assert bn >= 0
        assert type(bn) == int

        return bn ^ round(bn / 2)

    def _pack_index(self, chunks, nD):
        p = 2**nD  # Turn digits mod 2**nD back into a single number:
        return reduce(lambda n, chunk: n * p + chunk, chunks)
