
from lacuna.building import MyBuilding

class crater(MyBuilding):
    path = 'crater'

    def __init__( self, client, body_id:int = 0, building_id:int = 0 ):
        super().__init__( client, body_id, building_id )
