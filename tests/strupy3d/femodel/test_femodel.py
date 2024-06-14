import pytest

import numpy as np
from steelpy import aisc

from strupy3d import FEModel
from strupy3d.femodel.materials import Material
from strupy3d.femodel.sections import Section

w12x16 = aisc.W_shapes.W12X16

steel = Material(name="A36", young_mod=29000, yield_stress=36, shear_mod=11500)
beam_section = Section(name="W12X16", area=w12x16.area, Ix=w12x16.Ix, Iy=w12x16.Iy, J=w12x16.J)

@pytest.fixture
def valid_femodel():
    return FEModel()

def test_valid_femodel_initialization(valid_femodel):
    assert valid_femodel.analysis_complete == False
    assert valid_femodel.analysis_ready == False
    assert valid_femodel.elements == {}
    assert valid_femodel.element_parameters == {}
    assert np.array_equal(valid_femodel.global_combined_load_matrix, np.zeros([0,0]))
    assert np.array_equal(valid_femodel.global_load_matrix, np.zeros([0,0]))
    assert np.array_equal(valid_femodel.global_stiffness_matrix, np.zeros([0,0]))
    assert valid_femodel.loads == {}
    assert valid_femodel.loaded_nodes == {}
    assert valid_femodel.nodes == {}
    assert valid_femodel.num_elements == 0
    assert valid_femodel.num_nodes == 0
    assert valid_femodel.num_supports == 0
    assert valid_femodel.supported_nodes == {}
    assert valid_femodel.supports == {}

def test_add_node(valid_femodel):
    valid_femodel.add_node(coordinates=(0,0,0))

def test_node_already_exists(valid_femodel):
    valid_femodel.add_node(coordinates=(0,0,0))
    valid_femodel.add_node(coordinates=(0,0,0))

def test_add_element(valid_femodel):
    valid_femodel.add_node(coordinates=(0,0,0))
    valid_femodel.add_node(coordinates=(12,0,0))
    valid_femodel.add_element(node_ids=(1,2), material=steel, section=beam_section)

def test_element_already_exists(valid_femodel):
    valid_femodel.add_node(coordinates=(0,0,0))
    valid_femodel.add_node(coordinates=(12,0,0))
    valid_femodel.add_element(node_ids=(1,2), material=steel, section=beam_section)
    valid_femodel.add_element(node_ids=(1,2), material=steel, section=beam_section)

def test_node_not_exists_element(valid_femodel):
    valid_femodel.add_element(node_ids=(1,2), material=steel, section=beam_section)

def test_add_or_update_load(valid_femodel):
    valid_femodel.add_node(coordinates=(0,0,0))
    valid_femodel.add_or_update_load(direction="Tx", load_case="DL", magnitude=-2.2, node_id=1)
    valid_femodel.add_or_update_load(direction="Ty", load_case="LL", magnitude=-2.2, node_id=1)

def test_node_not_exists_load(valid_femodel):
    valid_femodel.add_or_update_load(direction="Ty", load_case="LL", magnitude=-2.2, node_id=1)

def test_add_or_update_support(valid_femodel):
    valid_femodel.add_node(coordinates=(0,0,0))
    valid_femodel.add_or_update_support(node_id=1, support_type=(1,1,1,0,0,0))
    valid_femodel.add_or_update_support(node_id=1, support_type=(1,1,1,1,1,1))

def test_node_not_exists_support(valid_femodel):
    valid_femodel.add_or_update_support(node_id=1, support_type=(1,1,1,0,0,0))

def test_calculate_element_parameters(valid_femodel):
    valid_femodel.add_node(coordinates=(0,0,0))
    valid_femodel.add_node(coordinates=(12,0,0))
    valid_femodel.add_node(coordinates=(12,0,12))
    valid_femodel.add_element(node_ids=(1,2), material=steel, section=beam_section)
    valid_femodel.add_element(node_ids=(2,3), material=steel, section=beam_section)
    valid_femodel._FEModel__calculate_element_parameters()

def test_delete_node(valid_femodel):
    valid_femodel.add_node(coordinates=(0,0,0))
    valid_femodel.add_node(coordinates=(12,0,0))
    valid_femodel.add_node(coordinates=(12,0,12))
    valid_femodel.add_element(node_ids=(1,2), material=steel, section=beam_section)
    valid_femodel.add_element(node_ids=(2,3), material=steel, section=beam_section)
    valid_femodel.add_or_update_support(node_id=1, support_type=(1,1,1,0,0,0))
    valid_femodel.add_or_update_support(node_id=3, support_type=(1,1,1,1,1,1))
    valid_femodel.add_or_update_load(direction="Tx", load_case="DL", magnitude=-2.2, node_id=3)
    valid_femodel.delete_node(node_id=3)

def test_number_unrestrained_dofs(valid_femodel):
    valid_femodel.add_node(coordinates=(0,0,0))
    valid_femodel.add_node(coordinates=(12,0,0))
    valid_femodel.add_node(coordinates=(12,0,12))
    valid_femodel.add_or_update_support(node_id=1, support_type=(1,1,1,0,0,0))
    valid_femodel.add_or_update_support(node_id=3, support_type=(1,1,1,1,1,1))

    dof_array = valid_femodel._FEModel__number_unrestrained_dofs()
    ex_dof_array = np.array((
        [0,0,0,1,2,3],
        [4,5,6,7,8,9],
        [0,0,0,0,0,0],
    ))

    assert np.array_equal(dof_array, ex_dof_array)

def test_assemble_global_stiffness_matrix(valid_femodel):
    valid_femodel.add_node(coordinates=(0,0,0))
    valid_femodel.add_node(coordinates=(12,0,0))
    valid_femodel.add_node(coordinates=(12,0,12))
    valid_femodel.add_element(node_ids=(1,2), material=steel, section=beam_section)
    valid_femodel.add_element(node_ids=(2,3), material=steel, section=beam_section)
    valid_femodel.add_or_update_support(node_id=1, support_type=(1,1,1,0,0,0))
    valid_femodel.add_or_update_support(node_id=3, support_type=(1,1,1,1,1,1))

    valid_femodel._FEModel__assemble_global_stiffness_matrix(dof_array=valid_femodel._FEModel__number_unrestrained_dofs())

def test_assemble_global_load_matrix(valid_femodel):
    valid_femodel.add_node(coordinates=(0,0,0))
    valid_femodel.add_node(coordinates=(12,0,0))
    valid_femodel.add_node(coordinates=(12,0,12))
    valid_femodel.add_element(node_ids=(1,2), material=steel, section=beam_section)
    valid_femodel.add_element(node_ids=(2,3), material=steel, section=beam_section)
    valid_femodel.add_or_update_support(node_id=1, support_type=(1,1,1,0,0,0))
    valid_femodel.add_or_update_support(node_id=3, support_type=(1,1,1,1,1,1))
    valid_femodel.add_or_update_load(direction="Tz", load_case="DL", magnitude=-5, node_id=2)

    valid_femodel._FEModel__assemble_global_load_matrix(dof_array=valid_femodel._FEModel__number_unrestrained_dofs())

def test_prepare_analysis(valid_femodel):
    valid_femodel.add_node(coordinates=(0,0,0))
    valid_femodel.add_node(coordinates=(12,0,0))
    valid_femodel.add_node(coordinates=(12,0,12))
    valid_femodel.add_element(node_ids=(1,2), material=steel, section=beam_section)
    valid_femodel.add_element(node_ids=(2,3), material=steel, section=beam_section)
    valid_femodel.add_or_update_support(node_id=1, support_type=(1,1,1,0,0,0))
    valid_femodel.add_or_update_support(node_id=3, support_type=(1,1,1,1,1,1))
    valid_femodel.add_or_update_load(direction="Tz", load_case="DL", magnitude=-5, node_id=2)

    valid_femodel.prepare_analysis()

    assert valid_femodel.global_stiffness_matrix.shape == (9,9)
    assert valid_femodel.global_load_matrix.shape == (9,7)
    assert np.array_equal(valid_femodel.global_combined_load_matrix, np.zeros([0,0]))

def test_prepare_analysis_asd(valid_femodel):
    valid_femodel.add_node(coordinates=(0,0,0))
    valid_femodel.add_node(coordinates=(12,0,0))
    valid_femodel.add_node(coordinates=(12,0,12))
    valid_femodel.add_element(node_ids=(1,2), material=steel, section=beam_section)
    valid_femodel.add_element(node_ids=(2,3), material=steel, section=beam_section)
    valid_femodel.add_or_update_support(node_id=1, support_type=(1,1,1,0,0,0))
    valid_femodel.add_or_update_support(node_id=3, support_type=(1,1,1,1,1,1))
    valid_femodel.add_or_update_load(direction="Tz", load_case="DL", magnitude=-5, node_id=2)

    valid_femodel.prepare_analysis(combination_type='asd')

    assert valid_femodel.global_stiffness_matrix.shape == (9,9)
    assert valid_femodel.global_load_matrix.shape == (9,7)
    assert valid_femodel.global_combined_load_matrix.shape == (9,16)

def test_prepare_analysis_lrfd(valid_femodel):
    valid_femodel.add_node(coordinates=(0,0,0))
    valid_femodel.add_node(coordinates=(12,0,0))
    valid_femodel.add_node(coordinates=(12,0,12))
    valid_femodel.add_element(node_ids=(1,2), material=steel, section=beam_section)
    valid_femodel.add_element(node_ids=(2,3), material=steel, section=beam_section)
    valid_femodel.add_or_update_support(node_id=1, support_type=(1,1,1,0,0,0))
    valid_femodel.add_or_update_support(node_id=3, support_type=(1,1,1,1,1,1))
    valid_femodel.add_or_update_load(direction="Tz", load_case="DL", magnitude=-5, node_id=2)

    valid_femodel.prepare_analysis(combination_type='lrfd')

    assert valid_femodel.global_stiffness_matrix.shape == (9,9)
    assert valid_femodel.global_load_matrix.shape == (9,7)
    assert valid_femodel.global_combined_load_matrix.shape == (9,16)

def test_invalid_prepare_analysis_combination_type(valid_femodel):
    valid_femodel.add_node(coordinates=(0,0,0))
    valid_femodel.add_node(coordinates=(12,0,0))
    valid_femodel.add_node(coordinates=(12,0,12))
    valid_femodel.add_element(node_ids=(1,2), material=steel, section=beam_section)
    valid_femodel.add_element(node_ids=(2,3), material=steel, section=beam_section)
    valid_femodel.add_or_update_support(node_id=1, support_type=(1,1,1,0,0,0))
    valid_femodel.add_or_update_support(node_id=3, support_type=(1,1,1,1,1,1))
    valid_femodel.add_or_update_load(direction="Tz", load_case="DL", magnitude=-5, node_id=2)

    with pytest.raises(TypeError):
        valid_femodel.prepare_analysis(combination_type=None)

def test_invalid_prepare_analysis_combination_value(valid_femodel):
    valid_femodel.add_node(coordinates=(0,0,0))
    valid_femodel.add_node(coordinates=(12,0,0))
    valid_femodel.add_node(coordinates=(12,0,12))
    valid_femodel.add_element(node_ids=(1,2), material=steel, section=beam_section)
    valid_femodel.add_element(node_ids=(2,3), material=steel, section=beam_section)
    valid_femodel.add_or_update_support(node_id=1, support_type=(1,1,1,0,0,0))
    valid_femodel.add_or_update_support(node_id=3, support_type=(1,1,1,1,1,1))
    valid_femodel.add_or_update_load(direction="Tz", load_case="DL", magnitude=-5, node_id=2)

    with pytest.raises(ValueError):
        valid_femodel.prepare_analysis(combination_type='invalid')        


