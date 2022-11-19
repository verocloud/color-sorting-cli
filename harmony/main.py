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
    get_ase_file_path,
    get_final_file_path,
)
from harmony.service_layer.writting_strategies import ASEWritting, DefaultWritting

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
        writting_strategy = DefaultWritting(color_format)
        writer = ColorWriter(writting_strategy)

        colors = reader.extract_from_file(colors_file)
        sorted_colors = sorter.sort(colors, direction)

        final_file_path = get_final_file_path(colors_file, sorting_algorithm, suffix)
        writer.write(sorted_colors, final_file_path)

        rich.print(f"Colors sorted and saved to {final_file_path}")

    except Exception as exception:
        rich.print(f"[bright_red] ERROR: {exception}")
        raise typer.Exit(code=1)


@app.command()
def toase(
    colors_file: typer.FileText, palette_name: str = DefaultParameters.PALETTE_NAME
):
    """Command to convert a text file into a ".ase" file"""
    try:
        reader = ColorReader()
        writting_strategy = ASEWritting(palette_name)
        writer = ColorWriter(writting_strategy)

        colors_list = reader.extract_from_file(colors_file)
        colors = tuple(colors_list)

        final_path = get_ase_file_path(colors_file)
        writer.write(colors, final_path)

        rich.print(f"File converted and saved to {final_path}")

    except Exception as exception:
        rich.print(f"[bright_red] ERROR: {exception}")
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
