import pytest

from compose_viz.parser import Parser


def test_parser_invalid_yaml() -> None:
    with pytest.raises(RuntimeError, match=r"Error parsing file 'tests/ymls/others/invalid.yml'.*"):
        Parser().parse("tests/ymls/others/invalid.yml")


def test_parser_empty_yaml() -> None:
    with pytest.raises(RuntimeError, match=r"Error parsing file 'tests/ymls/others/empty.yml'.*"):
        Parser().parse("tests/ymls/others/empty.yml")


def test_parser_no_services_found() -> None:
    with pytest.raises(AssertionError, match=r"No services found, aborting."):
        Parser().parse("tests/ymls/others/no-services.yml")
