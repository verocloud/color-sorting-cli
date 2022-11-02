import rich
import typer

from harmony.services import ColorExtractor, ColorSorter, get_final_file_path

app = typer.Typer(pretty_exceptions_show_locals=False)


@app.command()
def get_colors_from_file(file_path: str) -> None:
    """Entry point for generating a file with the sorted colors

    Args:
        file_path (str): path to the file with the original set of colors
    """
    extractor = ColorExtractor()
    sorter = ColorSorter()

    colors = extractor.extract_from_file(file_path)
    sorter.sort(colors)

    final_file_path = get_final_file_path(file_path)
    rich.print(f"Colors sorted and saved to {final_file_path}")


if __name__ == "__main__":
    app()
