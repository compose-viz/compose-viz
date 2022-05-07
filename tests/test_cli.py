import pytest
from typer.testing import CliRunner
from compose_viz import cli


runner = CliRunner()


def test_cli():
    input_path = "tests/in/000001.yaml"
    result = runner.invoke(cli.app, [input_path])

    assert result.exit_code == 0
    assert f"Successfully parsed {input_path}\n" in result.stdout
