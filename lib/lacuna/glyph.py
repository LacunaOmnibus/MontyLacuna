
class Glyph():
    """ Glyph base class """
    def __init__( self, client, mydict:dict, *args, **kwargs ):
        self.client = client
        for k, v in mydict.items():
            setattr(self, k, v)

class OwnedGlyph(Glyph):
    """ A glyph available on your planet.

    Attributes:
        type        "bauxite"
        quantity    23
    """

