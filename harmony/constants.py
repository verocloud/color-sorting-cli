import uuid
from enum import Enum

import typer


class DefaultParameters:
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


class ByteOrder(str, Enum):
    """Constants for the byte orders"""

    LITTLE: str = "little"
    BIG: str = "big"


class SortCommandArguments:
    """Store the "sort" command arguments"""

    colors_file: typer.FileText = typer.Argument(
        ..., help="File with the colors to be sorted"
    )
    sorting_algorithm: SortingStrategyName = typer.Option(
        "hillbert",
        "--sorting-algorithm",
        "-a",
        help="Algorithm to be used for sorting the colors",
    )
    direction: Directions = typer.Option(
        "forward",
        "--direction",
        "-d",
        help="If the colors will be sorted forward or backward",
    )
    color_format: ColorFormat = typer.Option(
        "input",
        "--color-format",
        "-f",
        help="The format the colors will be written in the output file",
    )
    suffix: str = typer.Option(
        "_sorted", "--suffix", "-s", help="Suffix to add to the name of the output file"
    )


class TXT2ASECommandArguments:
    """Store the "txt2ase" command arguments"""

    colors_file: typer.FileText = typer.Argument(
        ..., help="File with the colors to be sorted"
    )
    palette_name: str = typer.Option(
        DefaultParameters.PALETTE_NAME,
        "--palette-name",
        "-n",
        help='Name of the palette to be written in to the ".ase" file',
    )


class TXT2CLRCommandArguments:
    """Store the "txt2clr" command arguments"""

    colors_file: typer.FileText = typer.Argument(
        ..., help="File with the colors to be sorted"
    )


class MainArguments:
    """Store the core arguments"""

    version: bool = typer.Option(
        False,
        "--version",
        "-V",
        help="Display the current installed version of the CLI",
    )
