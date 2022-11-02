from dataclasses import dataclass


@dataclass
class RGB:
    """Model for the RGB format of color"""

    red: int
    green: int
    blue: int


@dataclass
class Color:
    """Model for the color"""

    rgb: RGB
    hexcode: str
    original_format: str
    description: str
