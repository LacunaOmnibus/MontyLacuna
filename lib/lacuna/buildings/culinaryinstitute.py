
from lacuna.building import Building

class culinaryinstitute(Building):
    path = 'culinaryinstitute'

    def __init__( self, client, body_id:int = 0, building_id:int = 0 ):
        super().__init__( client, body_id, building_id )
