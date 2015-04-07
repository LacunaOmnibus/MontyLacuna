
import lacuna.bc

class Glyph(lacuna.bc.SubClass):
    """ Glyph base class """

class OwnedGlyph(Glyph):
    """ A single specific glyph on your planet.

    Object Attributes::

        id          12345,
        name        "bauxite"
        type        "bauxite"
        quantity    23

    name and type are always the same.  There's no longer such a thing as an 
    individual glyph, only types of glyphs, which is why we have both an ID 
    and a quantity.
    """

class AssembledArtifact(Glyph):
    """ One or more artifacts created by assembling glyphs.

    Object Attributes::
        
        item_name   "Halls of Vrbansk"
        quantity    10
    """
    def __init__(self, client, name:str, quan:int):
        self.client     = client
        self.item_name  = name
        self.quantity   = quan


