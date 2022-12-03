import re
from typing import Any, Callable

from typer import Typer

from harmony.adapters import CommandWithVersion


class TestCommandWithVersion:
    """Tests for the command with version decorator"""

    def test_add_version_to_doc(self) -> None:
        """Test adding version to the command documentation"""
        arrangement = self._given_function()
        result = self._when_added_decorator(arrangement)
        self._then_should_add_version(result)

    def _given_function(self) -> Callable[..., Any]:
        def function_to_wrap():
            pass

        return function_to_wrap

    def _when_added_decorator(
        self, arrangement: Callable[..., Any]
    ) -> Callable[..., Any]:
        app = Typer()
        add_command = CommandWithVersion(app)

        return add_command(arrangement)

    def _then_should_add_version(self, result: Callable[..., Any]) -> None:
        expected_pattern = re.compile("Harmony ([0-9][.]){2}[0-9]")
        actual_docstring = result.__doc__
        there_is_version_in_doc = expected_pattern.search(actual_docstring) is not None

        print(actual_docstring)

        assert there_is_version_in_doc
