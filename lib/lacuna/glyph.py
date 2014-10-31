
class Glyph():
    """ Glyph base class """
    def __init__( self, client, mydict:dict, *args, **kwargs ):
        self.client = client
        for k, v in mydict.items():
            setattr(self, k, v)

class OwnedGlyph(Glyph):
    """ A single specific glyph on your planet.

    Attributes:
        id          12345,
        name        "bauxite"
        type        "bauxite"
        quantity    23

    name and type are always the same.  There's no longer such a thing as an 
    individual glyph, only types of glyphs, which is why we have both an ID 
    and a quantity.
    """

