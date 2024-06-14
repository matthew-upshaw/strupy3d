class Load:
    """
    The Load class represents a load that is applied at a node within the FEM
    system and contains information about its id, node of application,
    magnitude, direction, and load case.

    Attributes
    ----------
    direction : str
        string indication the direction of the load; options are
        Tx, Ty, Tz, Rx, Ry, Rz
    id : int
        unique id for each load within the system
    load_case : str
        string indication of the general load case for the load; options are
        DL, LL, LLr, SL, RL, WL, EL
    magnitude : float
        magnitude for the load, either in units of kip or kip-in
    node_id : int
        id for the node at which the node is applied
    """
    LOAD_DIRECTIONS = {
        'Tx':0,
        'Ty':1,
        'Tz':2,
        'Rx':3,
        'Ry':4,
        'Rz':5,
    }

    LOAD_CASES = {
        'DL':0,
        'LL':1,
        'LLr':2,
        'SL':3,
        'RL':4,
        'WL':5,
        'EL':6,
    }

    LOAD_COMBINATIONS = {
        'ASD':[
            [1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], # 1.0DL
            [1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0], # 1.0DL + 1.0LL
            [1.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0], # 1.0DL + 1.0LLr
            [1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0], # 1.0DL + 1.0SL
            [1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0], # 1.0DL + 1.0RL
            [1.0, 0.75, 0.75, 0.0, 0.0, 0.0, 0.0], # 1.0DL + 0.75LL + 0.75LLr
            [1.0, 0.75, 0.0, 0.75, 0.0, 0.0, 0.0], # 1.0DL + 0.75LL + 0.75SL
            [1.0, 0.75, 0.0, 0.0, 0.75, 0.0, 0.0], # 1.0DL + 0.75LL + 0.75RL
            [1.0, 0.0, 0.0, 0.0, 0.0, 0.6, 0.0], # 1.0DL + 0.6WL
            [1.0, 0.75, 0.75, 0.0, 0.0, 0.45, 0.0], # 1.0DL + 0.75LL + 0.75LLr + 0.45WL
            [1.0, 0.75, 0.0, 0.75, 0.0, 0.45, 0.0], # 1.0DL + 0.75LL + 0.75SL + 0.45WL
            [1.0, 0.75, 0.0, 0.0, 0.75, 0.45, 0.0], # 1.0DL + 0.75LL + 0.75RL + 0.45WL
            [0.6, 0.0, 0.0, 0.0, 0.0, 0.6, 0.0], # 0.6DL + 0.6WL
            [1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.7], # 1.0DL + 0.7EL
            [1.0, 0.75, 0.0, 0.75, 0.0, 0.0, 0.525], # 1.0DL + 0.75LL + 0.75SL + 0.525EL
            [0.6, 0.0, 0.0, 0.0, 0.0, 0.0, 0.7], # 0.6DL + 0.7EL
        ],
        'LRFD':[
            [1.4, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], # 1.4DL
            [1.2, 1.6, 0.5, 0.0, 0.0, 0.0, 0.0], # 1.2DL + 1.6LL + 0.5LLr
            [1.2, 1.6, 0.0, 0.5, 0.0, 0.0, 0.0], # 1.2DL + 1.6LL + 0.5SL
            [1.2, 1.6, 0.0, 0.0, 0.5, 0.0, 0.0], # 1.2DL + 1.6LL + 0.5RL
            [1.2, 1.0, 1.6, 0.0, 0.0, 0.0, 0.0], # 1.2DL + 1.0LL + 1.6LLr
            [1.2, 1.0, 0.0, 1.6, 0.0, 0.0, 0.0], # 1.2DL + 1.0LL + 1.6SL
            [1.2, 1.0, 0.0, 0.0, 1.6, 0.0, 0.0], # 1.2DL + 1.0LL + 1.6RL
            [1.2, 0.0, 1.6, 0.0, 0.0, 0.5, 0.0], # 1.2DL + 1.6LLr + 0.5WL
            [1.2, 0.0, 0.0, 1.6, 0.0, 0.5, 0.0], # 1.2DL + 1.6SL + 0.5WL
            [1.2, 0.0, 0.0, 0.0, 1.6, 0.5, 0.0], # 1.2DL + 1.6RL + 0.5WL
            [1.2, 1.0, 0.5, 0.0, 0.0, 1.0, 0.0], # 1.2DL + 1.0LL + 0.5LLr + 1.0WL
            [1.2, 1.0, 0.0, 0.5, 0.0, 1.0, 0.0], # 1.2DL + 1.0LL + 0.5SL + 1.0WL
            [1.2, 1.0, 0.0, 0.0, 0.5, 1.0, 0.0], # 1.2DL + 1.0LL + 0.5RL + 1.0WL
            [0.9, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0], # 0.9DL + 1.0WL
            [1.2, 1.0, 0.0, 0.2, 0.0, 0.0, 1.0], # 1.2DL + 1.0LL + 0.2SL + 1.0EL
            [0.9, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0], # 0.9DL + 1.0EL
        ],
    }

    def __init__(self, direction: str, id: int, load_case: str, magnitude: float, node_id: int):
        
        if not isinstance(direction, str):
            raise TypeError("'direction' must be a string")
        if direction not in self.LOAD_DIRECTIONS:
            raise ValueError("'direction' must be on of: 'Tx', 'Ty', 'Tz', 'Rx', 'Ry', 'Rz'")
        if not isinstance(id, int):
            raise TypeError("'id' must be an integer")
        if not isinstance(load_case, str):
            raise TypeError("'load_case' must be a string")
        if load_case not in self.LOAD_CASES:
            raise ValueError("'load_case' must be on of: 'DL', 'LL', 'LLr', 'SL', 'RL', 'WL', 'EL'")
        if not isinstance(magnitude, (int, float)):
            raise TypeError("'magnitude' must be a float or integer")
        if not isinstance(node_id, int):
            raise TypeError("'node_id' must be an integer")
        
        self.direction = direction
        self.id = id
        self.load_case = load_case
        self.magnitude = magnitude
        self.node_id = node_id

    def __str__(self) -> str:
        return f"Load with magnitude {self.magnitude} in {self.direction} at node {self.node_id}"
    