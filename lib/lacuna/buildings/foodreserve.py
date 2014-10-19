
from lacuna.building import Building

class foodreserve(Building):
    path = 'foodreserve'

    def __init__( self, client, body_id:int = 0, building_id:int = 0 ):
        super().__init__( client, body_id, building_id )
