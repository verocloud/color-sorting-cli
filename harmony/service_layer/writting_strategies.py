import logging
from abc import ABC, abstractmethod
from typing import List, Tuple

from harmony.constants import ByteOrder, ColorFormat
from harmony.exceptions import InvalidCLRFileException
from harmony.models import RGB, Color
from harmony.utils import float_to_bytes


class WritingStrategy(ABC):
    """Interface for output file writting strategies"""

    EXTENSION = ""

    @abstractmethod
    def write(self, colors: Tuple[Color, ...], final_file_path: str):
        """Write the sorted colors to a new file

        Args:
            colors (Tuple[Color, ...]): colors to written
            final_file_path (str): path to the new file
        """


class DefaultWriting(WritingStrategy):
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


class ASEWriting(WritingStrategy):
    """Writting strategy that results into an ".ase" file"""

    EXTENSION = "ase"

    FLOAT_BYTE_ORDER = ByteOrder.BIG

    def __init__(self, palette_name: str) -> None:
        self.palette_name = palette_name
        current_class = self.__class__
        self._logger = logging.getLogger(current_class.__name__)

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
            description_convertion_log_data = {
                "description": color.description,
                "description_bytes": description_bytes,
            }
            description_convertion_log_message = (
                'Color description "%(description)s" converted to '
                + "%(description_bytes)s"
            )
            self._logger.info(
                description_convertion_log_message, description_convertion_log_data
            )

            rgb_bytes = self._convert_rgb_to_bytes(color.rgb)

            rgb_convertion_log_data = {
                "rgb": str(color.rgb),
                "rgb_bytes": rgb_bytes,
            }
            self._logger.info(
                "RGB components %(rgb)s converted to %(rgb_bytes)s",
                rgb_convertion_log_data,
            )

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
        red_bytes = float_to_bytes(red_percentage, self.FLOAT_BYTE_ORDER)
        rgb_bytes.extend(red_bytes)

        green_percentage = rgb.green / 255
        green_bytes = float_to_bytes(green_percentage, self.FLOAT_BYTE_ORDER)
        rgb_bytes.extend(green_bytes)

        blue_percentage = rgb.blue / 255
        blue_bytes = float_to_bytes(blue_percentage, self.FLOAT_BYTE_ORDER)
        rgb_bytes.extend(blue_bytes)

        rgb_bytes.extend(b"\x00\x02")

        return rgb_bytes


class CLRWriting(WritingStrategy):
    """Writting strategy that results into an ".clr" file"""

    EXTENSION = "clr"

    CLASS_DECLARATION_BYTES = b"\x84\x84\x84"
    INHERITANCE_DECLARATION_BYTES = b"\x84\x84"
    NULL_BYTE = b"\x00"
    FLOAT_BYTE = b"\x83"
    INTEGER_16_BYTE = b"\x81"
    END_OF_DATA_BYTE = b"\x86"
    BYTE_ORDER = ByteOrder.LITTLE
    MAX_DIFFERENCE_FOR_COMPARING_FLOATS = 10 ^ (-3)

    def __init__(self) -> None:
        current_class = self.__class__
        self._logger = logging.getLogger(current_class.__name__)

    def write(self, colors: Tuple[Color, ...], final_file_path: str):
        """Write colors to a ".clr" file

        Args:
            colors (Tuple[Color, ...]): colors to be written
            final_file_path (str): path to the file where the colors will be passed

        Raises:
            InvalidCLRFileException: when a CLR file is tried to be written with less
            then 1 color
        """
        file_content = bytearray()
        file_start = self._get_file_start()

        color_count = len(colors)
        color_count_chunk = self._get_color_count_chunk(color_count)

        colors_list = list(colors)
        first_color = colors_list.pop(0)

        first_color_bytes = self._get_first_color_bytes(first_color)
        colors_bytes = self._get_colors_bytes(colors_list)

        bytes_to_add_to_the_file = (
            file_start,
            color_count_chunk,
            first_color_bytes,
            colors_bytes,
        )

        for item in bytes_to_add_to_the_file:
            file_content.extend(item)

        with open(final_file_path, "wb") as final_file:
            final_file.write(file_content)

    def _get_file_start(self) -> bytearray:
        file_start_bytes = bytearray()
        signature_bytes = b"\x04\x0bstreamtyped"
        start_of_file_bytes = b"\x81\xe8\x03\x84\x01\x69\x01"

        file_start_bytes.extend(signature_bytes)
        file_start_bytes.extend(start_of_file_bytes)

        return file_start_bytes

    def _get_color_count_chunk(self, color_count: int) -> bytearray:
        is_color_count_valid = color_count > 0

        if is_color_count_valid:
            color_chunk = bytearray()

            colors_count_chunk_bytes = b"\x84\x02\x40\x69\x85"
            colors_count_byte = self._get_color_count_bytes(color_count)

            color_chunk.extend(colors_count_chunk_bytes)
            color_chunk.extend(colors_count_byte)

            return color_chunk

        raise InvalidCLRFileException(
            f"CLR files must have at least one color, {color_count} was passed"
        )

    def _get_color_count_bytes(self, color_count: int) -> bytearray:
        if color_count <= 127:
            color_count_byte_case_one_byte = color_count.to_bytes(1, "little")
            return bytearray(color_count_byte_case_one_byte)

        color_count_bytes = color_count.to_bytes(2, "little")

        color_count_data_bytes = bytearray()
        color_count_data_bytes.extend(self.INTEGER_16_BYTE)
        color_count_data_bytes.extend(color_count_bytes)

        return color_count_data_bytes

    def _declare_map_value_type(self) -> bytearray:
        map_value_type_bytes = bytearray()

        nscolor_class_declaration_bytes = self._declare_class(b"NSColor")

        nsobject_class_name_bytes = b"NSObject"
        nsobject_class_name_count = len(nsobject_class_name_bytes)
        nsobject_class_name_count_byte = nsobject_class_name_count.to_bytes(1, "little")

        map_value_type_bytes.extend(nscolor_class_declaration_bytes)
        map_value_type_bytes.extend(self.NULL_BYTE)

        map_value_type_bytes.extend(self.INHERITANCE_DECLARATION_BYTES)
        map_value_type_bytes.extend(nsobject_class_name_count_byte)
        map_value_type_bytes.extend(nsobject_class_name_bytes)
        map_value_type_bytes.extend(self.NULL_BYTE)

        return map_value_type_bytes

    def _declare_map_keys_type(self) -> bytearray:
        return self._declare_class(b"NSString")

    def _declare_class(self, class_name: bytes) -> bytearray:
        class_declaration_bytes = bytearray()

        class_name_count = len(class_name)
        class_name_count_byte = class_name_count.to_bytes(1, "little")

        class_declaration_bytes.extend(self.CLASS_DECLARATION_BYTES)
        class_declaration_bytes.extend(class_name_count_byte)
        class_declaration_bytes.extend(class_name)

        return class_declaration_bytes

    def _get_first_color_bytes(self, first_color: Color) -> bytearray:
        first_color_bytes = bytearray()

        new_color_map_bytes = b"\x84\x02\x40\x40"
        map_values_type = self._declare_map_value_type()
        map_keys_type = self._declare_map_keys_type()

        colors_components_chunk_bytes = b"\x85\x84\x01\x63\x01\x84\x04\x66\x66\x66\x66"
        first_color_rgb = first_color.rgb
        first_color_rgb_bytes = self._convert_rgb_to_bytes(first_color_rgb)

        colors_names_chunk_bytes = b"\x01\x94\x84\x01\x2b"
        first_color_name = first_color.description
        first_color_name_bytes = self._convert_color_name_to_bytes(first_color_name)

        first_color_bytes.extend(new_color_map_bytes)
        first_color_bytes.extend(map_values_type)
        first_color_bytes.extend(colors_components_chunk_bytes)
        first_color_bytes.extend(first_color_rgb_bytes)
        first_color_bytes.extend(map_keys_type)
        first_color_bytes.extend(colors_names_chunk_bytes)
        first_color_bytes.extend(first_color_name_bytes)

        return first_color_bytes

    def _get_colors_bytes(self, colors: List[Color]) -> bytearray:
        colors_chunk_bytes = bytearray()

        for color in colors:
            rgb = color.rgb
            name = color.description

            components_bytes = self._convert_rgb_to_bytes(rgb)
            name_bytes = self._convert_color_name_to_bytes(name)

            colors_chunk_bytes.extend(b"\x94\x84\x93\x97\x01\x98")
            colors_chunk_bytes.extend(components_bytes)
            colors_chunk_bytes.extend(b"\x84\x96\x9a")
            colors_chunk_bytes.extend(name_bytes)

        return colors_chunk_bytes

    def _convert_rgb_to_bytes(self, rgb: RGB) -> bytearray:
        rgba_bytes = bytearray()

        red_as_decimal = rgb.red / 255
        green_as_decimal = rgb.green / 255
        blue_as_decimal = rgb.blue / 255

        red_bytes = self._get_color_component_bytes(red_as_decimal)
        green_bytes = self._get_color_component_bytes(green_as_decimal)
        blue_bytes = self._get_color_component_bytes(blue_as_decimal)
        alpha_bytes = (1).to_bytes(1, "little")

        rgba_bytes.extend(red_bytes)
        rgba_bytes.extend(green_bytes)
        rgba_bytes.extend(blue_bytes)
        rgba_bytes.extend(alpha_bytes)
        rgba_bytes.extend(self.END_OF_DATA_BYTE)

        rgb_conversion_log_data = {
            "rgb": str(rgb),
            "rgba_bytes": rgba_bytes,
        }
        self._logger.info(
            "RGB components %(rgb)s converted to %(rgba_bytes)s",
            rgb_conversion_log_data,
        )

        return rgba_bytes

    def _get_color_component_bytes(self, component_as_decimal: float) -> bytearray:
        difference_from_one = abs(1 - component_as_decimal)
        is_equal_to_one = difference_from_one < self.MAX_DIFFERENCE_FOR_COMPARING_FLOATS

        if is_equal_to_one:
            component_bytes = bytearray(b"\x01")
            return component_bytes

        return self._calculate_color_component_if_not_one(component_as_decimal)

    def _calculate_color_component_if_not_one(
        self, component_as_decimal: float
    ) -> bytearray:
        is_equal_to_zero = (
            component_as_decimal < self.MAX_DIFFERENCE_FOR_COMPARING_FLOATS
        )

        if is_equal_to_zero:
            return bytearray(b"\x00")

        component_value_bytes = float_to_bytes(component_as_decimal, self.BYTE_ORDER)

        component_bytes = bytearray(self.FLOAT_BYTE)
        component_bytes.extend(component_value_bytes)

        return component_bytes

    def _convert_color_name_to_bytes(self, name: str) -> bytearray:
        color_name_chunk_bytes = bytearray()

        color_name_bytes = bytes(name, encoding="utf8")
        color_name_count = len(color_name_bytes)

        if color_name_count > 255:
            color_name_bytes = color_name_bytes[:256]
            color_name_count = 255

        color_name_count_byte = color_name_count.to_bytes(1, "little")

        color_name_chunk_bytes.extend(color_name_count_byte)
        color_name_chunk_bytes.extend(color_name_bytes)
        color_name_chunk_bytes.extend(self.END_OF_DATA_BYTE)

        return color_name_chunk_bytes
