class Support:
    """
    The Support class contains information about all supports witin the finite
    element model, including the node_id and the support type.

    Attributes
    ----------
    id : int
        the unique id of the Support object within the finite element model
    node_id : int
        the id of the strupy3d.geometry.node.Node object that will be designated
        as a support node
    support_type : tuple
        tuple indicating the type of support; the tuple represents restrained
        degrees of freedom as (Tx, Ty, Tz, Rx, Ry, Rz) where a 1 indicates the 
        degree of freedom is restrained and a 0 indicates it is unrestrained
    """
    def __init__(self, id: int, node_id: int, support_type: tuple):

        if not isinstance(id, int):
            raise TypeError("'id' must be an integer")
        if not isinstance(node_id, int):
            raise TypeError("'node_id' must be an integer")
        if not self.__validate_support_type(support_type=support_type):
            raise TypeError("'support_type' must be a tuple of length 6, and each component must be either 0 or 1")

        self.id = id
        self.node_id = node_id
        self.support_type = support_type

    def __str__(self) -> str:
        return f"Support {self.id}: {self.support_type} at node {self.node_id}"
    
    def __validate_support_type(self, support_type: tuple) -> bool:
        if not isinstance(support_type, tuple):
            return False
        if len(support_type) != 6:
            return False
        if not all(isinstance(dof, int) for dof in support_type):
            return False
        for dof in support_type:
            if dof != 0 and dof != 1:
                return False
            
        return True