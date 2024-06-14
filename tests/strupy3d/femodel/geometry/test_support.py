import pytest

from strupy3d.femodel.geometry import Support

@pytest.fixture
def valid_support():
    return Support(id=1, node_id=1, support_type=(1,1,1,0,0,0))

def test_valid_support_initialization(valid_support):
    assert valid_support.id == 1
    assert valid_support.node_id == 1
    assert valid_support.support_type == (1,1,1,0,0,0)

def test_invalid_id():
    with pytest.raises(TypeError):
        Support(id='1', node_id=1, support_type=(1,1,1,0,0,0))

def test_invalid_nodeid():
    with pytest.raises(TypeError):
        Support(id=1, node_id='1', support_type=(1,1,1,0,0,0))

def test_invalid_support_type_type():
    with pytest.raises(TypeError):
        Support(id=1, node_id=1, support_type=None)

def test_invalid_support_type_length():
    with pytest.raises(TypeError):
        Support(id=1, node_id=1, support_type=(1,1,0))

def test_invalid_support_type_component_type():
    with pytest.raises(TypeError):
        Support(id=1, node_id=1, support_type=('1','1','1','0','0','0'))

def test_invalid_support_type_component_value():
    with pytest.raises(TypeError):
        Support(id=1, node_id=1, support_type=(1,1,2,0,0,0))

def test_support_string_representation(valid_support):
    assert str(valid_support) == "Support 1: (1, 1, 1, 0, 0, 0) at node 1"
