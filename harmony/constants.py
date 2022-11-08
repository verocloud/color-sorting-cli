from enum import Enum


class ColorFormat(str, Enum):
    """Contants for the color formats"""

    SAME_AS_INPUT: str = "input"
    RGB: str = "rgb"
    HEXCODE: str = "hexcode"


class SortingStrategyName(str, Enum):
    """Constants for the sorting strategies"""

    RGB: str = "rgb"
    HSV: str = "hsv"
    HSL: str = "hsl"
    LUMINOSITY: str = "luminosity"
    STEP: str = "step"
    ALTERNATED_STEP: str = "step-alternated"
    HILLBERT: str = "hillbert"
