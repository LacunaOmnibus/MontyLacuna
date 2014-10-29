
class Plan():
    """ Plan base class """
    def __init__( self, client, mydict:dict, *args, **kwargs ):
        self.client = client
        for k, v in mydict.items():
            setattr(self, k, v)

class OwnedPlan(Plan):
    """ Returned from viewing plans you currently own, as in your PCC.

    Attributes:
        name                "Interstellar Broadcast System"
        level               1
        extra_build_level   5
        quantity            23
    """

class PotentialSSPlan(Plan):
    """ Returned from viewing plans you can build, as in your Space Station Lab
    (A).

    Attributes:
        name                "Interstellar Broadcast System"
        type                "ibs"
        image               "ibs"
        url                 "/ibs"
    """

class LevelCosts(Plan):
    """ Not a plan at all, but the costs associated with creating a plan at your 
    SS Lab.

    Attributes:
        level   1,
        food    10000
        ore     10000
        water   10000
        energy  10000
        waste   2500
        time    1200 (in seconds)
    """
