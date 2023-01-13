import logging
from typing import Any, Dict, Tuple

from harmony.constants import ByteOrder
from harmony.models import RGB, Color
from harmony.service_layer.writting_strategies import WritingStrategy
from harmony.utils import float_to_bytes


class ASEWriting(WritingStrategy):
    """Writting strategy that results into an ".ase" file"""

    EXTENSION = "ase"

    FLOAT_BYTE_ORDER = ByteOrder.BIG

    def __init__(self, palette_name: str) -> None:
        self.palette_name = palette_name
        self._logger = logging.getLogger(self.__class__.__name__)

    def write(self, colors: Tuple[Color, ...], final_file_path: str):
        """Write colors to a ".ase" file

        Args:
            colors (Tuple[Color, ...]): colors to be written
            final_file_path (str): path to the file where the colors will be passed
        """
        with open(final_file_path, "wb") as colors_file:
            colors_file.write(self._get_file_content(colors))

    def _get_file_content(self, colors: Tuple[Color, ...]) -> bytes:
        file_content = self._get_file_head_bytes(colors)
        file_content.extend(self._get_palette_name_chunk())
        file_content.extend(self._get_color_bytes(colors))
        file_content.extend(self._get_final_chunk())

        return file_content

    def _get_file_head_bytes(self, colors: Tuple[Color, ...]) -> bytearray:
        return self._get_file_head(self._get_amount_of_ase_chunks(colors))

    @staticmethod
    def _get_amount_of_ase_chunks(colors: Tuple[Color, ...]) -> int:
        # The amount of ASE chunks is equal to the sum of the number of colors + one
        return len(colors) + 2

    @staticmethod
    def _get_final_chunk() -> bytes:
        return b"\xc0\x02\x00\x00\x00\x00"

    def _get_file_head(self, amount_of_ase_chunks: int) -> bytearray:
        file_head = bytearray(self._get_file_signature())
        file_head.extend(self._get_version_bytes())
        file_head.extend(self._get_ase_chunk_count_bytes(amount_of_ase_chunks))

        return file_head

    @staticmethod
    def _get_file_signature() -> bytes:
        return b"\x41\x53\x45\x46"

    @staticmethod
    def _get_version_bytes() -> bytes:
        return b"\x00\x01\x00\x00"

    @staticmethod
    def _get_ase_chunk_count_bytes(amount_of_ase_chunks) -> bytes:
        return amount_of_ase_chunks.to_bytes(4, "big")

    def _get_palette_name_chunk(self) -> bytearray:
        # chunk for the palette name + the final chunk
        palette_name_chunk = bytearray(b"\xc0\x01\x00\x00")
        palette_name_chunk.extend(self._get_palette_name_chunk_size_bytes())
        palette_name_chunk.extend(self._get_palette_name_chunk_count_bytes())
        palette_name_chunk.extend(self._get_palette_name_as_bytes())

        return palette_name_chunk

    def _get_palette_name_chunk_size_bytes(self) -> bytes:
        return len(self._get_palette_name_as_bytes()).to_bytes(2, "big")

    def _get_palette_name_chunk_count_bytes(self) -> bytes:
        return self._get_palette_name_chunk_count(
            self._get_palette_name_as_bytes()
        ).to_bytes(2, "big")

    def _get_palette_name_as_bytes(self) -> bytearray:
        palette_name_as_bytes = bytearray(
            bytes(self.palette_name, encoding="utf_16_be")
        )
        palette_name_as_bytes.extend(b"\x00\x00")

        return palette_name_as_bytes

    @staticmethod
    def _get_palette_name_chunk_count(palette_name: bytes) -> int:
        return int(len(palette_name) / 2)

    def _get_color_bytes(self, colors: Tuple[Color, ...]) -> bytearray:
        color_bytes = bytearray()

        for color in colors:
            color_bytes.extend(b"\x00\x01\x00\x00")

            self._logger.info(
                self._get_description_converted_log_message(),
                self._get_description_converted_log_data(color),
            )

            self._log_rgb_converted(color, self._convert_rgb_to_bytes(color.rgb))

            color_bytes.extend(self._get_color_chunk_size_bytes(color))
            color_bytes.extend(self._get_description_bytes(color.description))
            color_bytes.extend(self._convert_rgb_to_bytes(color.rgb))

        return color_bytes

    @staticmethod
    def _get_description_converted_log_message() -> str:
        return (
            'Color description "%(description)s" converted to '
            + "%(description_bytes)s"
        )

    def _get_description_converted_log_data(self, color: Color) -> Dict[str, Any]:
        return {
            "description": color.description,
            "description_bytes": self._get_description_bytes(color.description),
        }

    def _log_rgb_converted(self, color: Color, rgb_bytes: bytes) -> None:
        self._logger.info(
            "RGB components %(rgb)s converted to %(rgb_bytes)s",
            self._get_rgb_converted_log_data(color, rgb_bytes),
        )

    def _get_rgb_converted_log_data(
        self, color: Color, rgb_bytes: bytes
    ) -> Dict[str, Any]:
        return {
            "rgb": str(color.rgb),
            "rgb_bytes": rgb_bytes,
        }

    def _get_color_chunk_size_bytes(self, color: Color) -> bytes:
        return self._get_color_chunk_size(color).to_bytes(2, "big")

    def _get_color_chunk_size(self, color: Color) -> int:
        return self._get_description_bytes_length(
            color.description
        ) + self._get_rgb_as_bytes_length(color.rgb)

    def _get_description_bytes_length(self, description: str) -> int:
        return len(self._get_description_bytes(description))

    def _get_rgb_as_bytes_length(self, rgb: RGB) -> int:
        return len(self._convert_rgb_to_bytes(rgb))

    def _get_description_bytes(self, description: str) -> bytearray:
        description_bytes = bytearray(
            self._get_color_description_count_bytes(description)
        )
        description_bytes.extend(self._get_description_array(description))

        return description_bytes

    def _get_color_description_count_bytes(self, description: str) -> bytes:
        return self._get_color_description_count(description).to_bytes(2, "big")

    def _get_color_description_count(self, description: str) -> int:
        return int(self._get_description_array_length(description) / 2)

    def _get_description_array_length(self, description: str) -> int:
        return len(self._get_description_array(description))

    @staticmethod
    def _get_description_array(description: str) -> bytearray:
        description_as_bytes = bytearray(bytes(description, encoding="utf_16_be"))
        description_as_bytes.extend(b"\x00\x00\x00\x00")

        return description_as_bytes

    def _convert_rgb_to_bytes(self, rgb: RGB) -> bytearray:
        rgb_bytes = bytearray(b"RGB\x20")
        rgb_bytes.extend(float_to_bytes(rgb.red_as_percentage, self.FLOAT_BYTE_ORDER))
        rgb_bytes.extend(float_to_bytes(rgb.green_as_percentage, self.FLOAT_BYTE_ORDER))
        rgb_bytes.extend(float_to_bytes(rgb.blue_as_percentage, self.FLOAT_BYTE_ORDER))

        rgb_bytes.extend(b"\x00\x02")

        return rgb_bytes
