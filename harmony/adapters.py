from typing import Any, Callable

import typer

from harmony import __version__


class CommandWithVersion:
    """Decorator that adds the CLI installed version to the command help text before
    assigning to the app"""

    def __init__(self, app: typer.Typer) -> None:
        self._app = app

    def __call__(self, command: Callable[..., Any]) -> Any:
        command.__doc__ = self._add_version(command)
        add_command = self._app.command()

        return add_command(command)

    def _add_version(self, command: Callable[..., Any]):
        command_docs = command.__doc__

        if not command_docs:
            command_docs = ""

        return f"*Harmony {__version__} [{command.__name__}]*\n\n{command.__doc__}"
