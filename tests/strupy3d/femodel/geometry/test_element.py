import pytest

from steelpy import aisc

from strupy3d.femodel.geometry import Element
from strupy3d.femodel.materials import Material
from strupy3d.femodel.sections import Section

w12x16 = aisc.W_shapes.W12X16

steel = Material(name="A36", young_mod=29000, yield_stress=36, shear_mod=11500)
beam_section = Section(name="W12X16", area=w12x16.area, Ix=w12x16.Ix, Iy=w12x16.Iy, J=w12x16.J)

@pytest.fixture
def valid_element():
    return Element(id=1, material=steel, node_ids=(1,2), section=beam_section)

def test_valid_element_initialization(valid_element):
    assert valid_element.id == 1
    assert valid_element.material == steel
    assert valid_element.node_ids == (1,2)
    assert valid_element.section == beam_section

def test_invalid_id():
    with pytest.raises(TypeError):
        Element(id='0', material=steel, node_ids=(1,2), section=beam_section)

def test_invalid_material():
    with pytest.raises(TypeError):
        Element(id=1, material='steel', node_ids=(1,2), section=beam_section)

def test_invalid_nodeid_type():
    with pytest.raises(TypeError):
        Element(id=1, material=steel, node_ids=None, section=beam_section)

def test_invalid_nodeid_length():
    with pytest.raises(TypeError):
        Element(id=1, material=steel, node_ids=(1,2,3), section=beam_section)

def test_invalid_nodeid_component_type():
    with pytest.raises(TypeError):
        Element(id=1, material=steel, node_ids=('1','2'), section=beam_section)

def test_invalid_section():
    with pytest.raises(TypeError):
        Element(id=1, material=steel, node_ids=(1,2), section='beam_section')

def test_element_string_representation(valid_element):
    assert str(valid_element) == "Element 1 with nodes (1, 2)"