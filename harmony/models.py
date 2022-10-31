from dataclasses import dataclass


@dataclass
class RGB:
    """Model for the RGB format of color"""

    red: int
    blue: int
    green: int


@dataclass
class Color:
    """Model for the color"""

    rgb: RGB
    hexcode: str
