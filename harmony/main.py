# pylint: disable=too-many-locals,too-many-arguments
from typing import TextIO, Tuple

import rich
import typer

from harmony import __version__
from harmony.adapters import CommandWithVersion
from harmony.constants import (
    ColorFormat,
    Directions,
    SortCommandArguments,
    SortingStrategyName,
    TXT2ASECommandArguments,
    TXT2CLRCommandArguments,
)
from harmony.models import Color
from harmony.service_layer.ase_writting import ASEWriting
from harmony.service_layer.clr_writting import CLRWriting
from harmony.service_layer.services import (
    ColorReader,
    ColorSorter,
    ColorWriter,
    get_final_file_path,
    get_path_with_extension,
)
from harmony.service_layer.writting_strategies import DefaultWriting, WritingStrategy

app = typer.Typer(pretty_exceptions_show_locals=False, rich_markup_mode="markdown")


@CommandWithVersion(app)
def sort(
    colors_file: typer.FileText = SortCommandArguments.colors_file,
    sorting_algorithm: SortingStrategyName = SortCommandArguments.sorting_algorithm,
    direction: Directions = SortCommandArguments.direction,
    color_format: ColorFormat = SortCommandArguments.color_format,
    suffix: str = SortCommandArguments.suffix,
    generate_names: bool = SortCommandArguments.generate_names,
) -> None:
    """Entry point for generating a file with the sorted colors"""
    try:
        colors = ColorReader(generate_names).extract_from_file(colors_file)
        sorted_colors = ColorSorter(sorting_algorithm).sort(colors, direction)

        final_file_path = get_final_file_path(colors_file, sorting_algorithm, suffix)
        ColorWriter(DefaultWriting(color_format)).write(sorted_colors, final_file_path)

        rich.print(f"[green]Colors sorted and saved to {final_file_path}")

    except Exception as exception:
        rich.print(f"[bright_red] ERROR: {exception}")
        raise typer.Exit(code=1)


def _get_colors_tuple_for_convertion(
    must_generate_color_names: bool, colors_file: TextIO
) -> Tuple[Color, ...]:
    return tuple(ColorReader(must_generate_color_names).extract_from_file(colors_file))


def convert_txt_file(
    colors_file: typer.FileText,
    writing_strategy: WritingStrategy,
    must_generate_color_names: bool,
):
    """Convert the text file using the passed writing strategy

    Args:
        colors_file (typer.FileText): file to be converted
        writing_strategy (WritingStrategy): strategy to use when writing the new file
    """
    ColorWriter(writing_strategy).write(
        _get_colors_tuple_for_convertion(must_generate_color_names, colors_file),
        get_path_with_extension(colors_file, writing_strategy.EXTENSION),
    )

    rich.print(
        "[green]File converted and saved to "
        + get_path_with_extension(colors_file, writing_strategy.EXTENSION)
    )


@CommandWithVersion(app)
def txt2ase(
    colors_file: typer.FileText = TXT2ASECommandArguments.colors_file,
    palette_name: str = TXT2ASECommandArguments.palette_name,
    generate_names: bool = TXT2ASECommandArguments.generate_names,
):
    """Command to convert a text file into a ".ase" file"""
    try:
        convert_txt_file(colors_file, ASEWriting(palette_name), generate_names)

    except Exception as exception:
        rich.print(f"[bright_red] ERROR: {exception}")
        raise typer.Exit(code=1)


@CommandWithVersion(app)
def txt2clr(
    colors_file: typer.FileText = TXT2CLRCommandArguments.colors_file,
    generate_names: bool = TXT2CLRCommandArguments.generate_names,
):
    """Command to convert a text file into a ".clr" file"""
    try:
        convert_txt_file(colors_file, CLRWriting(), generate_names)

    except Exception as exception:
        rich.print(f"[bright_red] ERROR: {exception}")
        raise typer.Exit(code=1)


def _display_version(context: typer.Context):
    if context.invoked_subcommand:
        rich.print(
            "[bright_red] ERROR: parameter --version not compatible with other "
            + "commands"
        )
        raise typer.Exit(code=1)

    rich.print(f"Harmony {__version__}")


@app.callback(invoke_without_command=True)
def main(context: typer.Context, version: bool = False):
    """Harmony is a CLI that provides tools for managing colors"""
    if version:
        _display_version(context)


if __name__ == "__main__":
    app()
