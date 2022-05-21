from enum import Enum


class VolumeType(str, Enum):
    volume = "volume"
    bind = "bind"
    tmpfs = "tmpfs"


class Volume:
    def __init__(self, source: str, target: str, type: VolumeType = VolumeType.volume):
        self._source = source
        self._target = target
        self._type = type

    @property
    def source(self):
        return self._source

    @property
    def target(self):
        return self._target

    @property
    def type(self):
        return self._type
