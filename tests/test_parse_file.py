import pytest

from compose_viz.models.compose import Compose
from compose_viz.models.device import Device
from compose_viz.models.extends import Extends
from compose_viz.models.port import Port, Protocol
from compose_viz.models.service import Service
from compose_viz.models.volume import Volume, VolumeType
from compose_viz.parser import Parser


@pytest.mark.parametrize(
    "test_file_path, expected",
    [
        (
            "builds/docker-compose",
            Compose(
                services=[
                    Service(
                        name="frontend",
                        image="build from './frontend', image: awesome/frontend",
                    ),
                    Service(
                        name="backend",
                        image="build from 'backend' using '../backend.Dockerfile'",
                    ),
                    Service(
                        name="db",
                        image="build from './db'",
                    ),
                ],
            ),
        ),
        (
            "depends_on/docker-compose",
            Compose(
                services=[
                    Service(
                        name="frontend",
                        image="awesome/frontend",
                        depends_on=[
                            "db",
                            "redis",
                        ],
                    ),
                    Service(
                        name="backend",
                        image="awesome/backend",
                        depends_on=[
                            "db",
                            "redis",
                        ],
                    ),
                    Service(
                        name="db",
                        image="mysql",
                    ),
                    Service(
                        name="redis",
                        image="redis",
                    ),
                ],
            ),
        ),
        (
            "extends/docker-compose",
            Compose(
                services=[
                    Service(
                        name="base",
                        image="alpine:latest",
                    ),
                    Service(
                        name="derive_from_base",
                        image="alpine:edge",
                        extends=Extends(
                            service_name="base",
                        ),
                    ),
                    Service(
                        name="derive_from_file",
                        extends=Extends(
                            service_name="web",
                            from_file="web.yml",
                        ),
                    ),
                ],
            ),
        ),
        (
            "links/docker-compose",
            Compose(
                services=[
                    Service(
                        name="frontend",
                        image="awesome/frontend",
                        links=[
                            "db:database",
                        ],
                    ),
                    Service(
                        name="db",
                        image="mysql",
                    ),
                ],
            ),
        ),
        (
            "networks/docker-compose",
            Compose(
                services=[
                    Service(
                        name="frontend",
                        image="awesome/frontend",
                        networks=[
                            "front-tier",
                            "back-tier",
                        ],
                    ),
                    Service(
                        name="monitoring",
                        image="awesome/monitoring",
                        networks=[
                            "admin",
                        ],
                    ),
                    Service(
                        name="backend",
                        image="awesome/backend",
                        networks=[
                            "back-tier",
                            "admin",
                        ],
                    ),
                ],
            ),
        ),
        (
            "ports/docker-compose",
            Compose(
                services=[
                    Service(
                        name="frontend",
                        image="awesome/frontend",
                        ports=[
                            Port(
                                host_port="0.0.0.0:3000",
                                container_port="3000",
                            ),
                            Port(
                                host_port="0.0.0.0:3000-3005",
                                container_port="3000-3005",
                            ),
                            Port(
                                host_port="0.0.0.0:9090-9091",
                                container_port="8080-8081",
                            ),
                            Port(
                                host_port="0.0.0.0:49100",
                                container_port="22",
                            ),
                            Port(
                                host_port="127.0.0.1:8001",
                                container_port="8001",
                            ),
                            Port(
                                host_port="127.0.0.1:5000-5010",
                                container_port="5000-5010",
                            ),
                            Port(
                                host_port="0.0.0.0:6060",
                                container_port="6060",
                                protocol=Protocol.udp,
                            ),
                            Port(
                                host_port="0.0.0.0:7777",
                                container_port="7777",
                            ),
                            Port(
                                host_port="${BIND_IP:-127.0.0.1}:8080",
                                container_port="8080",
                            ),
                            Port(
                                host_port="127.0.0.1:8080",
                                container_port="80",
                                protocol=Protocol.tcp,
                            ),
                            Port(
                                host_port="0.0.0.0:443",
                                container_port="443",
                            ),
                        ],
                    ),
                ],
            ),
        ),
        (
            "volumes/docker-compose",
            Compose(
                services=[
                    Service(
                        name="backend",
                        image="awesome/backend",
                        volumes=[
                            Volume(
                                source="./data",
                                target="/data",
                            ),
                            Volume(
                                source="/var/run/postgres/postgres.sock",
                                target="/var/run/postgres/postgres.sock",
                                type=VolumeType.bind,
                            ),
                        ],
                    ),
                    Service(
                        name="common",
                        image="busybox",
                        volumes=[
                            Volume(
                                source="common-volume",
                                target="/var/lib/backup/data",
                            ),
                        ],
                    ),
                    Service(
                        name="cli",
                        extends=Extends(
                            service_name="common",
                        ),
                        volumes=[
                            Volume(
                                source="cli-volume",
                                target="/var/lib/backup/data",
                                access_mode="ro,z",
                            ),
                        ],
                    ),
                    Service(
                        name="tmp",
                        image="awesome/nginx",
                        volumes=[
                            Volume(
                                source="/app",
                                target="/app",
                                type=VolumeType.tmpfs,
                            ),
                        ],
                    ),
                ],
            ),
        ),
        (
            "cgroup_parent/docker-compose",
            Compose(
                services=[
                    Service(
                        name="frontend",
                        image="awesome/frontend",
                        cgroup_parent="system",
                    ),
                ],
            ),
        ),
        (
            "container_name/docker-compose",
            Compose(
                services=[
                    Service(
                        name="frontend",
                        image="awesome/frontend",
                        container_name="myfrontend",
                    ),
                ],
            ),
        ),
        (
            "env_file/docker-compose",
            Compose(
                services=[
                    Service(
                        name="frontend",
                        image="awesome/frontend",
                        env_file=["a.env"],
                    ),
                    Service(
                        name="backend",
                        image="awesome/backend",
                        env_file=["b.env"],
                    ),
                    Service(
                        name="db",
                        image="awesome/db",
                        env_file=["c.env", "d.env"],
                    ),
                ],
            ),
        ),
        (
            "expose/docker-compose",
            Compose(
                services=[
                    Service(
                        name="frontend",
                        image="awesome/frontend",
                        expose=["27118"],
                    ),
                    Service(
                        name="backend",
                        image="awesome/backend",
                        expose=["27017", "27018"],
                    ),
                ],
            ),
        ),
        (
            "profiles/docker-compose",
            Compose(
                services=[
                    Service(
                        name="frontend",
                        image="awesome/frontend",
                        profiles=["frontend"],
                    ),
                    Service(
                        name="phpmyadmin",
                        image="phpmyadmin",
                        profiles=["debug"],
                    ),
                    Service(
                        name="db",
                        image="awesome/db",
                        profiles=["db", "sql"],
                    ),
                ],
            ),
        ),
        (
            "devices/docker-compose",
            Compose(
                services=[
                    Service(
                        name="frontend",
                        image="awesome/frontend",
                        devices=[
                            Device(
                                host_path="/dev/ttyUSB0",
                                container_path="/dev/ttyUSB1",
                            )
                        ],
                    ),
                    Service(
                        name="backend",
                        image="awesome/backend",
                        devices=[
                            Device(
                                host_path="/dev/ttyUSB2",
                                container_path="/dev/ttyUSB3",
                            ),
                            Device(
                                host_path="/dev/sda",
                                container_path="/dev/xvda",
                                cgroup_permissions="rwm",
                            ),
                        ],
                    ),
                ],
            ),
        ),
    ],
)
def test_parse_file(test_file_path: str, expected: Compose) -> None:
    parser = Parser()
    actual = parser.parse(f"tests/ymls/{test_file_path}.yml")

    assert len(actual.services) == len(expected.services)

    for actual_service, expected_service in zip(actual.services, expected.services):
        assert actual_service.name == expected_service.name
        assert actual_service.image == expected_service.image

        assert len(actual_service.ports) == len(expected_service.ports)
        for actual_port, expected_port in zip(actual_service.ports, expected_service.ports):
            assert actual_port.host_port == expected_port.host_port
            assert actual_port.container_port == expected_port.container_port
            assert actual_port.protocol == expected_port.protocol

        assert actual_service.networks == expected_service.networks

        assert len(actual_service.volumes) == len(expected_service.volumes)
        for actual_volume, expected_volume in zip(actual_service.volumes, expected_service.volumes):
            assert actual_volume.source == expected_volume.source
            assert actual_volume.target == expected_volume.target
            assert actual_volume.type == expected_volume.type

        assert actual_service.depends_on == expected_service.depends_on
        assert actual_service.links == expected_service.links

        assert (actual_service.extends is not None) == (expected_service.extends is not None)

        if (actual_service.extends is not None) and (expected_service.extends is not None):
            assert actual_service.extends.service_name == expected_service.extends.service_name
            assert actual_service.extends.from_file == expected_service.extends.from_file

        assert actual_service.cgroup_parent == expected_service.cgroup_parent
        assert actual_service.container_name == expected_service.container_name

        assert actual_service.expose == expected_service.expose
        assert actual_service.env_file == expected_service.env_file
        assert actual_service.profiles == expected_service.profiles

        assert len(actual_service.devices) == len(expected_service.devices)
        for actual_device, expected_device in zip(actual_service.devices, expected_service.devices):
            assert actual_device.host_path == expected_device.host_path
            assert actual_device.container_path == expected_device.container_path
            assert actual_device.cgroup_permissions == expected_device.cgroup_permissions
