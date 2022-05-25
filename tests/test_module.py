import os


def test_module():
    assert os.system("python -m compose_viz") == 0
