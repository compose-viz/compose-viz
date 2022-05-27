from enum import Enum


class VolumeType(str, Enum):
    volume = "volume"
    bind = "bind"
    tmpfs = "tmpfs"
    npipe = "npipe"


class Volume:
    def __init__(self, source: str, target: str, type: VolumeType = VolumeType.volume, access_mode: str = "rw"):
        self._source = source
        self._target = target
        self._type = type
        self._access_mode = access_mode

    @property
    def source(self):
        return self._source

    @property
    def target(self):
        return self._target

    @property
    def type(self):
        return self._type

    @property
    def access_mode(self):
        return self._access_mode
