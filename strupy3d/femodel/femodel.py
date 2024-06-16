import math
import numpy as np
from scipy.sparse import lil_matrix
from scipy.sparse.linalg import spsolve

from .geometry import (
    Element,
    Node,
    Support,
)

from .loading import (
    Load,
)

from .materials import (
    Material,
)

from .sections import (
    Section,
)

class FEModel:
    """
    The FEModel object creates and analyzes the 3d finite element model.

    Attributes
    ----------
    analysis_complete : bool
        indicates whether the FEModel object has been successfully analyzed
    analysis_ready : bool
        indicates whether the FEModel object is ready to be analyzed
    displacement_vectors : numpy.ndarray
        numpy.ndarray representing the displacement vector for each load case
        or load combination as applicable
    elements : dict
        dictionary of strupy3d.geometry.element.Element objects in the FEModel
        object with element id's as keys
    element_parameters : dict
        dictionary holding the length, local stiffness matrix, and tranformation
        matrix for each element, with element id's as keys
    global_combined_load_matrix : numpy.ndarray
        numpy.ndarray representing the global load matrix, with load factors
        applied, for the finite element model where each column represents a
        load combination
    global_load_matrix : numpy.ndarray
        numpy.ndarray representing the global load matrix for the finite
        element model where each column represents a load case
    global_stiffness_matrix : numpy.ndarray
        numpy.ndarray representing the global stiffness matrix for the finite
        finite element model
    loads : dict
        dictionary of strupy3d.loading.load.Load objects in the FEModel object
        with load id's as keys
    loaded_nodes : dict
        dictionary of nodes that are designated as having a load applied to them
        with node id's as keys and load id's as values
    nodes : dict
        dictionary of strupy3d.geometry.node.Node objects in the FEModel object
        with node id's as keys
    num_elements : int
        number of elements added to the FEModel object
    num_loads : int
        number of loads added to the FEModel object
    num_nodes : int
        number of nodes added to the FEModel object
    num_supports : int
        number of supports added to the FEModel object
    supported_nodes : dict
        dictionary of nodes that are designated as supports with node id's as
        keys and support id's as values
    supports : dict
        dictionary of strupy3d.geometry.support.Support objects in the FEModel
        object with support id's as keys

    Methods
    -------
    add_element(node_ids, material, section)
        Adds an element to the finite element model.
    add_or_update_load(direction, load_case, magnitude, node_id)
        Adds a load to the finite element model.
    add_node(coordinates)
        Adds a node to the finite element model
    add_or_update_support(node_id, support_type):
        Adds a suppport at the indicted node if one does not already exist or
        updates the support if one does already exist.
    delete_element(element_id)
        Deletes an element from the finite element model.
    delete_load(load_id)
        Deletes a load from the finite element model.
    delete_node(node_id)
        Deletes a node and all associated elements, loads, and supports from
        the finite element model.
    delete_support(support_id)
        Deletes a support from the finite element model.
    prepare_analysis(combination_type)
        Prepares the finite element model for analysis.
    run(combination_type)
        Runs the analysis of the finite element model.
    """
    def __init__(self):
        self.analysis_complete = False
        self.analysis_ready = False
        self.displacement_vectors = np.zeros([0,0])
        self.elements = {}
        self.element_parameters = {}
        self.global_combined_load_matrix = np.zeros([0,0])
        self.global_load_matrix = np.zeros([0,0])
        self.global_stiffness_matrix = np.zeros([0,0])
        self.loads = {}
        self.loaded_nodes = {}
        self.nodes = {}
        self.num_elements = 0
        self.num_loads = 0
        self.num_nodes = 0
        self.num_supports = 0
        self.supported_nodes = {}
        self.supports = {}

    def add_element(self, node_ids: tuple, material: Material, section: Section):
        """
        Adds an element to the finite element model.

        Parameters
        ----------
        material : strupy3d.materials.material.Material object
            strupy3d.materials.material.Material object containing the element's
            material type
        node_ids : tuple
            id for the node at each end of the element
        section : strupy3d.sections.section.Section object
            strupy3d.sections.section.Section object containing the element's
            section type
        """
        try:
            self.__validate_add_element(node_ids=node_ids)
            self.num_elements += 1
            self.elements[self.num_elements] = Element(
                id=self.num_elements,
                node_ids=node_ids,
                material=material,
                section=section,
            )

            self.analysis_complete = False
            self.analysis_ready = False
        except ValueError as e:
            print(e, "Element not added.")

    def add_or_update_load(self, direction: str, load_case: str, magnitude: float, node_id: int):
        """
        Adds a load to the finite element model.

        Parameters
        ----------
        direction : str
            string indication the direction of the load; options are
            Tx, Ty, Tz, Rx, Ry, Rz
        load_case : str
            string indication of the general load case for the load; options are
            DL, LL, LLr, SL, RL, WL, EL
        magnitude : float
            magnitude for the load, either in units of kip or kip-in
        node_id : int
            id for the node at which the node is applied
        """
        try:
            self.__validate_add_or_update_load(node_id=node_id)
            if node_id in self.loaded_nodes.keys():
                self.loads[self.loaded_nodes[node_id]] = Load(
                    id=self.loaded_nodes[node_id],
                    direction=direction,
                    load_case=load_case,
                    magnitude=magnitude,
                    node_id=node_id,
                )
            else:
                self.num_loads += 1
                self.loads[self.num_loads] = Load(
                    id=self.num_loads,
                    direction=direction,
                    load_case=load_case,
                    magnitude=magnitude,
                    node_id=node_id,
                )

                self.loaded_nodes[node_id] = self.num_loads

                self.analysis_complete = False
                self.analysis_ready = False

        except ValueError as e:
            print(e, "Load not added.")

    def add_node(self, coordinates: tuple):
        """
        Adds a node to the finite element model.

        Parameters
        ----------
        coordinates : tuple
            (x, y, z) coordinates indicating the global location of the node
        """
        try:
            self.__validate_add_node(coordinates=coordinates)
            self.num_nodes += 1
            self.nodes[self.num_nodes] = Node(
                id=self.num_nodes,
                coordinates=coordinates
            )

            self.analysis_complete = False
            self.analysis_ready = False
        except ValueError as e:
            print(e, "Node not added.")

    def add_or_update_support(self, node_id: int, support_type: tuple):
        """
        Adds a suppport at the indicted node if one does not already exist or
        updates the support if one does already exist.

        Parameters
        ----------
        node_id : int
            the id of the strupy3d.geometry.node.Node object that will be designated
            as a support node
        support_type : tuple
            tuple indicating the type of support; the tuple represents restrained
            degrees of freedom as (Tx, Ty, Tz, Rx, Ry, Rz) where a 1 indicates the 
            degree of freedom is restrained and a 0 indicates it is unrestrained
        """
        try:
            self.__validate_add_or_update_support(node_id=node_id)
            if node_id in self.supported_nodes.keys():
                self.supports[self.supported_nodes[node_id]].support_type = support_type
            else:
                self.num_supports += 1
                self.supports[self.num_supports] = Support(
                    id=self.num_supports,
                    node_id=node_id,
                    support_type=support_type,
                )

                self.supported_nodes[node_id] = self.num_supports
            
            self.analysis_complete = False
            self.analysis_ready = False
        except ValueError as e:
            print(e, "Support not added.")

    def delete_element(self, element_id: int):
        """
        Deletes an element from the finite element model.

        Parameters
        ----------
        element_id : int
            unique id of the element to be deleted
        """
        if element_id in self.elements:
            _ = self.elements.pop(element_id)

            self.analysis_complete = False
            self.analysis_ready = False

    def delete_load(self, load_id: int):
        """
        Deletes a load from the finite element model.

        Parameters
        ----------
        load_id : int
            unique id of the load to be deleted
        """
        if load_id in self.loads:
            _ = self.loads.pop(load_id)
            self.loaded_nodes = { k:v for k,v in self.loaded_nodes.items() if v != load_id }

            self.analysis_complete = False
            self.analysis_ready = False

    def delete_node(self, node_id: int):
        """
        Deletes a node from the finite element model.

        Parameters
        ----------
        node_id : int
            unique id for the node to be deleted
        """
        if node_id in self.nodes:
            # Delete any elements associated with the node
            elements_to_delete = [element_id for element_id, element in self.elements.items() if node_id in element.node_ids]
            for element_id in elements_to_delete:
                self.delete_element(element_id=element_id)

            # Delete any loads associated with the node
            if node_id in self.loaded_nodes:
                self.delete_load(load_id=self.loaded_nodes[node_id])

            # Delete any supports associated with the node
            if node_id in self.supported_nodes:
                self.delete_support(support_id=self.supported_nodes[node_id])

            # Delete the node
            _ = self.nodes.pop(node_id)

            self.analysis_complete = False
            self.analysis_ready = False

    def delete_support(self, support_id: int):
        """
        Deletes a support from the finite element model.

        Parameters
        ----------
        support_id : int
            unique id of the support to be deleted
        """
        if support_id in self.supports:
            _ = self.supports.pop(support_id)
            self.supported_nodes = { k:v for k,v in self.supported_nodes.items() if v!= support_id }

            self.analysis_complete = False
            self.analysis_ready = False

    def prepare_analysis(self, combination_type: str='None'):
        """
        Prepares the finite element model for analysis.

        Parameters
        ----------
        combination_type : str, optional
            string representing the load combinations that should be used;
            options are 'ASD', 'LRFD', and 'None'; default = 'None'
        """
        if not isinstance(combination_type, str):
            raise TypeError("'combination_type' must be a string")
        if combination_type.upper() not in ["NONE", "ASD", "LRFD",]:
            raise ValueError("'combination_type' must be 'ASD', 'LRFD', or 'None'")
        
        dof_array = self.__number_unrestrained_dofs()
        self.global_stiffness_matrix = self.__assemble_global_stiffness_matrix(dof_array=dof_array)
        self.global_load_matrix = self.__assemble_global_load_matrix(dof_array=dof_array)

        if combination_type != "None":
            self.global_combined_load_matrix = self.__apply_load_factors(load_matrix=self.global_load_matrix, combination_type=combination_type.upper())

        self.analysis_ready = True

    def run(self, combination_type: str="None"):
        """
        Runs the analysis for the finite element model.

        Parameters
        ----------
        combination_type : str, optional
            string representing the load combinations that should be used;
            options are 'ASD', 'LRFD', and 'None'; default = 'None'
        """
        self.prepare_analysis(combination_type=combination_type)

        load_matrix = self.global_load_matrix

        if combination_type != "None":
            load_matrix = np.hstack((load_matrix, self.global_combined_load_matrix))

        num_lcs = load_matrix.shape[1]
        displacement_vectors = np.zeros_like(load_matrix)

        for i_lc in range(num_lcs):
            displacement_vectors[:,i_lc] = spsolve(self.global_stiffness_matrix, load_matrix[:,i_lc])

        self.displacement_vectors = displacement_vectors

        self.analysis_complete = True

    def __apply_load_factors(self, load_matrix: np.ndarray, combination_type: str) -> np.ndarray:
        """
        Applies either the ASD or LRFD load factors, as specified by the user,
        to the global load matrix.

        Parameters
        ----------
        load_matrix : numpy.ndarray
            numpy.ndarray representing the global load matrix
        combination_type : str
            string representing the combination type that should be applied;
            either 'ASD' or 'LRFD'

        Returns
        -------
        combined_load_matrix : numpy.ndarray
            numpy.ndarray representing the global combined load matrix
        """
        load_factors = np.array(Load.LOAD_COMBINATIONS[combination_type])

        combined_load_matrix = load_matrix @ load_factors.T

        return combined_load_matrix

    def __assemble_global_load_matrix(self, dof_array: np.ndarray) -> np.ndarray:
        """
        Assembles the global load matrix for the finite element model.

        Parameters
        ----------
        dof_array : numpy.ndarray
            numpy.ndarray containing the unrestrained dof number for each dof
            in each node

        Returns
        -------
        Pg : numpy.ndarray
            numpy.ndarray representing the global load matrix for the fintite
            element model
        """
        num_dofs = dof_array.max()
        num_load_cases = len(Load.LOAD_CASES)

        Pg = np.zeros((num_dofs, num_load_cases))

        for _, load in self.loads.items():
            node_id = load.node_id
            direction_id = Load.LOAD_DIRECTIONS[load.direction]
            magnitude = load.magnitude
            load_case_id = Load.LOAD_CASES[load.load_case]

            global_dof = dof_array[node_id-1, direction_id]

            if global_dof > 0:
                Pg[global_dof-1, load_case_id] += magnitude

        return Pg

    def __assemble_global_stiffness_matrix(self, dof_array: np.ndarray) -> np.ndarray:
        """
        Assembles the global stiffness matrix for the finite element model.

        Returns
        -------
        Kg : numpy.ndarray
            numpy.ndarray representing the global stiffness matrix for the
            finite element model
        """
        num_dofs = dof_array.max()

        self.__calculate_element_parameters()

        Kg = lil_matrix((num_dofs, num_dofs))

        for element_id, element in self.elements.items():
            kl = self.element_parameters[element_id]['kl']
            tm = self.element_parameters[element_id]['tm']

            kg = tm.T @ kl @ tm
            node_ids = element.node_ids

            local_dofs = []
            for node_id in node_ids:
                local_dofs.extend(dof_array[node_id-1].tolist())

            local_dofs = [dof for dof in local_dofs if dof > 0]

            for local_i, global_i in enumerate(local_dofs):
                for local_j, global_j in enumerate(local_dofs):
                    Kg[global_i-1, global_j-1] += kg[local_i, local_j]

        return Kg.tocsc()
        

    def __calculate_element_parameters(self):
        """
        Calculates the length, local stiffness matrix, and local transformation
        matrix for each element in the finite element model.
        """
        self.element_parameters = {}
        for element_id, element in self.elements.items():
            cur_element = {}
            node_i = np.array(self.nodes[element.node_ids[0]].coordinates)
            node_j = np.array(self.nodes[element.node_ids[1]].coordinates)

            cur_element['length'] = math.sqrt(sum((node_j-node_i)**2))
            cur_element['kl'] = self.__calculate_local_stiffness_matrix(element=element)
            cur_element['tm'] = self.__calculate_local_transformation_matrix(element=element)

            self.element_parameters[element_id] = cur_element

    def __calculate_local_stiffness_matrix(self, element: Element) -> np.ndarray:
        """
        Calculates the local stiffness matrix for the input element.

        Parameters
        ----------
        element : strupy3d.geometry.element.Element
            strupy3d.geometry.element.Element object for which the local
            stiffness matrix should be calculated

        Returns
        -------
        local_k : numpy.ndarray
            numpy.ndarray containing the element local stiffness matrix
        """
        node_i = np.array(self.nodes[element.node_ids[0]].coordinates)
        node_j = np.array(self.nodes[element.node_ids[1]].coordinates)

        L = math.sqrt(sum((node_j-node_i)**2))

        E = element.material.young_mod
        G = element.material.shear_mod

        A = element.section.area
        Izz = element.section.Ix
        Iyy = element.section.Iy
        Ip = element.section.J

        local_k = np.zeros([12, 12])

        local_k[0,0] = E*A/L
        local_k[0,6] = -E*A/L

        local_k[1,1] = 12*E*Izz/L**3
        local_k[1,5] = 6*E*Izz/L**2
        local_k[1,7] = -12*E*Izz/L**3
        local_k[1,11] = 6*E*Izz/L**2

        local_k[2,2] = 12*E*Iyy/L**3
        local_k[2,4] = -6*E*Iyy/L**2
        local_k[2,8] = -12*E*Iyy/L**3
        local_k[2,10] = -6*E*Iyy/L**2

        local_k[3,3] = G*Ip/L
        local_k[3,9] = -G*Ip/L

        local_k[4,4] = 4*E*Iyy/L
        local_k[4,8] = 6*E*Iyy/L**2
        local_k[4,10] = 2*E*Iyy/L

        local_k[5,5] = 4*E*Izz/L
        local_k[5,7] = -6*E*Izz/L**2
        local_k[5,11] = 2*E*Izz/L

        local_k[6,6] = E*A/L

        local_k[7,7] = 12*E*Izz/L**3
        local_k[7,11] = -6*E*Izz/L**2

        local_k[8,8] = 12*E*Iyy/L**3
        local_k[8,10] = 6*E*Iyy/L**2

        local_k[9,9] = G*Ip/L

        local_k[10,10] = 4*E*Iyy/L

        local_k[11,11] = 4*E*Izz/L

        local_k = local_k + local_k.T - np.diag(local_k.diagonal())

        return local_k
    
    def __calculate_local_transformation_matrix(self, element: Element) -> np.ndarray:
        """
        Calculates the local tranformation matrix for the input element.

        Parameters
        ----------
        element : strupy3d.geometry.element.Element
            strupy3d.geometry.element.Element object for which the local
            stiffness matrix should be calculated

        Returns
        -------
        local_t : numpy.ndarray
            numpy.ndarray containing the element local stiffness matrix        
        """
        node_i = np.array(self.nodes[element.node_ids[0]].coordinates)
        node_j = np.array(self.nodes[element.node_ids[1]].coordinates)

        L = math.sqrt(sum((node_j-node_i)**2))

        ix, iy, iz = node_i
        jx, jy, jz = node_j

        local_t = np.zeros([12,12])

        if math.isclose(abs(jx-ix), 0, abs_tol=1e-6) and math.isclose(abs(jy-iy), 0, abs_tol=1e-6):
            i_offset = np.array([ix-1, iy, iz])
            j_offset = np.array([jx-1, jy, jz])
        else:
            i_offset = np.array([ix, iy, iz+1])
            j_offset = np.array([jx, jy, jz+1])
        node_k = i_offset + 0.5*(j_offset-i_offset)

        local_x_vector = node_j - node_i
        local_x_unit = local_x_vector/L

        vector_in_plane = node_k - node_i
        local_y_vector = vector_in_plane - np.dot(vector_in_plane, local_x_unit)*local_x_unit
        mag_y_vector = math.sqrt(sum(local_y_vector**2))
        local_y_unit = local_y_vector/mag_y_vector

        local_z_unit = np.cross(local_x_unit, local_y_unit)

        rotation_matrix = np.array([local_x_unit, local_y_unit, local_z_unit]).T

        local_t[0:3, 0:3] = rotation_matrix.T
        local_t[3:6, 3:6] = rotation_matrix.T
        local_t[6:9, 6:9] = rotation_matrix.T
        local_t[9:12, 9:12] = rotation_matrix.T

        return local_t
            
    def __number_unrestrained_dofs(self) -> np.ndarray:
        """
        Creates an array that holds the unrestrained dof number for each dof
        in each node

        Parameters
        ----------
        None

        Returns
        -------
        dof_array : numpy.ndarray
            numpy.ndarray containing the unrestrained dof number for each dof
            in each node
        """
        dof_array = np.ones((len(self.nodes),6), dtype=int)

        for node, support_id in self.supported_nodes.items():
            dof_array[node-1] = 1 - np.array(self.supports[support_id].support_type)

        dof_array = dof_array*np.cumsum(dof_array.flatten()).reshape((len(self.nodes),6))

        return dof_array

    def __validate_add_element(self, node_ids: tuple):
        """
        Validates the new node to be added by ensuring that an element between
        the specified nodes does not already exist.

        Parameters
        ----------
        node_ids : tuple
            id for the node at each end of the element
        """
        for element_id in self.elements:
            if node_ids == self.elements[element_id].node_ids:
                raise ValueError(f"Element already exists between nodes {node_ids[0]} and {node_ids[1]}!")
            
        for node in node_ids:
            if node not in self.nodes:
                raise ValueError(f"Node with id {node} does not exist!")
            
    def __validate_add_or_update_load(self, node_id: int):
        """
        Validates the load to be added by ensuring that the node to which the
        load is to be added exists.

        Parameters
        ----------
        node_id : int
            id for the node at which the load is to be added or updated
        """
        if node_id not in self.nodes:
            raise ValueError(f"Node with id {node_id} does not exist!")

    def __validate_add_node(self, coordinates: tuple):
        """
        Validates the new node to be added by ensuring that a node at the
        specified coordinates does not already exist.

        Parameters
        ----------
        coordinates : tuple
            (x, y, z) coordinates indicating the global location of the node
        """
        for node_id in self.nodes:
            if all(np.isclose(np.asarray(coordinates), np.asarray(self.nodes[node_id].coordinates))):
                raise ValueError(f"Node already exists at {coordinates}!")
            
    def __validate_add_or_update_support(self, node_id: int):
        """
        Validates the support to be added or updated by ensuring the node to
        which the support is to be added exists.

        Parameters
        ----------
        node_id : int
            id for the node at which the load is to be added or updated
        """
        if node_id not in self.nodes:
            raise ValueError(f"Node with id {node_id} does not exist!")
            