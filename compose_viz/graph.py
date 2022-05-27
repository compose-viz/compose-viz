from typing import Optional

import graphviz

from compose_viz.models.compose import Compose


def apply_vertex_style(type) -> dict:
    style = {
        "service": {
            "shape": "component",
        },
        "volume": {
            "shape": "folder",
        },
        "network": {
            "shape": "pentagon",
        },
        "port": {
            "shape": "circle",
        },
    }

    return style[type]


def apply_edge_style(type) -> dict:
    style = {
        "ports": {
            "style": "solid",
            "dir": "both",
        },
        "links": {
            "style": "solid",
        },
        "volumes": {
            "style": "dashed",
            "dir": "both",
        },
        "depends_on": {
            "style": "dotted",
        },
        "extends": {
            "dir": "both",
            "arrowhead": "inv",
            "arrowtail": "dot",
        },
    }

    return style[type]


class Graph:
    def __init__(self, compose: Compose, filename: str) -> None:
        self.dot = graphviz.Digraph()
        self.dot.attr("graph", background="#ffffff", pad="0.5", ratio="fill")
        self.compose = compose
        self.filename = filename

    def validate_name(self, name: str) -> str:
        # graphviz does not allow ':' in node name
        transTable = name.maketrans({":": ""})
        return name.translate(transTable)

    def add_vertex(self, name: str, type: str, lable: Optional[str] = None) -> None:
        self.dot.node(self.validate_name(name), lable, **apply_vertex_style(type))

    def add_edge(self, head: str, tail: str, type: str, lable: Optional[str] = None) -> None:
        self.dot.edge(self.validate_name(head), self.validate_name(tail), lable, **apply_edge_style(type))

    def render(self, format: str, cleanup: bool = True) -> None:
        for service in self.compose.services:
            if service.image is not None:
                self.add_vertex(service.name, "service", lable=f"{service.name}\n({service.image})")
            if service.extends is not None:
                self.add_vertex(service.name, "service", lable=f"{service.name}\n")
                self.add_edge(service.extends.service_name, service.name, "extends")
            for network in service.networks:
                self.add_vertex(network, "network", lable=f"net:{network}")
                self.add_edge(service.name, network, "links")
            for volume in service.volumes:
                self.add_vertex(volume.source, "volume")
                self.add_edge(service.name, volume.source, "volumes", lable=volume.target)
            for port in service.ports:
                self.add_vertex(port.host_port, "port", lable=port.host_port)
                self.add_edge(port.host_port, service.name, "ports", lable=port.container_port)
            for link in service.links:
                if ":" in link:
                    service_name, alias = link.split(":", 1)
                    self.add_edge(service_name, service.name, "links", alias)
                else:
                    self.add_edge(link, service.name, "links")
            for depends_on in service.depends_on:
                self.add_edge(service.name, depends_on, "depends_on")

        self.dot.render(outfile=f"{self.filename}.{format}", format=format, cleanup=cleanup)
