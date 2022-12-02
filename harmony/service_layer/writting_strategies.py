from abc import ABC, abstractmethod
from typing import Tuple

from harmony.constants import ColorFormat
from harmony.models import RGB, Color
from harmony.utils import float_to_bytes


class WrittingStrategy(ABC):
    """Interface for output file writting strategies"""

    @abstractmethod
    def write(self, colors: Tuple[Color, ...], final_file_path: str):
        """Write the sorted colors to a new file

        Args:
            colors (Tuple[Color, ...]): colors to written
            final_file_path (str): path to the new file
        """


class DefaultWritting(WrittingStrategy):
    """Writting strategy that results in a simple text file"""

    def __init__(self, color_format):
        color_string_getter_dict = {
            ColorFormat.HEXCODE: self._get_hexcode_string,
            ColorFormat.RGB: self._get_rgb_string,
            ColorFormat.SAME_AS_INPUT: self._get_color_as_input_format,
        }

        self._get_color_string = color_string_getter_dict[color_format]

    def write(self, colors: Tuple[Color, ...], final_file_path: str):
        """Write colors to a text file

        Args:
            colors (Tuple[Color, ...]): colors to be written
            final_file_path (str): path to the file where the colors will be passed
        """

        file_content: str = ""

        for color in colors:
            file_content += self._get_color_string(color)

        with open(final_file_path, "w", encoding="utf8") as final_file:
            final_file.write(file_content)

    def _get_color_as_input_format(self, color: Color) -> str:
        is_input_format_as_hexcode = color.original_format == ColorFormat.HEXCODE

        if is_input_format_as_hexcode:
            return self._get_hexcode_string(color)

        return self._get_rgb_string(color)

    def _get_hexcode_string(self, color: Color) -> str:
        return f"{color.hexcode} {color.description}\n"

    def _get_rgb_string(self, color: Color) -> str:
        rgb = color.rgb
        return f"({rgb.red}, {rgb.green}, {rgb.blue}) {color.description}\n"


class ASEWritting(WrittingStrategy):
    """Writting strategy that results into an ".ase" file"""

    def __init__(self, palette_name: str) -> None:
        self.palette_name = palette_name

    def write(self, colors: Tuple[Color, ...], final_file_path: str):
        """Write colors to a ".ase" file

        Args:
            colors (Tuple[Color, ...]): colors to be written
            final_file_path (str): path to the file where the colors will be passed
        """
        # The amount of ASE chunks is equal to the sum of the number of colors + one
        # chunk for the palette name + the final chunk
        amount_of_ase_chunks = len(colors) + 2
        file_head_bytes = self._get_file_head(amount_of_ase_chunks)
        file_content = file_head_bytes

        palette_name_chunk = self._get_palette_name_chunk()
        file_content.extend(palette_name_chunk)

        color_bytes = self._get_color_bytes(colors)
        file_content.extend(color_bytes)

        final_chunk = b"\xc0\x02\x00\x00\x00\x00"
        file_content.extend(final_chunk)

        with open(final_file_path, "wb") as colors_file:
            colors_file.write(file_content)

    def _get_file_head(self, amount_of_ase_chunks: int) -> bytearray:
        file_signature = b"\x41\x53\x45\x46"
        file_head = bytearray(file_signature)

        version_bytes = b"\x00\x01\x00\x00"
        file_head.extend(version_bytes)

        ase_chunk_count_bytes = amount_of_ase_chunks.to_bytes(4, "big")
        file_head.extend(ase_chunk_count_bytes)

        return file_head

    def _get_palette_name_chunk(self) -> bytearray:
        palette_name_chunk = bytearray(b"\xc0\x01\x00\x00")
        palette_name = bytearray(bytes(self.palette_name, encoding="utf_16_be"))
        palette_name.extend(b"\x00\x00")

        palette_name_chunk_size = len(palette_name)
        palette_name_chunk_size_bytes = palette_name_chunk_size.to_bytes(2, "big")
        palette_name_chunk.extend(palette_name_chunk_size_bytes)

        palette_name_chunk_count = int(len(palette_name) / 2)
        palette_name_chunk_count_bytes = palette_name_chunk_count.to_bytes(2, "big")
        palette_name_chunk.extend(palette_name_chunk_count_bytes)

        palette_name_chunk.extend(palette_name)

        return palette_name_chunk

    def _get_color_bytes(self, colors: Tuple[Color, ...]) -> bytearray:
        color_bytes = bytearray()

        for color in colors:
            color_bytes.extend(b"\x00\x01\x00\x00")

            description_bytes = self._get_description_bytes(color.description)
            rgb_bytes = self._convert_rgb_to_bytes(color.rgb)

            color_chunk_size = len(description_bytes) + len(rgb_bytes)
            color_chunk_size_bytes = color_chunk_size.to_bytes(2, "big")

            color_bytes.extend(color_chunk_size_bytes)
            color_bytes.extend(description_bytes)
            color_bytes.extend(rgb_bytes)

        return color_bytes

    def _get_description_bytes(self, description: str) -> bytearray:
        description_bytes = bytearray()

        description_array = bytearray(bytes(description, encoding="utf_16_be"))
        description_array.extend(b"\x00\x00\x00\x00")

        color_description_count = int(len(description_array) / 2)
        color_description_count_bytes = color_description_count.to_bytes(2, "big")
        description_bytes.extend(color_description_count_bytes)

        description_bytes.extend(description_array)

        return description_bytes

    def _convert_rgb_to_bytes(self, rgb: RGB) -> bytearray:
        rgb_bytes = bytearray(b"RGB\x20")

        red_percentage = rgb.red / 255
        red_bytes = float_to_bytes(red_percentage)
        rgb_bytes.extend(red_bytes)

        green_percentage = rgb.green / 255
        green_bytes = float_to_bytes(green_percentage)
        rgb_bytes.extend(green_bytes)

        blue_percentage = rgb.blue / 255
        blue_bytes = float_to_bytes(blue_percentage)
        rgb_bytes.extend(blue_bytes)

        rgb_bytes.extend(b"\x00\x02")

        return rgb_bytes
