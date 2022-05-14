from re import S
from compose_viz.compose import Compose
from compose_viz.compose import Service
import yaml

class Parser:
    def __init__(self):
        pass

    def parse(self, file_path: str) -> Compose:
        # validate input file using `docker-compose config -q sys.argv[1]` first
        # load the yaml file
        with open(file_path, "r") as f:
            try:
                yaml_data = yaml.safe_load(f)
            except yaml.YAMLError as exc:
                raise yaml.YAMLError
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
                service_networks = service["networks"]
                #print("networks: {}".format(service_networks))
            services.append(Service(
                name=service_name,
                image=service_image,
                networks=service_networks,
            ))
        # create Compose object
        compose = Compose(services)

        return compose
