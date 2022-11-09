import rich
import typer

from harmony.constants import ColorFormat, SortingStrategyName
from harmony.service_layer.services import (
    ColorReader,
    ColorSorter,
    ColorWriter,
    get_final_file_path,
)

app = typer.Typer(pretty_exceptions_show_locals=False)


@app.command()
def sort_colors_from_file(
    colors_file: typer.FileText,
    sorting_algorithm: SortingStrategyName = "hillbert",  # type: ignore
    color_format: ColorFormat = "input",  # type: ignore
) -> None:
    """Entry point for generating a file with the sorted colors"""
    try:
        reader = ColorReader()
        sorter = ColorSorter(sorting_algorithm)
        writer = ColorWriter(color_format)

        colors = reader.extract_from_file(colors_file)
        sorted_colors = sorter.sort(colors)

        final_file_path = get_final_file_path(colors_file)
        writer.write_colors_to_file(sorted_colors, final_file_path)

        rich.print(f"Colors sorted and saved to {final_file_path}")

    except Exception as exception:
        rich.print(f"[bright_red] ERROR: {exception}")
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
