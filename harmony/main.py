import rich
import typer

from harmony.constants import ColorFormat
from harmony.services import ColorReader, ColorSorter, ColorWriter, get_final_file_path

app = typer.Typer(pretty_exceptions_show_locals=False)


@app.command()
def get_colors_from_file(
    file_path: str, format: str = ColorFormat.SAME_AS_INPUT
) -> None:
    """Entry point for generating a file with the sorted colors

    Args:
        file_path (str): path to the file with the original set of colors
    """
    try:
        reader = ColorReader()
        sorter = ColorSorter()
        writer = ColorWriter(format)

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
