from abc import ABC, abstractmethod
from plistlib import InvalidFileException
from typing import List, Tuple

from harmony.constants import MAXIMUM_RGB_VALUE, ColorFormat
from harmony.models import RGB, Color
from harmony.utils import convert_hexcode_from_3_to_6_chars_form


class ReadingStrategy(ABC):
    """Interface for a object resposible for converting a string to a Color object"""

    @abstractmethod
    def read(self, raw_string) -> Color:
        """Convert a raw string containing the data of the color to a Color object"""


class HexcodeReading(ReadingStrategy):
    """Convert a raw string the with a hexcode string into a Color object"""

    def read(self, raw_string) -> Color:
        description = ""

        if self._there_is_whitespace_in(raw_string):
            raw_string, description = self._split_hexcode_and_description(raw_string)

        return Color(
            rgb=RGB.from_hexcode(raw_string),
            hexcode=convert_hexcode_from_3_to_6_chars_form(raw_string).lower(),
            original_format=ColorFormat.HEXCODE,
            description=description,
        )

    def _split_hexcode_and_description(
        self, hexcode_and_description: str
    ) -> Tuple[str, str]:
        return (
            self._get_hexcode_from_hexcode_and_description(hexcode_and_description),
            self._get_description_from_hexcode_and_description(hexcode_and_description),
        )

    def _get_hexcode_from_hexcode_and_description(
        self, hexcode_and_description: str
    ) -> str:
        return hexcode_and_description[
            : self._get_hexcode_and_description_split_index(hexcode_and_description)
        ]

    def _get_description_from_hexcode_and_description(
        self, hexcode_and_description: str
    ) -> str:
        return hexcode_and_description[
            self._get_description_start_index(hexcode_and_description) :
        ].strip()

    def _there_is_whitespace_in(self, string_to_verify: str) -> bool:
        return self._get_hexcode_and_description_split_index(string_to_verify) > 0

    def _get_description_start_index(self, hexcode_and_description: str) -> int:
        return (
            self._get_hexcode_and_description_split_index(hexcode_and_description) + 1
        )

    @staticmethod
    def _get_hexcode_and_description_split_index(hexcode_and_description: str) -> int:
        return hexcode_and_description.find(" ")


class RGBReading(ReadingStrategy):
    """Convert a raw string the with RGB components into a Color object"""

    def read(self, raw_string) -> Color:
        for amount in self._get_components_from_rgb_and_description(raw_string):
            self._check_rgb_amount(amount)

        return Color(
            rgb=self._get_rgb_from_rgb_and_description(raw_string),
            hexcode=self._get_and_clean_hexcode_from_rgb_and_description(raw_string),
            original_format=ColorFormat.RGB,
            description=self._get_description_from_rgb_and_description(raw_string),
        )

    def _get_red_from_rgb_and_description(self, rgb_and_description: str) -> int:
        return self._get_components_from_rgb_and_description(rgb_and_description)[0]

    def _get_and_clean_rgb_from_rgb_and_description(
        self, rgb_and_description: str
    ) -> str:
        return self._remove_whitespaces_and_parenthesis_from(
            self._get_rgb_string_from_rgb_and_description(rgb_and_description)
        )

    def _get_rgb_string_from_rgb_and_description(self, rgb_and_description: str) -> str:
        return rgb_and_description[
            : self._get_rgb_and_description_split_index(rgb_and_description)
        ]

    @staticmethod
    def _remove_whitespaces_and_parenthesis_from(string_to_clean: str) -> str:
        return string_to_clean.replace(" ", "").replace("(", "").replace(")", "")

    def _get_description_from_rgb_and_description(
        self, rgb_and_description: str
    ) -> str:
        return rgb_and_description[
            self._get_description_start_index(rgb_and_description) :
        ].strip()

    def _get_description_start_index(self, rgb_and_description: str) -> int:
        return self._get_rgb_and_description_split_index(rgb_and_description) + 1

    @staticmethod
    def _get_rgb_and_description_split_index(rgb_and_description: str) -> int:
        return rgb_and_description.index(")")

    def _get_and_clean_hexcode_from_rgb_and_description(
        self, rgb_and_description: str
    ) -> str:
        return (
            "#"
            + self._get_hexcode_from_rgb_and_description(rgb_and_description).lower()
        )

    def _get_hexcode_from_rgb_and_description(self, rgb_and_description: str) -> str:
        return self._get_hexcode_from_rgb(
            self._get_rgb_from_rgb_and_description(rgb_and_description)
        )

    def _get_rgb_from_rgb_and_description(self, rgb_and_description: str) -> RGB:
        # pylint: disable=no-value-for-parameter
        return RGB(*self._get_components_from_rgb_and_description(rgb_and_description))

    def _get_components_from_rgb_and_description(
        self, rgb_and_description: str
    ) -> Tuple[int, ...]:
        components: List[int] = []

        for component in self._get_and_clean_rgb_from_rgb_and_description(
            rgb_and_description
        ).split(","):
            components.append(int(component))

        return tuple(components)

    @staticmethod
    def _get_hexcode_from_rgb(rgb: RGB) -> str:
        return f"{int(rgb.red):02x}{int(rgb.green):02x}{int(rgb.blue):02x}"

    def _check_rgb_amount(self, amount: int) -> None:
        """Raise exception if amount not between 0 and 255"""
        if self._is_amount_not_between_zero_and_255(amount):
            raise InvalidFileException(
                "The amount of red, green and blue needs to be between 0 and 255, "
                + f"{amount} is invalid"
            )

    def _is_amount_not_between_zero_and_255(self, amount: int) -> bool:
        return not (
            self._is_amount_greater_or_equal_to_zero(amount)
            and self._is_amount_less_than_maximum_rgb_value(amount)
        )

    @staticmethod
    def _is_amount_greater_or_equal_to_zero(amount: int) -> bool:
        return amount >= 0

    @staticmethod
    def _is_amount_less_than_maximum_rgb_value(amount: int) -> bool:
        return amount <= MAXIMUM_RGB_VALUE
