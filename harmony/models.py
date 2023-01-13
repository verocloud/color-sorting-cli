from abc import ABC
from dataclasses import dataclass
from typing import Any, Dict, Tuple

from harmony import constants
from harmony.utils import convert_hexcode_from_3_to_6_chars_form


@dataclass
class RGB:
    """Model for the RGB format of color"""

    red: int
    green: int
    blue: int

    def __str__(self):
        return f"RGB({self.red}, {self.green}, {self.blue})"

    @classmethod
    def from_hexcode(cls, hexcode: str):
        """Make a RGB object from a hexcode string"""
        return cls(
            cls._get_red_from_hexcode(hexcode),
            cls._get_green_from_hexcode(hexcode),
            cls._get_blue_from_hexcode(hexcode),
        )

    @classmethod
    def _get_red_from_hexcode(cls, hexcode: str) -> int:
        return int(cls._clean_hexcode(hexcode)[:2], 16)

    @classmethod
    def _get_green_from_hexcode(cls, hexcode: str) -> int:
        return int(cls._clean_hexcode(hexcode)[2:4], 16)

    @classmethod
    def _get_blue_from_hexcode(cls, hexcode: str) -> int:
        return int(cls._clean_hexcode(hexcode)[4:], 16)

    @staticmethod
    def _clean_hexcode(hexcode) -> str:
        return convert_hexcode_from_3_to_6_chars_form(hexcode).replace("#", "")

    @property
    def red_as_percentage(self) -> float:
        """Return the red component as percentage"""
        return self.red / constants.MAXIMUM_RGB_VALUE

    @property
    def green_as_percentage(self) -> float:
        """Return the green component as percentage"""
        return self.green / constants.MAXIMUM_RGB_VALUE

    @property
    def blue_as_percentage(self) -> float:
        """Return the blue component as percentage"""
        return self.blue / constants.MAXIMUM_RGB_VALUE


@dataclass
class Color:
    """Model for the color"""

    rgb: RGB
    hexcode: str
    original_format: str
    description: str

    @property
    def rgb_red(self) -> int:
        """Return the value of red from the RGB of the color"""
        return self.rgb.red

    @property
    def rgb_green(self) -> int:
        """Return the value of green from the RGB of the color"""
        return self.rgb.green

    @property
    def rgb_blue(self) -> int:
        """Return the value of blue from the RGB of the color"""
        return self.rgb.blue


@dataclass
class HueData:
    """Store the data to calculate the hue for the HSV format"""

    red_as_percentage: float
    green_as_percentage: float
    blue_as_percentage: float

    @classmethod
    def from_rgb(cls, rgb: RGB) -> "HueData":
        """Make a HueData object from the data of a RGB object"""
        return cls(
            rgb.red_as_percentage, rgb.green_as_percentage, rgb.blue_as_percentage
        )

    @property
    def difference_between_biggest_and_smallest(self) -> float:
        """Return the difference between the biggest and the smallest values between the
        components"""
        return self.biggest_value - self._get_smallest_value()

    @property
    def biggest_value(self) -> float:
        """Return the biggest value between the components"""
        return max(
            self.red_as_percentage, self.green_as_percentage, self.blue_as_percentage
        )

    def _get_smallest_value(self) -> float:
        return min(
            self.red_as_percentage, self.green_as_percentage, self.blue_as_percentage
        )

    @property
    def difference_of_red_from_biggest_value(self):
        """Return the difference from red to the biggest value"""
        return abs(self.red_as_percentage - self.biggest_value)

    @property
    def difference_of_green_from_biggest_value(self):
        """Return the difference from red to the biggest value"""
        return abs(self.green_as_percentage - self.biggest_value)

    @property
    def difference_of_blue_from_biggest_value(self):
        """Return the difference from red to the biggest value"""
        return abs(self.blue_as_percentage - self.biggest_value)

    @property
    def differences_from_biggest_value(self):
        """Return the differences from the values to the biggest value"""
        return (
            self.difference_of_red_from_biggest_value,
            self.difference_of_green_from_biggest_value,
            self.difference_of_blue_from_biggest_value,
        )


@dataclass
class SaturationData:
    """Store the data needed to calculate the saturation data"""

    biggest_value: float
    difference_between_biggest_and_smallest: float

    @classmethod
    def from_hue_data(cls, hue_data: HueData) -> "SaturationData":
        """Make a SaturationData object from the data in a HueData object"""
        return cls(
            hue_data.biggest_value, hue_data.difference_between_biggest_and_smallest
        )

    @classmethod
    def from_rgb(cls, rgb: RGB) -> "SaturationData":
        """Make a SaturationData object from the data in a RGB object"""
        return cls.from_hue_data(HueData.from_rgb(rgb))


@dataclass
class HSL:
    """Store the data of the HSL of a color"""

    hue: int
    saturation: float
    luminosity: float


class DataModel(ABC):
    """Interface for the data table models"""


@dataclass
class ColorName(DataModel):
    """Store the data of the color name"""

    name: str
    hsl: HSL


@dataclass
class InsertQueryData:
    """Store the data needed to form a INSERT SQL query"""

    table_name: str
    data_to_insert: Dict[str, Any]

    @property
    def columns(self) -> Tuple[str, ...]:
        """Return the name of the columns related to the passed values"""
        return tuple(self.data_to_insert.keys())

    @property
    def values_to_insert(self) -> Tuple[Any, ...]:
        """Return the values passed for the new table registry"""
        return tuple(self.data_to_insert.values())
