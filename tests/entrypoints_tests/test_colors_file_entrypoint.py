import os

import pytest
from click.testing import Result
from typer.testing import CliRunner

from harmony.main import app
from tests.helpers import get_temporary_file_path


class TestColorsFileEntrypoint:
    @pytest.fixture
    def runner(self) -> CliRunner:
        return CliRunner()

    def test_passing_file(self, runner: CliRunner) -> None:
        """Test passing valid file to CLI"""
        arrangements = self._given_valid_file()
        results = self._when_file_is_sent(runner, arrangements)
        self._then_should_show_success_message(results, arrangements)
        os.remove(arrangements)

    def _given_valid_file(self) -> str:
        return get_temporary_file_path()

    def _then_should_show_success_message(self, results: Result, source_file: str):
        expected_exit_code = 0
        actual_exit_code = results.exit_code

        expected_final_file_path = self._get_final_file_path(source_file)
        expected_message = f"Colors sorted and saved to {expected_final_file_path}"
        actual_message = results.stdout

        assert expected_exit_code == actual_exit_code
        assert expected_message in actual_message

    def _get_final_file_path(self, source_file_path: str) -> str:
        index_of_extension = source_file_path.rfind(".")

        if index_of_extension >= 0:
            extension = source_file_path[index_of_extension:]
            return f"{source_file_path[:index_of_extension]}_sorted{extension}"

        return f"{source_file_path}_sorted"

    def test_passing_invalid_file(self, runner: CliRunner):
        """Test passing invalid file to CLI"""
        arrangements = "not-a-file"
        results = self._when_file_is_sent(runner, arrangements)
        self._then_should_show_error_message(results, arrangements)

    def _when_file_is_sent(self, runner: CliRunner, arrangements: str) -> Result:
        return runner.invoke(app, [arrangements])

    def _then_should_show_error_message(self, results: Result, source_file: str):
        expected_exit_code = 2
        actual_exit_code = results.exit_code

        assert expected_exit_code == actual_exit_code
