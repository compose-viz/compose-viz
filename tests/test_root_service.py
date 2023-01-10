import os

from typer.testing import CliRunner

from compose_viz import cli

runner = CliRunner()


def test_root_service() -> None:
    input_path = "examples/voting-app/docker-compose.yml"
    output_filename = "compose-viz-test"
    default_format = "png"
    result = runner.invoke(cli.app, ["-r", "vote", "-o", output_filename, input_path])

    assert result.exit_code == 0
    assert f"Successfully parsed {input_path}\n" in result.stdout
    assert os.path.exists(f"{output_filename}.{default_format}")

    os.remove(f"{output_filename}.{default_format}")


def test_root_service_key_error() -> None:
    input_path = "examples/voting-app/docker-compose.yml"
    output_filename = "compose-viz-test"
    default_format = "png"
    result = runner.invoke(cli.app, ["-r", "not_exist_service", "-o", output_filename, input_path])

    assert result.exit_code == 1
    assert result.exception is not None
    assert result.exception.args[0] == f"Service 'not_exist_service' not found in given compose file: '{input_path}'"
    assert not os.path.exists(f"{output_filename}.{default_format}")
