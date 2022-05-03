import os
import sys

def test_validate_input_file():
    process = os.system("docker-compose -f " + sys.argv[2] + " config -q")
    assert process == 0