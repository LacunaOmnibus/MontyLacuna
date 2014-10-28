
""" 
Different types of ship objects have varying attributes depending on what 
state the ship is in.
"""

class Ship():
    """ Base class """
    def __init__( self, client, mydict:dict, *args, **kwargs ):
        self.client = client
        for k, v in mydict.items():
            setattr(self, k, v)

class BuildingShip(Ship):
    """ A ship being built (currently in the shipyard queue):
             id               "1234",
             type             "spy_pod",
             type_human       "Spy Pod",
             date_completed   "01 31 2010 13:09:05 +0600"
    """
    def __init__( self, client, mydict:dict, *args, **kwargs ):
        super().__init__( client, mydict, *args, **kwargs )

class PotentialShip(Ship):
    """ A PotentialShip does not yet exist in any form; this is a ship that is 
    able to be built (returned from a call to shipyard.get_buildable()):
            can             1,       # can it be built or not
            combat          0,
            hold_size       1000,
            max_occupants   2,
            reason          null,    # if it can't an array ref will be here with the exception for why not
            speed           1000,    # 100 roughly equals 1 star in 1 hour
            stealth         1500
            type            placebo
            cost    {
                "seconds" : 900,
                "food" : 1100,
                "water" : 1000,
                "energy" : 1200,
                "ore" : 1200,
                "waste" : 100,
            },
    """
    def __init__( self, client, mydict:dict, *args, **kwargs ):
        for k, v in mydict['attributes'].items():
            setattr(self, k, v)
        del mydict['attributes']
        super().__init__( client, mydict, *args, **kwargs )


