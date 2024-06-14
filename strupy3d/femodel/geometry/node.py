class Node:
    """
    The Node class represents a single node in the FEM system and contains
    information about its location and identification.

    Attributes
    ----------
    coordinates : tuple
        (x, y, z) coordinates indicating the global location of the node
    id : int
        unique id for each node within the system
    """
    def __init__(self, id: int, coordinates: tuple):

        if not isinstance(id, int):
            raise TypeError("'id' must be an integer")
        if not self.__validate_coordinates(coordinates=coordinates):
            raise TypeError("'coordinates' must be a tuple of length 3, and each coordinate must be an integer or float")
        
        self.id: int = id
        self.coordinates: tuple = coordinates

    def __str__(self) -> str:
        return f"Node {self.id} at {self.coordinates}"
    
    def __validate_coordinates(self, coordinates: tuple) -> bool:
        if not isinstance(coordinates, tuple):
            return False
        if len(coordinates) != 3:
            return False
        if not all(isinstance(coord, (int, float)) for coord in coordinates):
            return False
        
        return True
    