import os

from harmony.service_layer.services import get_ase_file_path
from tests.helpers import get_temporary_file_path


class TestASEPathGenerator:
    """Tests for the ".ase" path generator"""

    def test_generating_file_path(self) -> None:
        """Test generating path to the output file"""
        arrangement = self._given_options()

        try:
            result = self._when_generator_is_called(arrangement)
            self._then_should_generate_path(arrangement, result)

        finally:
            os.remove(arrangement)

    def _given_options(self) -> str:
        source_file_path = get_temporary_file_path()

        return source_file_path

    def _when_generator_is_called(self, arrangement: str) -> str:
        source_file = open(arrangement)
        final_path = get_ase_file_path(source_file)

        source_file.close()
        return final_path

    def _then_should_generate_path(self, source_file_path: str, result: str) -> None:
        expected_path = f"{source_file_path}.ase"
        actual_path = result

        assert expected_path == actual_path
