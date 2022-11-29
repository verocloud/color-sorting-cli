import rich
import typer

from harmony.constants import (
    ColorFormat,
    DefaultParameters,
    Directions,
    SortingStrategyName,
)
from harmony.service_layer.services import (
    ColorReader,
    ColorSorter,
    ColorWriter,
    get_final_file_path,
    get_path_with_extension,
)
from harmony.service_layer.writting_strategies import (
    ASEWriting,
    CLRWriting,
    DefaultWriting,
    WritingStrategy,
)

app = typer.Typer(pretty_exceptions_show_locals=False)


@app.command()
def sort(
    colors_file: typer.FileText,
    sorting_algorithm: SortingStrategyName = "hillbert",  # type: ignore
    direction: Directions = "forward",  # type: ignore
    color_format: ColorFormat = "input",  # type: ignore
    suffix: str = "_sorted",
) -> None:
    """Entry point for generating a file with the sorted colors"""
    try:
        reader = ColorReader()
        sorter = ColorSorter(sorting_algorithm)
        writting_strategy = DefaultWriting(color_format)
        writer = ColorWriter(writting_strategy)

        colors = reader.extract_from_file(colors_file)
        sorted_colors = sorter.sort(colors, direction)

        final_file_path = get_final_file_path(colors_file, sorting_algorithm, suffix)
        writer.write(sorted_colors, final_file_path)

        rich.print(f"[green]Colors sorted and saved to {final_file_path}")

    except Exception as exception:
        rich.print(f"[bright_red] ERROR: {exception}")
        raise typer.Exit(code=1)


def convert_txt_file(colors_file: typer.FileText, writing_strategy: WritingStrategy):
    """Convert the text file using the passed writing strategy

    Args:
        colors_file (typer.FileText): file to be converted
        writing_strategy (WritingStrategy): strategy to use when writing the new file
    """

    reader = ColorReader()
    writer = ColorWriter(writing_strategy)

    colors_list = reader.extract_from_file(colors_file)
    colors = tuple(colors_list)

    final_path = get_path_with_extension(colors_file, writing_strategy.EXTENSION)
    writer.write(colors, final_path)

    rich.print(f"[green]File converted and saved to {final_path}")


@app.command()
def txt2ase(
    colors_file: typer.FileText,
    palette_name: str = DefaultParameters.PALETTE_NAME.value,
):
    """Command to convert a text file into a ".ase" file"""
    try:
        writing_strategy = ASEWriting(palette_name)
        convert_txt_file(colors_file, writing_strategy)

    except Exception as exception:
        rich.print(f"[bright_red] ERROR: {exception}")
        raise typer.Exit(code=1)


@app.command()
def txt2clr(colors_file: typer.FileText):
    """Command to convert a text file into a ".clr" file"""
    try:
        writing_strategy = CLRWriting()
        convert_txt_file(colors_file, writing_strategy)

    except Exception as exception:
        rich.print(f"[bright_red] ERROR: {exception}")
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
