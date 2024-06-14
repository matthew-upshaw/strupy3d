from strupy3d.femodel.materials import Material
from strupy3d.femodel.sections import Section

class Element:
    """
    The Element class represents a single element in the FEM system and 
    contains information about its end nodes, material, section properties,
    and identification.

    Attributes
    ----------
    id : int
        unique id for each element within the system
    material : strupy3d.materials.material.Material object
        strupy3d.materials.material.Material object containing the element's
        material type
    node_ids : tuple
        id for the node at each end of the element
    section : strupy3d.sections.section.Section object
        strupy3d.sections.section.Section object containing the element's section
        type
    """
    def __init__(self, id: int, material: Material, node_ids: tuple, section: Section):

        if not isinstance(id, int):
            raise TypeError("'id' must be an integer")
        if not isinstance(material, Material):
            raise TypeError("'material' must be a strupy3d.materials.material.Material object")
        if not self.__validate_node_ids(node_ids=node_ids):
            raise TypeError("'node_ids' must be a tuple of length 2, and each id must be an integer")
        if not isinstance(section, Section):
            raise TypeError("'section' must be a strupy3d.sections.section.Section object")
        
        self.id = id
        self.material = material
        self.node_ids = node_ids
        self.section = section

    def __str__(self) -> str:
        return f"Element {self.id} with nodes {self.node_ids}"
    
    def __validate_node_ids(self, node_ids: tuple) -> bool:
        if not isinstance(node_ids, tuple):
            return False
        if len(node_ids) != 2:
            return False
        if not all(isinstance(id, int) for id in node_ids):
            return False
        
        return True
    