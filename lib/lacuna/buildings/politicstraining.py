
from lacuna.building import Building

"""

    The view() method includes the key 'spies', a dict:
                {
                    "max_points" : 2600,
                    "points_per" : 45,
                    "in_training" : 4,
                },

"""

class politicstraining(Building):
    path = 'politicstraining'

    def __init__( self, client, body_id:int = 0, building_id:int = 0 ):
        super().__init__( client, body_id, building_id )
