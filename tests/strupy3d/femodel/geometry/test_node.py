import pytest

from strupy3d.femodel.geometry import Node

@pytest.fixture
def valid_node():
    return Node(id=1, coordinates=(0,0,0))

def test_valid_node_initialization(valid_node):
    assert valid_node.id == 1
    assert valid_node.coordinates == (0,0,0)

def test_invalid_id():
    with pytest.raises(TypeError):
        Node(id='1', coordinates=(1,1,1))

def test_invalid_coordinates_type():
    with pytest.raises(TypeError):
        Node(id=1, coordinates=None)

def test_invalid_coordinates_length():
    with pytest.raises(TypeError):
        Node(id=1, coordinates=(0,0))

def test_invalid_coordinates_component_type():
    with pytest.raises(TypeError):
        Node(id=1, coordinates=('0','0','0'))

def test_node_string_representation(valid_node):
    assert str(valid_node) == "Node 1 at (0, 0, 0)"