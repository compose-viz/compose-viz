from enum import Enum
from typing import Optional

import typer

from compose_viz import __app_name__, __version__
from compose_viz.graph import Graph
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
    output_path: str = typer.Option(
        "./compose-viz.png",
        "--output-path",
        "-o",
        help="Output path for the generated visualization file.",
    ),
    format: VisualizationFormats = typer.Option(
        "PNG",
        "--format",
        "-m",
        help="Output format for the generated visualization file.",
    ),
    _: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="Show the version of compose-viz.",
        callback=_version_callback,
        is_eager=True,
    ),
) -> None:
    parser = Parser()
    compose = parser.parse(input_path)

    if compose:
        typer.echo(f"Successfully parsed {input_path}")

    Graph(compose, output_path).render(format)

    raise typer.Exit()


def start_cli() -> None:
    app(prog_name="cpv")
