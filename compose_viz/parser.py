from re import S
from compose_viz.compose import Compose
from compose_viz.compose import Service
from ruamel.yaml import YAML


class Parser:
    def __init__(self):
        pass

    def parse(self, file_path: str) -> Compose:
        # validate input file using `docker-compose config -q sys.argv[1]` first
        # load the yaml file
        with open(file_path, "r") as f:
            try:
                yaml = YAML(typ='safe', pure=True)
                yaml_data = yaml.load(f)
            except YAML.YAMLError as exc:
                raise YAML.YAMLError
        # validate the yaml file
        if not yaml_data:
            print("Error: empty yaml file")
            raise ValueError
        if not yaml_data.get("services"):
            print("Error: no services found")
            raise ValueError
        # parse services data into Service objects
        services_data = yaml_data["services"]
        services = []
        for service, service_name in zip(services_data.values(), services_data.keys()):
            #print("name: {}".format(service_name))
            if service.get("image"):
                service_image = service["image"]
                #print("image: {}".format(service_image))
            if service.get("networks"):
                if(type(service["networks"]) is list):
                    service_networks = service["networks"]
                else:
                    service_networks = list(service["networks"].keys())
                #print("networks: {}".format(service_networks))
            services.append(Service(
                name=service_name,
                image=service_image,
                networks=service_networks,
            ))
        # create Compose object
        compose = Compose(services)

        return compose
