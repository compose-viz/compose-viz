from typing import List, Optional

from ruamel.yaml import YAML

from compose_viz.compose import Compose, Service
from compose_viz.extends import Extends

class service_parse_rule:
    def __init__(
        self, 
        name: str, parse_path: List[str],
        target: List[str]
    ) -> None:
        self.name = name
        self.parse_path = parse_path
        self.target = target

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
        services_data = yaml_data["services"]
        services = self.parse_service_data(yaml_data["services"])

        # create Compose object
        compose = Compose(services)

        return compose

    def parse_service_data(self, services_yaml_data: List):
        services = []
        for service, service_name in zip(services_yaml_data.values(), services_yaml_data.keys()):
            
            service_image: Optional[str] = None
            if service.get("image"):
                service_image = service["image"]
            elif service.get("build"):
                service_image = "build from " + service["build"]
                

            service_networks: List[str] = []
            if service.get("networks"):
                if type(service["networks"]) is list:
                    service_networks = service["networks"]
                else:
                    service_networks = list(service["networks"].keys())
                

            service_extends: Optional[Extends] = None
            if service.get("extends"):
                service_extends = Extends(service_name=service["extends"]["service"])
                

            service_ports: List[str] = []
            if service.get("ports"):
                service_ports = service["ports"]

            service_depends_on: List[str] = []
            if service.get("depends_on"):
                service_depends_on = service["depends_on"]

            services.append(
                Service(
                    name=service_name,
                    image=service_image,
                    networks=service_networks,
                    extends=service_extends,
                    ports=service_ports,
                    depends_on=service_depends_on,
                )
            )
            # Service print debug
            #print("--------------------")
            #print("Service name: {}".format(service_name))
            #print("image: {}".format(service_image))
            #print("networks: {}".format(service_networks))
            #print("image: {}".format(service_image))
            #print("extends: {}".format(service_extends))
            #print("ports: {}".format(service_ports))
            #print("depends: {}".format(service_depends_on))


        return services
