
from lacuna.building import MyBuilding

class beach2(MyBuilding):
    path = 'beach2'

    def __init__( self, client, body_id:int = 0, building_id:int = 0 ):
        super().__init__( client, body_id, building_id )
