class Section:
    """
    The Section class contains relevant design information for the section to
    be used in the finite element model.

    Attributes
    ----------
    area : float
        the cross-sectional area of the section in in^2
    Ix : float
        the moment of inertia of the section about its x-x axis in in^4
    Iy : float
        the moment of inertia of the section about its y-y axis in in^4
    J : float
        the polar moment of inertia of the section in in^4
    name : str
        the name of the section
    """
    def __init__(self, area: float, Ix: float, Iy: float, J: float, name: str):

        if not isinstance(area, (int, float)):
            raise TypeError("'area' must be an integer or float")
        if not isinstance(Ix, (int, float)):
            raise TypeError("'Ix' must be an integer or float")
        if not isinstance(Iy, (int, float)):
            raise TypeError("'Iy' must be an integer or float")
        if not isinstance(J, (int, float)):
            raise TypeError("'J' must be an integer or float")
        if not isinstance(name, str):
            raise TypeError("'name' must be a string")

        self.area = area
        self.Ix = Ix
        self.Iy = Iy
        self.J = J
        self.name = name

    def __str__(self) -> str:
        return f"{self.name}"