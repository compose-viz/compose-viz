import pytest

from compose_viz.parser import Parser


def test_parser_error_parsing_file():
    with pytest.raises(RuntimeError, match=r"Error parsing file 'tests/in/invalid.yaml'.*"):
        Parser().parse("tests/in/invalid.yaml")


def test_parser_invalid_yaml():
    with pytest.raises(RuntimeError, match=r"Empty yaml file, aborting."):
        Parser().parse("tests/in/000000.yaml")


def test_parser_no_services_found():
    with pytest.raises(RuntimeError, match=r"No services found, aborting."):
        Parser().parse("tests/in/no-services.yaml")
