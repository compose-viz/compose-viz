from typer.testing import CliRunner
from compose_viz.parser import Parser
from compose_viz.compose import Compose
from compose_viz.service import Service


def test_parse_file():
    expected: Compose = Compose([
        Service(
            name='frontend',
            image='awesome/webapp',
            networks=['front-tier', 'back-tier'],
        ),
        Service(
            name='monitoring',
            image='awesome/monitoring',
            networks=['admin'],
        ),
        Service(
            name='backend',
            image='awesome/backend',
            networks=['back-tier', 'admin'],
        ),
    ])

    parser = Parser()
    actual = parser.parse('tests/in/000001.yaml')

    assert actual == expected
