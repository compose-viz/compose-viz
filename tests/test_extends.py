import pytest

from compose_viz.extends import Extends


def test_extend_init():
    try:
        Extends(service_name="frontend", from_file="tests/in/000001.yaml")
        Extends(service_name="frontend")

        assert True
    except Exception as e:
        assert False, e

    with pytest.raises(TypeError):
        Extends(from_file="tests/in/000001.yaml")  # type: ignore
