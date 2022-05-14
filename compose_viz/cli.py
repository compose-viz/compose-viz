from enum import Enum
import typer
from typing import Optional
from compose_viz import __app_name__, __version__
from compose_viz.parser import Parser


class VisualizationFormats(str, Enum):
    png = "PNG"
    dot = "DOT"


app = typer.Typer(
    invoke_without_command=True,
    no_args_is_help=True,
    subcommand_metavar="",
    add_completion=False,
)


def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"{__app_name__} {__version__}")
        raise typer.Exit()


@app.callback()
def compose_viz(
    input_path: str,
    output_path: Optional[str] = typer.Option(
        None,
        "--output_path",
        "-o",
        help="Output path for the generated visualization.",
    ),
    format: VisualizationFormats = typer.Option(
        "PNG",
        "--format",
        "-m",
        help="Output format for the generated visualization.",
    ),
    _: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="Show the version of compose_viz.",
        callback=_version_callback,
        is_eager=True,
    )
) -> None:
    parser = Parser()
    compose = parser.parse(input_path)

    if compose:
        typer.echo(f"Successfully parsed {input_path}")

    raise typer.Exit()


def start_cli() -> None:
    app(prog_name=__app_name__)
