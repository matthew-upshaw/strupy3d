class Material:
    """
    The Material class contains the relevant design information for a material
    to be used in the finite element model.

    Attributes
    ----------
    name : str
        the name of the material
    shear_mod : float
        the shear modulus of the material in ksi
    yield_stress : float
        the yield stress of the material in ksi
    young_mod : float
        the Young's Modulus of the material in ksi
    """
    def __init__(self, name: str, shear_mod: float, yield_stress: float, young_mod: float):

        if not isinstance(name, str):
            raise TypeError("'name' must be a string")
        if not isinstance(shear_mod, (int, float)):
            raise TypeError("'shear_mod' must be an integer or float")
        if not isinstance(yield_stress, (int, float)):
            raise TypeError("'yield_stress' must be an integer or float")
        if not isinstance(young_mod, (int, float)):
            raise TypeError("'young_mod' must be an integer or float")

        self.name = name
        self.shear_mod = shear_mod
        self.yield_stress = yield_stress
        self.young_mod = young_mod

    def __str__(self) -> str:
        return f"{self.name}"