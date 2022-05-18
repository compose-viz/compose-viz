import pytest
from compose_viz.parser import Parser
from compose_viz.compose import Compose
from compose_viz.service import Service
from compose_viz.extends import Extends

@pytest.mark.parametrize('test_input,expected',[
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
        ),
        Service(
            name='common',
            image='busybox',
            extends=Extends(service_name='frontend'),
        ),
        Service(
            name='cli',
            extends=['common'],
        ),
    ])),
    ('tests/in/000011.yaml',Compose([
        Service(
            name='frontend',
            image='awesome/webapp',
            networks=['front-tier', 'back-tier'],
        ),
        Service(
            name='monitoring',
            image='awesome/monitoring',
            networks=['admin'],
            extends=Extends(service_name='frontend'),
        ),
        Service(
            name='backend',
            image='awesome/backend',
            networks=['back-tier', 'admin'],
            extends=Extends(service_name='frontend'),
        ),
    ])),
    ('tests/in/000100.yaml',Compose([
        Service(
            name='web',
            ports=['8000:5000'],
        ),
        Service(
            name='redis',
            image='redis:alpine',
        ),
    ])),
    ('tests/in/000101.yaml',Compose([
        Service(
            name='frontend',
            image='awesome/webapp',
            ports=['8000:5000'],
            networks=['front-tier', 'back-tier'],
        ),
        Service(
            name='monitoring',
            image='awesome/monitoring',
            ports=['8000:5001'],
            networks=['admin'],
        ),
        Service(
            name='backend',
            image='awesome/backend',
            ports=['8000:5010'],
            networks=['back-tier', 'admin'],
        ),
    ])),
    ('tests/in/000110.yaml',Compose([
        Service(
            name='frontend',
            image='awesome/webapp',
            ports=['8000:5000'],
        ),
        Service(
            name='monitoring',
            image='awesome/monitoring',
            extends=Extends(service_name='frontend'),
        ),
        Service(
            name='backend',
            image='awesome/backend',
            extends=Extends(service_name='frontend'),
            ports=['8000:5001'],
        ),
    ])),
    ('tests/in/000111.yaml',Compose([
        Service(
            name='frontend',
            image='awesome/webapp',
            ports=['8000:5000'],
            networks=['front-tier', 'back-tier'],
        ),
        Service(
            name='monitoring',
            image='awesome/monitoring',
            networks=['admin'],
            extends=Extends(service_name='frontend'),
        ),
        Service(
            name='backend',
            image='awesome/backend',
            ports=['8000:5001'],
            networks=['back-tier', 'admin'],
            extends=Extends(service_name='frontend'),
        ),
    ])),
    ('tests/in/001000.yaml',Compose([
        Service(
            name='web',
            depends_on=['db','redis'],
        ),
        Service(
            name='redis',
            image='redis',
        ),
        Service(
            name='db',
            image='postgres',
        ),
    ])),
    ('tests/in/001001.yaml',Compose([
        Service(
            name='frontend',
            image='awesome/webapp',
            networks=['front-tier', 'back-tier'],
            depends_on=['monitoring','backend'],
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
    ('tests/in/001010.yaml',Compose([
        Service(
            name='web',
            depends_on=['db','redis'],
            extends=Extends(service_name='redis'),
        ),
        Service(
            name='redis',
            image='redis',
        ),
        Service(
            name='db',
            image='postgres',
        ),
    ])),
    ('tests/in/001011.yaml',Compose([
        Service(
            name='frontend',
            image='awesome/webapp',
            networks=['front-tier', 'back-tier'],
            depends_on=['monitoring','backend'],
            extends=Extends(service_name='backend'),
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
    ('tests/in/001100.yaml',Compose([
        Service(
            name='frontend',
            image='awesome/webapp',
            ports=['8000:5000'],
        ),
        Service(
            name='monitoring',
            image='awesome/monitoring',
            depends_on=['backend'],
            ports=['8000:5010'],
        ),
        Service(
            name='backend',
            image='awesome/backend',
            ports=['8000:5001'],
        ),
    ])),
    ('tests/in/001101.yaml',Compose([
        Service(
            name='frontend',
            image='awesome/webapp',
            networks=['front-tier', 'back-tier'],
        ),
        Service(
            name='monitoring',
            image='awesome/monitoring',
            networks=['admin'],
            depends_on=['backend'],
            ports=['8000:5010'],
        ),
        Service(
            name='backend',
            image='awesome/backend',
            networks=['back-tier', 'admin'],
        ),
    ])),
    ('tests/in/001110.yaml',Compose([
        Service(
            name='frontend',
            image='awesome/webapp',
            ports=['8000:5000'],
        ),
        Service(
            name='monitoring',
            image='awesome/monitoring',
            depends_on=['backend'],
            extends=Extends(service_name='frontend'),
            ports=['8000:5010'],
        ),
        Service(
            name='backend',
            image='awesome/backend',
            ports=['8000:5001'],
        ),
    ])),
    ('tests/in/001111.yaml',Compose([
        Service(
            name='frontend',
            image='awesome/webapp',
            networks=['front-tier', 'back-tier'],
        ),
        Service(
            name='monitoring',
            image='awesome/monitoring',
            networks=['admin'],
            depends_on=['backend'],
            extends=Extends(service_name='frontend'),
            ports=['8000:5010'],
        ),
        Service(
            name='backend',
            image='awesome/backend',
            networks=['back-tier', 'admin'],
        ),
    ])),
    ('tests/in/010000.yaml',Compose([
        Service(
            name='backend',
            image='awesome/backend',
            volumes=['db-data'],
        ),
    ])),
    ('tests/in/010001.yaml',Compose([
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
            volumes=['db-data'],
        ),
    ])),
    ('tests/in/010010.yaml',Compose([
        Service(
            name='common',
            image='busybox',
            volumes=['common-volume'],
        ),
        Service(
            name='cli',
            extends=Extends(service_name='common'),
            volumes=['cli-volume'],
        ),
    ])),
    ('tests/in/010011.yaml',Compose([
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
            volumes=['db-data'],
            extends=Extends(service_name='monitoring'),
        ),
    ])),
    ('tests/in/010100.yaml',Compose([
        Service(
            name='backend',
            image='awesome/backend',
            volumes=['db-data'],
            ports=["8000:5000"],
        ),
    ])),

    ('tests/in/010111.yaml',Compose([
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
            volumes=['db-data'],
            extends=Extends(service_name='monitoring'),
            ports=['8000:5000'],
        ),
    ])),

    ('tests/in/011100.yaml',Compose([
        Service(
            name='frontend',
            image='awesome/webapp',
        ),
        Service(
            name='monitoring',
            image='awesome/monitoring',
        ),
        Service(
            name='backend',
            image='awesome/backend',
            volumes=['db-data'],
            depends_on=['monitoring'],
            extends=Extends(service_name='frontend'),
            ports=['8000:5010'],
        ),
    ])),

    ('tests/in/011110.yaml',Compose([
        Service(
            name='frontend',
            image='awesome/webapp',
        ),
        Service(
            name='monitoring',
            image='awesome/monitoring',
        ),
        Service(
            name='backend',
            image='awesome/backend',
            volumes=['db-data'],
            depends_on=['monitoring'],
            extends=Extends(service_name='frontend'),
            ports=['8000:5010'],
        ),
    ])),
    ('tests/in/011111.yaml',Compose([
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
            volumes=['db-data'],
            depends_on=['monitoring'],
            extends=Extends(service_name='monitoring'),
            ports=['8000:5010'],
        ),
    ])),
    ('tests/in/100000.yaml',Compose([
        Service(
            name='web',
            links=['db:database'],
        ),
        Service(
            name='db',
            image='postgres',
        ),
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
