class Extends:
    def __init__(self, from_file: str, service_name: str):
        self._from_file = from_file
        self._service_name = service_name

    @property
    def from_file(self):
        return self._from_file

    @property
    def service_name(self):
        return self._service_name