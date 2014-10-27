
from lacuna.bc import LacunaObject
from lacuna.building import Building

"""
    The view() method will include the key 'party'.  If there is a party 
    currently ongoing, this key will contain:
            {
                "seconds_remaining" : 397,
                "happiness" : 10000,
                "can_throw" : 0
            }

    If there is no party happening right now, that 'party' key will contain 
    only:
            { "can_throw" : 1 }

"""

class park(Building):
    path = 'park'

    def __init__( self, client, body_id:int = 0, building_id:int = 0 ):
        super().__init__( client, body_id, building_id )

    @LacunaObject.set_empire_status
    @Building.call_building_meth
    def throw_a_party( self, *args, **kwargs ):
        """ Throw a party at the park to gain happiness.

        Requires 10,000 food, which will be used automatically, and produces a 
        base of 3,000 happiness.

        For each unique food type you have onsite (in quantities of at least 
        500), the happiness multiplier increases by one.  So four food types 
        increases your multiplier to 4, giving you:
            3000 (base happy) * 4 (food multiplier) == 12,000 happy

        Additionally, each level of the park awards an additional multiplier of 
        0.3.  So at level 10, a party would give you:
            3000 (base happy) * (10 * 0.3 == 3) (level multiplier) == 9,000 happy

        Once a party has been thrown, it takes 12 hours to wind down, at which 
        point you can throw another party.

        Raises ServerError 1010 if there's already a party going on.
        """
        pass

    @LacunaObject.set_empire_status
    @Building.call_building_meth
    def subsidize_party( self, *args, **kwargs ):
        """
        """
        pass



