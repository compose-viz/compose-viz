from typing import List, Optional

from compose_viz.models.device import Device
from compose_viz.models.extends import Extends
from compose_viz.models.port import Port
from compose_viz.models.volume import Volume


class Service:
    def __init__(
        self,
        name: str,
        image: Optional[str] = None,
        ports: List[Port] = [],
        networks: List[str] = [],
        volumes: List[Volume] = [],
        depends_on: List[str] = [],
        links: List[str] = [],
        extends: Optional[Extends] = None,
        cgroup_parent: Optional[str] = None,
        container_name: Optional[str] = None,
        devices: List[Device] = [],
        env_file: List[str] = [],
        expose: List[str] = [],
        profiles: List[str] = [],
    ) -> None:
        self._name = name
        self._image = image
        self._ports = ports
        self._networks = networks
        self._volumes = volumes
        self._depends_on = depends_on
        self._links = links
        self._extends = extends
        self._cgroup_parent = cgroup_parent
        self._container_name = container_name
        self._devices = devices
        self._env_file = env_file
        self._expose = expose
        self._profiles = profiles

    @property
    def name(self):
        return self._name

    @property
    def image(self):
        return self._image

    @property
    def ports(self):
        return self._ports

    @property
    def networks(self):
        return self._networks

    @property
    def volumes(self):
        return self._volumes

    @property
    def depends_on(self):
        return self._depends_on

    @property
    def links(self):
        return self._links

    @property
    def extends(self):
        return self._extends

    @property
    def cgroup_parent(self):
        return self._cgroup_parent

    @property
    def container_name(self):
        return self._container_name

    @property
    def devices(self):
        return self._devices

    @property
    def env_file(self):
        return self._env_file

    @property
    def expose(self):
        return self._expose

    @property
    def profiles(self):
        return self._profiles
