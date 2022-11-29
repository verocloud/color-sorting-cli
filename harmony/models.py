from dataclasses import dataclass


@dataclass
class RGB:
    """Model for the RGB format of color"""

    red: int
    green: int
    blue: int

    def __str__(self):
        return f"RGB({self.red}, {self.green}, {self.blue})"


@dataclass
class Color:
    """Model for the color"""

    rgb: RGB
    hexcode: str
    original_format: str
    description: str
