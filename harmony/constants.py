import uuid
from enum import Enum


class DefaultParameters(str, Enum):
    """Constants for the default subjective parameters"""

    PALETTE_NAME: str = f"Palette {uuid.uuid4()} sorted by Harmony"


class ColorFormat(str, Enum):
    """Constants for the color formats"""

    SAME_AS_INPUT: str = "input"
    RGB: str = "rgb"
    HEXCODE: str = "hexcode"


class Directions(str, Enum):
    """Constants for the direction of the sorting"""

    FORWARD: str = "forward"
    BACKWARD: str = "backward"


class SortingStrategyName(str, Enum):
    """Constants for the sorting strategies"""

    RGB: str = "rgb"
    HSV: str = "hsv"
    HSL: str = "hsl"
    LUMINOSITY: str = "luminosity"
    STEP: str = "step"
    ALTERNATED_STEP: str = "step-alternated"
    HILLBERT: str = "hillbert"
