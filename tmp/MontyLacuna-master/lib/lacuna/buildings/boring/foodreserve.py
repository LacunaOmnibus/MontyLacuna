
from lacuna.bc import LacunaObject
from lacuna.building import MultiStorage

class foodreserve(MultiStorage):
    path = 'foodreserve'

    def __init__( self, client, body_id:int = 0, building_id:int = 0 ):
        super().__init__( client, body_id, building_id )
