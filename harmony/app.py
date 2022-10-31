import rich
import typer

from harmony.services import check_for_file_path, get_final_file_path

app = typer.Typer(pretty_exceptions_show_locals=False)


@app.command()
def get_colors_from_file(file_path: str):
    check_for_file_path(file_path)
    final_file_path = get_final_file_path(file_path)

    rich.print(f"Colors sorted and saved to {final_file_path}")


if __name__ == "__main__":
    app()
