import os

import pytest
from typer.testing import CliRunner

from compose_viz import cli

runner = CliRunner()


@pytest.mark.parametrize(
    "test_file_path",
    [
        "tests/ymls/builds/docker-compose.yml",
        "tests/ymls/depends_on/docker-compose.yml",
        "tests/ymls/extends/docker-compose.yml",
        "tests/ymls/links/docker-compose.yml",
        "tests/ymls/networks/docker-compose.yml",
        "tests/ymls/others/docker-compose.yml",
        "tests/ymls/ports/docker-compose.yml",
        "tests/ymls/volumes/docker-compose.yml",
        "examples/full-stack-node-app/docker-compose.yml",
    ],
)
def test_cli(test_file_path: str) -> None:
    input_path = f"{test_file_path}"
    output_path = "compose-viz-test.png"
    result = runner.invoke(cli.app, ["-o", output_path, input_path])

    assert result.exit_code == 0
    assert f"Successfully parsed {input_path}\n" in result.stdout
    assert os.path.exists(output_path)

    os.remove(output_path)
