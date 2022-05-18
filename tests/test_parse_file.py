import pytest
from compose_viz.parser import Parser
from compose_viz.compose import Compose
from compose_viz.service import Service

@pytest.mark.parametrize("test_input,expected",[
    ('tests/in/000001.yaml',Compose([
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
    ])),
    ('tests/in/000010.yaml',Compose([
        Service(
            name='base',
            image='busybox',
            user='root',
        ),
        Service(
            name='common',
            image='busybox',
            extends='base'
        ),
        Service(
            name='cli',
            extends='common'
        ),
    ])),
    ('tests/in/000100.yaml',Compose([
        #version='3.9'
        Service(
            build='.',
            ports=['8000:5000']
        ),
        Service(
            name='redis',
            image='redis:alpine',
        ),
    ])),
    ('tests/in/001000.yaml',Compose([
        Service(
            name='web',
            build='.',
            depends_on=['db','redis']
        ),
        Service(
            name='redis',
            image='redis'
        ),
        Service(
            name='db',
            image='postgres'
        ),
    ])),
    ('tests/in/010000.yaml',Compose([
        Service(
            name='backend',
            image='awesome/backend',
            volumes=['db-data']
        )
    ])),
    ('tests/in/100000.yaml',Compose([
        Service(
            name='web',
            build='.',
            links=['db:database']
        ),
        Service(
            name='db',
            image='postgres'
        )
    ])),
    ])
    
def test_parse_file(test_input, expected):
    parser = Parser()
    actual = parser.parse(test_input)

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
