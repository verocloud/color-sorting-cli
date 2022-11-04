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
    file_path: str,
    sorting_algorithm: str = SortingStrategyName.HILLBERT,
    color_format: str = ColorFormat.SAME_AS_INPUT,
) -> None:
    """Entry point for generating a file with the sorted colors

    Args:
        file_path (str): path to the file with the original set of colors
        sorting_algorithm (str): algorithm to be used for sorting the colors
        color_format (str): format of the colors to be writted to the file
    """
    try:
        reader = ColorReader()
        sorter = ColorSorter(sorting_algorithm)
        writer = ColorWriter(color_format)

        colors = reader.extract_from_file(file_path)
        sorted_colors = sorter.sort(colors)

        final_file_path = get_final_file_path(file_path)
        writer.write_colors_to_file(sorted_colors, final_file_path)

        rich.print(f"Colors sorted and saved to {final_file_path}")

    except Exception as exception:
        rich.print(f"[bright_red] ERROR: {exception}")
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
