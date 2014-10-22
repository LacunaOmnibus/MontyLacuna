
from lacuna.bc import LacunaObject
from lacuna.building import Storage

class energyreserve(Storage):
    path = 'energyreserve'

    def __init__( self, client, body_id:int = 0, building_id:int = 0 ):
        super().__init__( client, body_id, building_id )
