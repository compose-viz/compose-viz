from typing import List


class Service:
    def __init__(self, name: str, image: str, ports: List[str] = [], networks: List[str] = [], volumes: List[str] = [], depends_on: List[str] = [], links: List[str] = [], extends: List[str] = []) -> None:
        self.name = name
        self.image = image
        self.ports = ports
        self.networks = networks
        self.volumes = volumes
        self.depends_on = depends_on
        self.links = links
        self.extends = extends
