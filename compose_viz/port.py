from enum import Enum


class Protocol(str, Enum):
    tcp = "tcp"
    udp = "udp"
    any = "any"


class Port:
    def __init__(self, host_port: str, container_port: str, protocol: Protocol = Protocol.any):
        self._host_port = host_port
        self._container_port = container_port
        self._protocol = protocol

    @property
    def host_port(self):
        return self._host_port

    @property
    def container_port(self):
        return self._container_port

    @property
    def protocol(self):
        return self._protocol
