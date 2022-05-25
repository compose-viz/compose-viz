import re
from typing import Dict, List, Optional

from ruamel.yaml import YAML

from compose_viz.compose import Compose, Service
from compose_viz.extends import Extends
from compose_viz.port import Port, Protocol
from compose_viz.volume import Volume, VolumeType


class Parser:
    def __init__(self):
        pass

    def parse(self, file_path: str) -> Compose:
        # load the yaml file
        with open(file_path, "r") as f:
            try:
                yaml = YAML(typ="safe", pure=True)
                yaml_data = yaml.load(f)
            except Exception as e:
                raise RuntimeError(f"Error parsing file '{file_path}': {e}")
        # validate the yaml file
        if not yaml_data:
            raise RuntimeError("Empty yaml file, aborting.")
        if not yaml_data.get("services"):
            raise RuntimeError("No services found, aborting.")

        # parse services data into Service objects
        services = self.parse_service_data(yaml_data["services"])

        # create Compose object
        compose = Compose(services)

        return compose

    def parse_service_data(self, services_yaml_data: Dict[str, dict]) -> List[Service]:
        services: List[Service] = []
        for service, service_name in zip(services_yaml_data.values(), services_yaml_data.keys()):

            service_image: Optional[str] = None
            if service.get("build"):
                if type(service["build"]) is str:
                    service_image = f"build from '{service['build']}'"
                elif type(service["build"]) is dict:
                    if service["build"].get("context") and service["build"].get("dockerfile"):
                        service_image = (
                            f"build from '{service['build']['context']}' using '{service['build']['dockerfile']}'"
                        )
                    elif service["build"].get("context"):
                        service_image = f"build from '{service['build']['context']}'"
            if service.get("image"):
                if service_image:
                    service_image += ", image: " + service["image"]
                else:
                    service_image = service["image"]

            service_networks: List[str] = []
            if service.get("networks"):
                if type(service["networks"]) is list:
                    service_networks = service["networks"]
                elif type(service["networks"]) is dict:
                    service_networks = list(service["networks"].keys())

            service_extends: Optional[Extends] = None
            if service.get("extends"):
                assert type(service["extends"]) is dict, "Invalid extends format, aborting."
                assert service["extends"]["service"], "Missing extends service, aborting."
                extend_service_name = str(service["extends"]["service"])

                extend_from_file: Optional[str] = None
                if service["extends"].get("file"):
                    assert service["extends"]["file"], "Missing extends file, aborting."
                    extend_from_file = str(service["extends"]["file"])

                service_extends = Extends(service_name=extend_service_name, from_file=extend_from_file)

            service_ports: List[Port] = []
            if service.get("ports"):
                assert type(service["ports"]) is list
                for port_data in service["ports"]:
                    if type(port_data) is dict:
                        # define a nested function to limit variable scope
                        def long_syntax():
                            assert type(port_data) is dict
                            assert port_data["target"]

                            container_port: str = str(port_data["target"])
                            host_port: str = ""
                            protocol: Protocol = Protocol.any

                            if port_data.get("published"):
                                host_port = str(port_data["published"])
                            else:
                                host_port = container_port

                            if port_data.get("host_ip"):
                                host_ip = str(port_data["host_ip"])
                                host_port = f"{host_ip}:{host_port}"
                            else:
                                host_port = f"0.0.0.0:{host_port}"

                            if port_data.get("protocol"):
                                protocol = Protocol[str(port_data["protocol"])]

                            assert host_port, "Error parsing port, aborting."

                            service_ports.append(
                                Port(
                                    host_port=host_port,
                                    container_port=container_port,
                                    protocol=protocol,
                                )
                            )

                        long_syntax()
                    elif type(port_data) is str:
                        # ports that needs to parse using regex:
                        #     - "3000"
                        #     - "3000-3005"
                        #     - "8000:8000"
                        #     - "9090-9091:8080-8081"
                        #     - "49100:22"
                        #     - "127.0.0.1:8001:8001"
                        #     - "127.0.0.1:5000-5010:5000-5010"
                        #     - "6060:6060/udp"

                        def short_syntax():
                            assert type(port_data) is str
                            regex = r"(?P<host_ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:)?((?P<host_port>\d+(\-\d+)?):)?((?P<container_port>\d+(\-\d+)?))?(/(?P<protocol>\w+))?"  # noqa: E501
                            match = re.match(regex, port_data)
                            if match:
                                host_ip: Optional[str] = match.group("host_ip")
                                host_port: Optional[str] = match.group("host_port")
                                container_port: Optional[str] = match.group("container_port")
                                protocol: Optional[str] = match.group("protocol")

                                assert container_port, "Invalid port format, aborting."

                                if container_port and not host_port:
                                    host_port = container_port

                                if host_ip:
                                    host_port = f"{host_ip}{host_port}"
                                else:
                                    host_port = f"0.0.0.0:{host_port}"

                                assert host_port, "Error while parsing port, aborting."

                                if protocol:
                                    service_ports.append(
                                        Port(
                                            host_port=host_port,
                                            container_port=container_port,
                                            protocol=Protocol[protocol],
                                        )
                                    )
                                else:
                                    service_ports.append(
                                        Port(
                                            host_port=host_port,
                                            container_port=container_port,
                                        )
                                    )

                        short_syntax()

            service_depends_on: List[str] = []
            if service.get("depends_on"):
                if type(service["depends_on"]) is list:
                    for depends_on in service["depends_on"]:
                        service_depends_on.append(str(depends_on))
                elif type(service["depends_on"]) is dict:
                    service_depends_on = list(service["depends_on"].keys())

            service_volumes: List[Volume] = []
            if service.get("volumes"):
                assert type(service["volumes"]) is list
                for volume_data in service["volumes"]:
                    if type(volume_data) is dict:
                        assert volume_data["source"] and volume_data["target"], "Invalid volume input, aborting."

                        volume_source: str = str(volume_data["source"])
                        volume_target: str = str(volume_data["target"])
                        volume_type: VolumeType = VolumeType.volume

                        if volume_data.get("type"):
                            volume_type = VolumeType[str(volume_data["type"])]

                        service_volumes.append(Volume(source=volume_source, target=volume_target, type=volume_type))
                    elif type(volume_data) is str:
                        assert ":" in volume_data, "Invalid volume input, aborting."

                        spilt_data = volume_data.split(":")
                        if len(spilt_data) == 2:
                            service_volumes.append(Volume(source=spilt_data[0], target=spilt_data[1]))
                        elif len(spilt_data) == 3:
                            service_volumes.append(
                                Volume(source=spilt_data[0], target=spilt_data[1], access_mode=spilt_data[2])
                            )

            service_links: List[str] = []
            if service.get("links"):
                service_links = service["links"]

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
            # Service print debug
            # print("--------------------")
            # print("Service name: {}".format(service_name))
            # print("image: {}".format(service_image))
            # print("networks: {}".format(service_networks))
            # print("image: {}".format(service_image))
            # print("extends: {}".format(service_extends))
            # print("ports: {}".format(service_ports))
            # print("depends: {}".format(service_depends_on))

        return services
