
from lacuna.building import MyBuilding

class corn(MyBuilding):
    path = 'corn'

    def __init__( self, client, body_id:int = 0, building_id:int = 0 ):
        super().__init__( client, body_id, building_id )
