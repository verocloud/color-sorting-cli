import uuid
from enum import Enum

import typer

MAXIMUM_RGB_VALUE = 255
MAXIMUM_HUE_VALUE = 360
MAXIMUM_8_BIT_INTEGER_VALUE = 255


class Resources:
    """Constants for the package resources"""

    COLOR_NAMES_CSV = "color-names.csv"
    SQLITE_DATABASE = "db.sqlite3"


class DefaultParameters:
    """Constants for the default subjective parameters"""

    PALETTE_NAME: str = f"Palette {uuid.uuid4()} sorted by Harmony"
    SUFFIX: str = "_sorted"


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
        SortingStrategyName.HILLBERT.value,
        "--sorting-algorithm",
        "-a",
        help="Algorithm to be used for sorting the colors",
    )
    direction: Directions = typer.Option(
        Directions.FORWARD.value,
        "--direction",
        "-d",
        help="If the colors will be sorted forward or backward",
    )
    color_format: ColorFormat = typer.Option(
        ColorFormat.SAME_AS_INPUT.value,
        "--color-format",
        "-f",
        help="The format the colors will be written in the output file",
    )
    suffix: str = typer.Option(
        DefaultParameters.SUFFIX,
        "--suffix",
        "-s",
        help="Suffix to add to the name of the output file",
    )
    generate_names: bool = typer.Option(
        True,
        "--no-generate-color-names",
        "-G",
        help="Disables the color name generation for the unlabelled colors.",
    )


class TXT2ASECommandArguments:
    """Store the "txt2ase" command arguments"""

    colors_file: typer.FileText = typer.Argument(..., help="File to be converted")
    palette_name: str = typer.Option(
        DefaultParameters.PALETTE_NAME,
        "--palette-name",
        "-n",
        help='Name of the palette to be written in to the ".ase" file',
    )
    generate_names: bool = typer.Option(
        True,
        "--no-generate-color-names",
        "-G",
        help="Disables the color name generation for the unlabelled colors.",
    )


class TXT2CLRCommandArguments:
    """Store the "txt2clr" command arguments"""

    colors_file: typer.FileText = typer.Argument(..., help="File to be converted")
    generate_names: bool = typer.Option(
        True,
        "--no-generate-color-names",
        "-G",
        help="Disables the color name generation for the unlabelled colors.",
    )


class MainArguments:
    """Store the core arguments"""

    version: bool = typer.Option(
        False,
        "--version",
        "-V",
        help="Display the current installed version of the CLI",
    )


class TableNames:
    """Constants for the database tables names"""

    COLOR_NAME = "namegeneration_colorname"


class QueryConstants:
    """Constants for query sintax elements"""

    ALL_COLUMNS = ["*"]


class FloatComparisonTolerance(float, Enum):
    """Constants for tolerance on float comparison"""

    THREE_DECIMAL_PLACES = 10 ** (-3)
    SEVEN_DECIMAL_PLACES = 10 ** (-7)
