from typing import Optional


class Device:
    def __init__(self, host_path: str, container_path: str, cgroup_permissions: Optional[str] = None):
        self._host_path = host_path
        self._container_path = container_path
        self._cgroup_permissions = cgroup_permissions

    @property
    def host_path(self):
        return self._host_path

    @property
    def container_path(self):
        return self._container_path

    @property
    def cgroup_permissions(self):
        return self._cgroup_permissions
