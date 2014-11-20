
from lacuna.building import MyBuilding

class beach8(MyBuilding):
    path = 'beach8'

    def __init__( self, client, body_id:int = 0, building_id:int = 0 ):
        super().__init__( client, body_id, building_id )
