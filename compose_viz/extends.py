from typing import Optional


class Extends:
    def __init__(self, service_name: str, from_file: Optional[str] = None):
        self._service_name = service_name
        self._from_file = from_file

    @property
    def service_name(self):
        return self._service_name

    @property
    def from_file(self):
        return self._from_file
