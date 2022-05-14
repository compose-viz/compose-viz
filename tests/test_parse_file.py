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

    assert len(actual.services) == len(expected.services)

    for actual_service, expected_service in zip(actual.services, expected.services):
        assert actual_service.name == expected_service.name
        assert actual_service.image == expected_service.image
        assert actual_service.ports == expected_service.ports
        assert actual_service.networks == expected_service.networks
        assert actual_service.volumes == expected_service.volumes
        assert actual_service.depends_on == expected_service.depends_on
        assert actual_service.links == expected_service.links
        assert actual_service.extends == expected_service.extends
