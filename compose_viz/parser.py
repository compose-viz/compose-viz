import re
from os import path
from typing import Any, Dict, List, Optional, Union

from pydantic_yaml import parse_yaml_raw_as

import compose_viz.spec.compose_spec as spec
from compose_viz.models.compose import Compose, Service
from compose_viz.models.device import Device
from compose_viz.models.extends import Extends
from compose_viz.models.port import AppProtocol, Port, Protocol
from compose_viz.models.volume import Volume, VolumeType


class Parser:
    def __init__(self, no_ports: bool = False, simple: bool = False):
        self.no_ports = no_ports
        self.simple = simple

    @staticmethod
    def _unwrap_depends_on(data_depends_on: Union[spec.ListOfStrings, Dict[Any, spec.DependsOn], None]) -> List[str]:
        service_depends_on = []
        if type(data_depends_on) is spec.ListOfStrings:
            service_depends_on = data_depends_on.root
        elif type(data_depends_on) is dict:
            for depends_on in data_depends_on.keys():
                service_depends_on.append(str(depends_on))
        return service_depends_on

    @staticmethod
    def compile_dependencies(service_name: str, services: Dict[Any, spec.Service], file_path: str) -> List[str]:
        assert service_name in services, f"Service '{service_name}' not found in given compose file: '{file_path}'"

        dependencies = []
        for dependency in Parser._unwrap_depends_on(services[service_name].depends_on):
            if dependency:
                dependencies.append(dependency)
                dependencies.extend(Parser.compile_dependencies(dependency, services, file_path))
        return dependencies

    def get_source(self, source: str):
        return path.basename(source) if self.simple else source

    def parse(self, file_path: str, root_service: Optional[str] = None) -> Compose:
        compose_data: spec.ComposeSpecification

        try:
            with open(file_path, "r") as file:
                file_content = file.read()
            compose_data = parse_yaml_raw_as(spec.ComposeSpecification, file_content)
        except Exception as e:
            raise RuntimeError(f"Error parsing file '{file_path}': {e}")

        services: List[Service] = []

        assert compose_data.services is not None, "No services found, aborting."

        root_dependencies: List[str] = []
        if root_service:
            root_dependencies = Parser.compile_dependencies(root_service, compose_data.services, file_path)
            root_dependencies.append(root_service)
            root_dependencies = list(set(root_dependencies))

        for service_name, service_data in compose_data.services.items():
            service_name = str(service_name)
            if root_service and service_name not in root_dependencies:
                continue

            service_image: Optional[str] = None
            if service_data.build is not None:
                if type(service_data.build) is str:
                    service_image = f"build from '{service_data.build}'"
                elif type(service_data.build) is spec.Build:
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
                    service_networks = service_data.networks.root
                elif type(service_data.networks) is dict:
                    service_networks = list(service_data.networks.keys())

            service_extends: Optional[Extends] = None
            if service_data.extends is not None:
                # https://github.com/compose-spec/compose-spec/blob/master/spec.md#extends
                # The value of the extends key MUST be a dictionary.
                assert type(service_data.extends) is spec.Extends
                service_extends = Extends(
                    service_name=service_data.extends.service, from_file=service_data.extends.file
                )

            service_ports: List[Port] = []
            if service_data.ports is not None and not self.no_ports:
                for port_data in service_data.ports:
                    host_ip: Optional[str] = None
                    host_port: Optional[str] = None
                    container_port: Optional[str] = None
                    protocol: Optional[str] = None
                    app_protocol: Optional[str] = None

                    if type(port_data) is float:
                        container_port = str(int(port_data))
                        host_port = f"0.0.0.0:{container_port}"
                    elif type(port_data) is str:
                        regex = r"((?P<host_ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:|(\$\{([^}]+)\}):)|:|)?((?P<host_port>\d+(\-\d+)?):)?((?P<container_port>\d+(\-\d+)?))?(/(?P<protocol>\w+))?"  # noqa: E501
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
                    elif type(port_data) is spec.Ports:
                        assert port_data.target is not None, "Invalid port format, aborting."

                        if type(port_data.published) is str or type(port_data.published) is int:
                            host_port = str(port_data.published)

                        if type(port_data.target) is int:
                            container_port = str(port_data.target)

                        host_ip = port_data.host_ip
                        protocol = port_data.protocol
                        app_protocol = port_data.app_protocol

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

                    if app_protocol is None:
                        app_protocol = "na"

                    service_ports.append(
                        Port(
                            host_port=host_port,
                            container_port=container_port,
                            protocol=Protocol[protocol],
                            app_protocol=AppProtocol[app_protocol],
                        )
                    )

            service_depends_on: List[str] = []
            if service_data.depends_on is not None:
                service_depends_on = Parser._unwrap_depends_on(service_data.depends_on)

            service_volumes: List[Volume] = []
            if service_data.volumes is not None:
                for volume_data in service_data.volumes:
                    if type(volume_data) is str:
                        assert ":" in volume_data, "Invalid volume input, aborting."

                        split_data = volume_data.split(":")
                        source = self.get_source(split_data[0])
                        if len(split_data) == 2:
                            service_volumes.append(Volume(source=source, target=split_data[1]))
                        elif len(split_data) == 3:
                            service_volumes.append(
                                Volume(
                                    source=source,
                                    target=split_data[1],
                                    access_mode=split_data[2],
                                )
                            )
                    elif type(volume_data) is spec.Volumes:
                        assert volume_data.target is not None, "Invalid volume input, aborting."

                        # https://github.com/compose-spec/compose-spec/blob/master/spec.md#long-syntax-4
                        # `volume_data.source` is not applicable for a tmpfs mount.
                        if volume_data.source is None:
                            volume_data.source = volume_data.target

                        assert volume_data.source is not None
                        source = self.get_source(volume_data.source)

                        service_volumes.append(
                            Volume(
                                source=source,
                                target=volume_data.target,
                                type=VolumeType[volume_data.type],
                            )
                        )

            service_links: List[str] = []
            if service_data.links is not None:
                service_links = service_data.links

            cgroup_parent: Optional[str] = None
            if service_data.cgroup_parent is not None:
                cgroup_parent = service_data.cgroup_parent

            container_name: Optional[str] = None
            if service_data.container_name is not None:
                container_name = service_data.container_name

            env_file: List[str] = []
            if service_data.env_file is not None:
                if type(service_data.env_file.root) is str:
                    env_file = [service_data.env_file.root]
                elif type(service_data.env_file.root) is list:
                    for env_file_data in service_data.env_file.root:
                        if type(env_file_data) is str:
                            env_file.append(env_file_data)
                        elif type(env_file_data) is spec.EnvFilePath:
                            env_file.append(env_file_data.path)
                else:
                    print(f"Invalid env_file data: {service_data.env_file.root}")

            expose: List[str] = []
            if service_data.expose is not None:
                for port in service_data.expose:
                    expose.append(str(port))

            profiles: List[str] = []
            if service_data.profiles is not None:
                if type(service_data.profiles) is spec.ListOfStrings:
                    profiles = service_data.profiles.root

            devices: List[Device] = []
            if service_data.devices is not None:
                for device_data in service_data.devices:
                    if type(device_data) is str:
                        assert ":" in device_data, "Invalid volume input, aborting."

                        split_data = device_data.split(":")
                        if len(split_data) == 2:
                            devices.append(Device(host_path=split_data[0], container_path=split_data[1]))
                        elif len(split_data) == 3:
                            devices.append(
                                Device(
                                    host_path=split_data[0],
                                    container_path=split_data[1],
                                    cgroup_permissions=split_data[2],
                                )
                            )

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
                    cgroup_parent=cgroup_parent,
                    container_name=container_name,
                    env_file=env_file,
                    expose=expose,
                    profiles=profiles,
                    devices=devices,
                )
            )

        return Compose(services=services)
