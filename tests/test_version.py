from typer.testing import CliRunner
from compose_viz import cli, __app_name__, __version__


runner = CliRunner()


def test_version():
    result = runner.invoke(cli.app, ["--version"])

    assert result.exit_code == 0
    assert f"{__app_name__} {__version__}\n" in result.stdout
