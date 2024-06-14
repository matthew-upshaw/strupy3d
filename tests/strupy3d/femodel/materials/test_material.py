import pytest

from strupy3d.femodel.materials import Material

@pytest.fixture
def valid_material():
    return Material(name="A36", shear_mod=11500, yield_stress=36, young_mod=29000)

def test_valid_material_initialization(valid_material):
    assert valid_material.name == "A36"
    assert valid_material.shear_mod == 11500
    assert valid_material.yield_stress == 36
    assert valid_material.young_mod == 29000

def test_invalid_name():
    with pytest.raises(TypeError):
        Material(name=None, shear_mod=11500, yield_stress=36, young_mod=29000)

def test_invalid_shearmod():
    with pytest.raises(TypeError):
        Material(name="A36", shear_mod=None, yield_stress=36, young_mod=29000)

def test_invalid_yieldstress():
    with pytest.raises(TypeError):
        Material(name="A36", shear_mod=11500, yield_stress=None, young_mod=29000)

def test_invalid_youngmod():
    with pytest.raises(TypeError):
        Material(name="A36", shear_mod=11500, yield_stress=36, young_mod=None)

def test_material_string_representation(valid_material):
    assert str(valid_material) == "A36"
