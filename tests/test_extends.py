import pytest

from compose_viz.extends import Extends


def test_extend_init_normal() -> None:
    try:
        e = Extends(service_name="frontend", from_file="tests/ymls/others/empty.yaml")

        assert e.service_name == "frontend"
        assert e.from_file == "tests/ymls/others/empty.yaml"
    except Exception as e:
        assert False, e


def test_extend_init_without_from_file() -> None:
    try:
        e = Extends(service_name="frontend")

        assert e.service_name == "frontend"
        assert e.from_file is None
    except Exception as e:
        assert False, e


def test_extend_init_without_service_name() -> None:
    with pytest.raises(TypeError):
        Extends(from_file="tests/ymls/others/empty.yaml")  # type: ignore
