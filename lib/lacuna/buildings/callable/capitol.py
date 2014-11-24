
from lacuna.bc import LacunaObject
from lacuna.building import MyBuilding

class capitol(MyBuilding):
    path = 'capitol'

    def __init__( self, client, body_id:int = 0, building_id:int = 0 ):
        super().__init__( client, body_id, building_id )

    @LacunaObject.set_empire_status
    @MyBuilding.call_building_meth
    def rename_empire( self, name:str, **kwargs ):
        """ Renames your empire.

        Renaming your empire has a base cost of 30E, but that cost is reduced 
        by 1E per level of the capitol.  So at Capitol level 30, the rename 
        process has no cost.

        Throws ServerError 1010 if you attempt to rename your empire more 
        than once in a 24 hour period.
        """
        pass
