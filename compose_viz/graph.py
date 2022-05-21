import graphviz

from compose_viz.compose import Compose


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
        },
        "links": {
            "style": "solid",
        },
        "volumes": {
            "style": "dashed",
        },
        "depends_on": {
            "style": "dotted",
        },
    }

    return style[type]


class Graph:
    def __init__(self, compose: Compose, filename: str) -> None:
        self.dot = graphviz.Digraph()
        self.dot.attr("graph", background="#ffffff", pad="0.5", ratio="fill")
        self.compose = compose
        self.filename = filename

    def add_vertex(self, name: str, type: str) -> None:
        self.dot.node(name, **apply_vertex_style(type))

    def add_edge(self, head: str, tail: str, type: str) -> None:
        self.dot.edge(head, tail, **apply_edge_style(type))

    def render(self, format: str, cleanup: bool = True) -> None:
        for service in self.compose.services:
            self.add_vertex(service.name, "service")
            for network in service.networks:
                self.add_vertex("net#" + network, "network")
                self.add_edge(service.name, "net#" + network, "links")
            for volume in service.volumes:
                self.add_vertex(volume.source, "volume")
                self.add_edge(service.name, volume.source, "links")
            for port in service.ports:
                self.add_vertex(port, "port")
                self.add_edge(service.name, port, "ports")
            for depends_on in service.depends_on:
                self.dot.edge(depends_on, service.name, "depends_on")

        self.dot.render(outfile=self.filename, format=format, cleanup=cleanup)
