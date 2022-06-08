import os

import pytest
from typer.testing import CliRunner

from compose_viz import cli

runner = CliRunner()


@pytest.mark.parametrize(
    "test_file_path",
    [
        "tests/ymls/builds/docker-compose.yml",
        "tests/ymls/cgroup_parent/docker-compose.yml",
        "tests/ymls/container_name/docker-compose.yml",
        "tests/ymls/depends_on/docker-compose.yml",
        "tests/ymls/devices/docker-compose.yml",
        "tests/ymls/env_file/docker-compose.yml",
        "tests/ymls/expose/docker-compose.yml",
        "tests/ymls/extends/docker-compose.yml",
        "tests/ymls/links/docker-compose.yml",
        "tests/ymls/networks/docker-compose.yml",
        "tests/ymls/ports/docker-compose.yml",
        "tests/ymls/profiles/docker-compose.yml",
        "tests/ymls/volumes/docker-compose.yml",
        "examples/full-stack-node-app/docker-compose.yml",
        "examples/non-normative/docker-compose.yml",
    ],
)
def test_cli(test_file_path: str) -> None:
    input_path = f"{test_file_path}"
    output_filename = "compose-viz-test"
    default_format = "png"
    result = runner.invoke(cli.app, ["-o", output_filename, input_path])

    assert result.exit_code == 0
    assert f"Successfully parsed {input_path}\n" in result.stdout
    assert os.path.exists(f"{output_filename}.{default_format}")

    os.remove(f"{output_filename}.{default_format}")
