import pytest

from compose_viz.extends import Extends
from compose_viz.service import Service


def test_extend_init():
    try:
        Extends(service_name="frontend", from_file="tests/in/000001.yaml")
        Extends(service_name="frontend")

        assert True
    except Exception as e:
        assert False, e

    with pytest.raises(TypeError):
        Extends(from_file="tests/in/000001.yaml")  # type: ignore


def test_service_init():
    with pytest.raises(ValueError, match=r"Both image and extends are not defined in service 'frontend', aborting."):
        Service(name="frontend")

    with pytest.raises(
        ValueError, match=r"Only one of image and extends can be defined in service 'frontend', aborting."
    ):
        Service(
            name="frontend", image="image", extends=Extends(service_name="frontend", from_file="tests/in/000001.yaml")
        )
