import re
from typing import List, Optional

from pydantic import ValidationError

import compose_viz.spec.compose_spec as spec
from compose_viz.models.compose import Compose, Service
from compose_viz.models.extends import Extends
from compose_viz.models.port import Port, Protocol
from compose_viz.models.volume import Volume, VolumeType


class Parser:
    def __init__(self):
        pass

    def parse(self, file_path: str) -> Compose:
        compose_data: spec.ComposeSpecification

        try:
            compose_data = spec.ComposeSpecification.parse_file(file_path)
        except ValidationError as e:
            raise RuntimeError(f"Error parsing file '{file_path}': {e}")

        services: List[Service] = []

        assert compose_data.services is not None, "No services found, aborting."

        for service_name, service_data in compose_data.services.items():
            service_name = str(service_name)

            service_image: Optional[str] = None
            if service_data.build is not None:
                if type(service_data.build) is str:
                    service_image = f"build from '{service_data.build}'"
                elif type(service_data.build) is spec.BuildItem:
                    if service_data.build.context is not None and service_data.build.dockerfile is not None:
                        service_image = (
                            f"build from '{service_data.build.context}' using '{service_data.build.dockerfile}'"
                        )
                    elif service_data.build.context is not None:
                        service_image = f"build from '{service_data.build.context}'"
            if service_data.image is not None:
                if service_image is not None:
                    service_image += ", image: " + service_data.image
                else:
                    service_image = service_data.image

            service_networks: List[str] = []
            if service_data.networks is not None:
                if type(service_data.networks) is spec.ListOfStrings:
                    service_networks = service_data.networks.__root__
                elif type(service_data.networks) is dict:
                    service_networks = list(service_data.networks.keys())

            service_extends: Optional[Extends] = None
            if service_data.extends is not None:
                # https://github.com/compose-spec/compose-spec/blob/master/spec.md#extends
                # The value of the extends key MUST be a dictionary.
                assert type(service_data.extends) is spec.Extend
                service_extends = Extends(
                    service_name=service_data.extends.service, from_file=service_data.extends.file
                )

            service_ports: List[Port] = []
            if service_data.ports is not None:
                for port_data in service_data.ports:
                    host_ip: Optional[str] = None
                    host_port: Optional[str] = None
                    container_port: Optional[str] = None
                    protocol: Optional[str] = None

                    if type(port_data) is float:
                        container_port = str(int(port_data))
                        host_port = f"0.0.0.0:{container_port}"
                    elif type(port_data) is str:
                        regex = r"(?P<host_ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:)?((?P<host_port>\d+(\-\d+)?):)?((?P<container_port>\d+(\-\d+)?))?(/(?P<protocol>\w+))?"  # noqa: E501
                        match = re.match(regex, port_data)

                        if match:
                            host_ip = match.group("host_ip")
                            host_port = match.group("host_port")
                            container_port = match.group("container_port")
                            protocol = match.group("protocol")

                            assert container_port, "Invalid port format, aborting."

                            if container_port is not None and host_port is None:
                                host_port = container_port

                            if host_ip is not None:
                                host_port = f"{host_ip}{host_port}"
                            else:
                                host_port = f"0.0.0.0:{host_port}"
                    elif type(port_data) is spec.Port:
                        assert port_data.target is not None, "Invalid port format, aborting."

                        # ruamel.yaml does not parse port as int
                        assert type(port_data.published) is not int

                        if type(port_data.published) is str:
                            host_port = port_data.published

                        if type(port_data.target) is int:
                            container_port = str(port_data.target)

                        host_ip = port_data.host_ip
                        protocol = port_data.protocol

                        if container_port is not None and host_port is None:
                            host_port = container_port

                        if host_ip is not None:
                            host_port = f"{host_ip}:{host_port}"
                        else:
                            host_port = f"0.0.0.0:{host_port}"

                    assert host_port is not None, "Error while parsing port, aborting."
                    assert container_port is not None, "Error while parsing port, aborting."

                    if protocol is None:
                        protocol = "any"

                    service_ports.append(
                        Port(
                            host_port=host_port,
                            container_port=container_port,
                            protocol=Protocol[protocol],
                        )
                    )

            service_depends_on: List[str] = []
            if service_data.depends_on is not None:
                if type(service_data.depends_on) is spec.ListOfStrings:
                    service_depends_on = service_data.depends_on.__root__
                elif type(service_data.depends_on) is dict:
                    for depends_on in service_data.depends_on.keys():
                        service_depends_on.append(str(depends_on))

            service_volumes: List[Volume] = []
            if service_data.volumes is not None:
                for volume_data in service_data.volumes:
                    if type(volume_data) is str:
                        assert ":" in volume_data, "Invalid volume input, aborting."

                        spilt_data = volume_data.split(":")
                        if len(spilt_data) == 2:
                            service_volumes.append(Volume(source=spilt_data[0], target=spilt_data[1]))
                        elif len(spilt_data) == 3:
                            service_volumes.append(
                                Volume(
                                    source=spilt_data[0],
                                    target=spilt_data[1],
                                    access_mode=spilt_data[2],
                                )
                            )
                    elif type(volume_data) is spec.ServiceVolume:
                        assert volume_data.target is not None, "Invalid volume input, aborting."

                        # https://github.com/compose-spec/compose-spec/blob/master/spec.md#long-syntax-4
                        # `volume_data.source` is not applicable for a tmpfs mount.
                        if volume_data.source is None:
                            volume_data.source = volume_data.target

                        assert volume_data.source is not None

                        service_volumes.append(
                            Volume(
                                source=volume_data.source,
                                target=volume_data.target,
                                type=VolumeType[volume_data.type],
                            )
                        )

            service_links: List[str] = []
            if service_data.links is not None:
                service_links = service_data.links

            services.append(
                Service(
                    name=service_name,
                    image=service_image,
                    networks=service_networks,
                    extends=service_extends,
                    ports=service_ports,
                    depends_on=service_depends_on,
                    volumes=service_volumes,
                    links=service_links,
                )
            )

        return Compose(services=services)
