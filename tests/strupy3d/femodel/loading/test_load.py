import pytest

from strupy3d.femodel.loading import Load

@pytest.fixture
def valid_load():
    return Load(direction="Tx", id=1, load_case="DL", magnitude=-2.2, node_id=1)

def test_valid_load_initialization(valid_load):
    assert valid_load.direction == "Tx"
    assert valid_load.id == 1
    assert valid_load.load_case == "DL"
    assert valid_load.magnitude == -2.2
    assert valid_load.node_id == 1

def test_invalid_direction_type():
    with pytest.raises(TypeError):
        Load(direction=None, id=1, load_case='DL', magnitude=-2.2, node_id=1)

def test_invalid_direction_value():
    with pytest.raises(ValueError):
        Load(direction="x", id=1, load_case="DL", magnitude=-2.2, node_id=1)

def test_invalid_id():
    with pytest.raises(TypeError):
        Load(direction="Tx", id=None, load_case="DL", magnitude=-2.2, node_id=1)

def test_invalid_loadcase_type():
    with pytest.raises(TypeError):
        Load(direction="Tx", id=1, load_case=None, magnitude=-2.2, node_id=1)

def test_invalid_loadcase_value():
    with pytest.raises(ValueError):
        Load(direction="Tx", id=1, load_case="dead", magnitude=-2.2, node_id=1)

def test_invalid_magnitude():
    with pytest.raises(TypeError):
        Load(direction="Tx", id=1, load_case="DL", magnitude=None, node_id=1)

def test_invalid_nodeid():
    with pytest.raises(TypeError):
        Load(direction="Tx", id=1, load_case="DL", magnitude=-2.2, node_id=None)

def test_load_string_representation(valid_load):
    assert str(valid_load) == "Load with magnitude -2.2 in Tx at node 1"
