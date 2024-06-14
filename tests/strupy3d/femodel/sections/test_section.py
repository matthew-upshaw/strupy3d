import pytest

from strupy3d.femodel.sections import Section

@pytest.fixture
def valid_section():
    return Section(area=12, Ix=120, Iy=40, J=160, name="section")

def test_valid_section_initialization(valid_section):
    assert valid_section.area == 12
    assert valid_section.Ix == 120
    assert valid_section.Iy == 40
    assert valid_section.J == 160
    assert valid_section.name == "section"

def test_invalid_area():
    with pytest.raises(TypeError):
        Section(area=None, Ix=120, Iy=40, J=160, name="section")

def test_invalid_Ix():
    with pytest.raises(TypeError):
        Section(area=12, Ix=None, Iy=40, J=160, name="section")

def test_invalid_Iy():
    with pytest.raises(TypeError):
        Section(area=12, Ix=120, Iy=None, J=160, name="section")

def test_invalid_J():
    with pytest.raises(TypeError):
        Section(area=12, Ix=120, Iy=40, J=None, name="section")

def test_invalid_name():
    with pytest.raises(TypeError):
        Section(area=12, Ix=120, Iy=40, J=160, name=None)

def test_section_string_representation(valid_section):
    assert str(valid_section) == "section"
