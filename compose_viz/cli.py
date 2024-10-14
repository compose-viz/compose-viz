from typing import Optional

import typer

from compose_viz import __app_name__, __version__
from compose_viz.graph import Graph
from compose_viz.models.viz_formats import VizFormats
from compose_viz.parser import Parser

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
    output_filename: str = typer.Option(
        "compose-viz",
        "--output-filename",
        "-o",
        help="Output filename for the generated visualization file.",
    ),
    format: VizFormats = typer.Option(
        "png",
        "--format",
        "-m",
        help="Output format for the generated visualization file.",
    ),
    root_service: str = typer.Option(
        None,
        "--root-service",
        "-r",
        help="Root of the service tree (convenient for large compose yamls)",
    ),
    include_legend: bool = typer.Option(
        False,
        "--legend",
        "-l",
        help="Include a legend in the visualization.",
    ),
    no_ports: bool = typer.Option(
        False,
        "--no-ports",
        "-p",
        help="Don't show ports.",
    ),
    simple: bool = typer.Option(
        False, "--simple", "-s", help="Output a more simple graph with no image names and only basename of sources."
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
    parser = Parser(no_ports, simple)
    compose = parser.parse(input_path, root_service=root_service)

    if compose:
        typer.echo(f"Successfully parsed {input_path}")

    Graph(compose, output_filename, include_legend, simple).render(format)

    raise typer.Exit()


def start_cli() -> None:
    app(prog_name="cpv")
