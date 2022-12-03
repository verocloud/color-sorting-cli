import re
from typing import List

from click.testing import Result
from typer.testing import CliRunner

from harmony.main import app


class TestVersionCommand:
    """Tests for the --version command"""

    def test_displaying_version(self) -> None:
        """Test displaying current installed versio"""
        arrangement = self._given_arguments()
        result = self._when_runned(arrangement)
        self._then_should_show_version(result)

    def _given_arguments(self) -> List[str]:
        return ["--version"]

    def _then_should_show_version(self, result: Result) -> None:
        expected_exit_code = 0
        actual_exit_code = result.exit_code

        expected_pattern = re.compile("Harmony ([0-9][.]){2}[0-9]")
        actual_output = result.stdout
        did_output_version = expected_pattern.search(actual_output) is not None

        assert expected_exit_code == actual_exit_code
        assert did_output_version

    def test_running_together_with_command(self) -> None:
        """Test running --version together with other command"""
        arrangement = self._given_args_with_other_command()
        result = self._when_runned(arrangement)
        self._then_should_raise_incompatible(result)

    def _given_args_with_other_command(self) -> List[str]:
        return ["--version", "sort"]

    def _when_runned(self, arrangement: List[str]) -> Result:
        runner = CliRunner()
        return runner.invoke(app, arrangement)

    def _then_should_raise_incompatible(self, result: Result) -> None:
        expected_exit_code = 1
        actual_exit_code = result.exit_code

        assert expected_exit_code == actual_exit_code
