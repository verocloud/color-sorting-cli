import os
from typing import Dict

from harmony.constants import SortingStrategyName
from harmony.service_layer.services import get_final_file_path
from tests.helpers import get_temporary_file_path


class TestFilePathGenerator:
    """Tests for the file path generator"""

    def test_generating_file_path(self) -> None:
        """Test generating path to the output file"""
        arrangement = self._given_options()
        temporary_file_path = arrangement.get("source_file_path", "not-a-file")

        result = self._when_generator_is_called(arrangement)
        self._then_should_generate_path(temporary_file_path, result)

        os.remove(temporary_file_path)

    def _given_options(self) -> Dict[str, object]:
        source_file_path = get_temporary_file_path()
        sorting_strategy = SortingStrategyName.HILLBERT
        suffix = "_somesuffix"

        return {
            "source_file_path": source_file_path,
            "sorting_strategy": sorting_strategy,
            "suffix": suffix,
        }

    def _when_generator_is_called(self, arrangement: Dict[str, object]) -> str:
        temporary_file_path = arrangement.pop("source_file_path", "not-a-file")
        source_file = open(temporary_file_path)

        source_file_data = {"source_file": source_file}
        arrangement.update(source_file_data)

        final_path = get_final_file_path(**arrangement)
        source_file.close()

        return final_path

    def _then_should_generate_path(
        self, source_file_path: Dict[str, object], result: str
    ) -> None:
        expected_path = self._get_expected_path(source_file_path)
        actual_path = result

        assert expected_path == actual_path

    def _get_expected_path(self, source_file_path: str) -> str:
        file_path = ""
        extension = ""

        extension_index = source_file_path.rfind(".")
        there_is_an_extension = extension_index > 0

        if there_is_an_extension:
            file_path = source_file_path[:extension_index]
            extension = source_file_path[extension_index:]

            return f"{file_path}_hillbert_somesuffix{extension}"

        return f"{source_file_path}_hillbert"
