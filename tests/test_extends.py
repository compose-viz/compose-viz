import pytest
from compose_viz.service import Service
    
def test_parse_file():
    with pytest.raises(ValueError, match=r"Both image and extends are not defined in service 'frontend', aborting."):
        Service(name='frontend')
