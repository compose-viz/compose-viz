from typing import List

from compose_viz.models.service import Service


class Compose:
    def __init__(self, services: List[Service]) -> None:
        self._services = services

    @property
    def services(self):
        return self._services
