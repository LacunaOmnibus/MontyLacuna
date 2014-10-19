
from lacuna.building import Building

class network19(Building):
    path = 'network19'

    def __init__( self, client, body_id:int = 0, building_id:int = 0 ):
        super().__init__( client, body_id, building_id )
