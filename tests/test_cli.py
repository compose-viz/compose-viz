import os

import pytest
from typer.testing import CliRunner

from compose_viz import cli

runner = CliRunner()


@pytest.mark.parametrize(
    "test_file_path",
    [
        "builds/docker-compose",
        "depends_on/docker-compose",
        "extends/docker-compose",
        "links/docker-compose",
        "networks/docker-compose",
        "ports/docker-compose",
        "volumes/docker-compose",
    ],
)
def test_cli(test_file_path: str) -> None:
    input_path = f"tests/ymls/{test_file_path}.yml"
    output_path = "compose-viz-test.png"
    result = runner.invoke(cli.app, ["-o", output_path, input_path])

    assert result.exit_code == 0
    assert f"Successfully parsed {input_path}\n" in result.stdout
    assert os.path.exists(output_path)

    os.remove(output_path)
