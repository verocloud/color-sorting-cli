import logging
from plistlib import InvalidFileException
from typing import Any, Dict, List, Tuple

from harmony.constants import (
    MAXIMUM_8_BIT_INTEGER_VALUE,
    ByteOrder,
    FloatComparisonTolerance,
)
from harmony.models import RGB, Color
from harmony.service_layer.writting_strategies import WritingStrategy
from harmony.utils import are_almost_equal, float_to_bytes


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

    def __init__(self) -> None:
        self._logger = logging.getLogger(self.__class__.__name__)

    def write(self, colors: Tuple[Color, ...], final_file_path: str):
        """Write colors to a ".clr" file

        Args:
            colors (Tuple[Color, ...]): colors to be written
            final_file_path (str): path to the file where the colors will be passed

        Raises:
            InvalidCLRFileException: when a CLR file is tried to be written with less
            then 1 color
        """
        with open(final_file_path, "wb") as final_file:
            final_file.write(self._get_file_content(colors))

    def _get_file_content(self, colors: Tuple[Color, ...]) -> bytes:
        file_content = bytearray()

        for item in self._get_bytes_to_add_to_the_file(colors):
            file_content.extend(item)

        return file_content

    def _get_bytes_to_add_to_the_file(
        self, colors: Tuple[Color, ...]
    ) -> Tuple[bytes, ...]:
        colors_list = list(colors)
        first_color_bytes = self._get_first_color_bytes(colors_list.pop(0))

        return (
            self._get_file_start(),
            self._get_color_count_chunk_from_collection(colors),
            first_color_bytes,
            self._get_colors_bytes(colors_list),
        )

    def _get_color_count_chunk_from_collection(
        self, colors: Tuple[Color, ...]
    ) -> bytes:
        return self._get_color_count_chunk(len(colors))

    def _get_file_start(self) -> bytearray:
        file_start_bytes = bytearray(self._get_signature_bytes())
        file_start_bytes.extend(self._get_start_of_file_bytes())

        return file_start_bytes

    @staticmethod
    def _get_signature_bytes() -> bytes:
        return b"\x04\x0bstreamtyped"

    @staticmethod
    def _get_start_of_file_bytes() -> bytes:
        return b"\x81\xe8\x03\x84\x01\x69\x01"

    def _get_color_count_chunk(self, color_count: int) -> bytearray:
        if self._is_color_count_valid(color_count):
            color_chunk = bytearray(self._get_colors_count_chunk_bytes())
            color_chunk.extend(self._get_color_count_bytes(color_count))

            return color_chunk

        raise InvalidFileException(
            f"CLR files must have at least one color, but {color_count} was passed"
        )

    @staticmethod
    def _is_color_count_valid(color_count: int) -> bool:
        return color_count > 0

    @staticmethod
    def _get_colors_count_chunk_bytes() -> bytes:
        return b"\x84\x02\x40\x69\x85"

    def _get_color_count_bytes(self, color_count: int) -> bytearray:
        if color_count <= 127:
            return bytearray(color_count.to_bytes(1, "little"))

        color_count_data_bytes = bytearray(self.INTEGER_16_BYTE)
        color_count_data_bytes.extend(color_count.to_bytes(2, "little"))

        return color_count_data_bytes

    def _declare_map_value_type(self) -> bytearray:
        map_value_type_bytes = bytearray(self._declare_class(b"NSColor"))
        map_value_type_bytes.extend(self.NULL_BYTE)
        map_value_type_bytes.extend(self.INHERITANCE_DECLARATION_BYTES)
        map_value_type_bytes.extend(
            self._get_nsobject_class_name_count().to_bytes(1, "little")
        )
        map_value_type_bytes.extend(self._get_nsobject_class_name_bytes())
        map_value_type_bytes.extend(self.NULL_BYTE)

        return map_value_type_bytes

    def _get_nsobject_class_name_count(self) -> int:
        return len(self._get_nsobject_class_name_bytes())

    @staticmethod
    def _get_nsobject_class_name_bytes() -> bytes:
        return b"NSObject"

    def _declare_map_keys_type(self) -> bytearray:
        return self._declare_class(b"NSString")

    def _declare_class(self, class_name: bytes) -> bytearray:
        class_declaration_bytes = bytearray(self.CLASS_DECLARATION_BYTES)
        class_declaration_bytes.extend(len(class_name).to_bytes(1, "little"))
        class_declaration_bytes.extend(class_name)

        return class_declaration_bytes

    def _get_first_color_bytes(self, first_color: Color) -> bytearray:
        first_color_bytes = bytearray(self._get_new_color_map_bytes())
        first_color_bytes.extend(self._declare_map_value_type())
        first_color_bytes.extend(self._get_colors_components_chunk_bytes())
        first_color_bytes.extend(self._convert_rgb_to_bytes(first_color.rgb))
        first_color_bytes.extend(self._declare_map_keys_type())
        first_color_bytes.extend(self._get_colors_names_chunk_bytes())
        first_color_bytes.extend(
            self._convert_color_name_to_bytes(first_color.description)
        )

        return first_color_bytes

    @staticmethod
    def _get_new_color_map_bytes() -> bytes:
        return b"\x84\x02\x40\x40"

    @staticmethod
    def _get_colors_components_chunk_bytes() -> bytes:
        return b"\x85\x84\x01\x63\x01\x84\x04\x66\x66\x66\x66"

    @staticmethod
    def _get_colors_names_chunk_bytes() -> bytes:
        return b"\x01\x94\x84\x01\x2b"

    def _get_colors_bytes(self, colors: List[Color]) -> bytearray:
        colors_chunk_bytes = bytearray()

        for color in colors:
            colors_chunk_bytes.extend(b"\x94\x84\x93\x97\x01\x98")
            colors_chunk_bytes.extend(self._convert_rgb_to_bytes(color.rgb))
            colors_chunk_bytes.extend(b"\x84\x96\x9a")
            colors_chunk_bytes.extend(
                self._convert_color_name_to_bytes(color.description)
            )

        return colors_chunk_bytes

    def _convert_rgb_to_bytes(self, rgb: RGB) -> bytearray:
        rgba_bytes = bytearray(self._get_color_component_bytes(rgb.red_as_percentage))
        rgba_bytes.extend(self._get_color_component_bytes(rgb.green_as_percentage))
        rgba_bytes.extend(self._get_color_component_bytes(rgb.blue_as_percentage))
        rgba_bytes.extend(self._get_alpha_bytes())
        rgba_bytes.extend(self.END_OF_DATA_BYTE)

        self._logger.info(
            "RGB components %(rgb)s converted to %(rgba_bytes)s",
            self._get_rgb_converted_log_data(rgb, rgba_bytes),
        )

        return rgba_bytes

    @staticmethod
    def _get_rgb_converted_log_data(rgb: RGB, rgba_bytes: bytes) -> Dict[str, Any]:
        return {
            "rgb": str(rgb),
            "rgba_bytes": rgba_bytes,
        }

    @staticmethod
    def _get_alpha_bytes() -> bytes:
        return (1).to_bytes(1, "little")

    def _get_color_component_bytes(self, component_as_decimal: float) -> bytes:
        if self._is_component_as_decimal_near_one(component_as_decimal):
            return (1).to_bytes(1, "little")

        return self._calculate_color_component_if_not_one(component_as_decimal)

    @staticmethod
    def _is_component_as_decimal_near_one(component_as_decimal) -> bool:
        return are_almost_equal(
            component_as_decimal,
            1,
            tolerance=FloatComparisonTolerance.THREE_DECIMAL_PLACES,
        )

    def _calculate_color_component_if_not_one(
        self, component_as_decimal: float
    ) -> bytes:
        if self._is_color_component_near_zero(component_as_decimal):
            return (0).to_bytes(1, "little")

        component_bytes = bytearray(self.FLOAT_BYTE)
        component_bytes.extend(float_to_bytes(component_as_decimal, self.BYTE_ORDER))

        return component_bytes

    @staticmethod
    def _is_color_component_near_zero(component_as_decimal: float) -> bool:
        return are_almost_equal(
            component_as_decimal, 0, FloatComparisonTolerance.THREE_DECIMAL_PLACES
        )

    def _convert_color_name_to_bytes(self, name: str) -> bytearray:
        color_name_bytes = bytes(name, encoding="utf8")

        if len(bytes(name, encoding="utf8")) > MAXIMUM_8_BIT_INTEGER_VALUE:
            color_name_bytes = color_name_bytes[: self._get_last_char_allowed_index()]

        color_name_chunk_bytes = bytearray(len(color_name_bytes).to_bytes(1, "little"))
        color_name_chunk_bytes.extend(color_name_bytes)
        color_name_chunk_bytes.extend(self.END_OF_DATA_BYTE)

        return color_name_chunk_bytes

    @staticmethod
    def _get_last_char_allowed_index() -> int:
        return MAXIMUM_8_BIT_INTEGER_VALUE + 1
