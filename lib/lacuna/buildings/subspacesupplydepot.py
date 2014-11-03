
from lacuna.bc import LacunaObject
from lacuna.building import MyBuilding

"""
    This entire module is untested; I haven't got an SSD to fool with.

    Since a utility script to run an SSD wouldn't have much utility, I'm not 
    going to stress over this too much.


    Each method in here should return the same thing, a retval containing the 
    key 'building':
            {
                "work" : {
                    "seconds_remaining" : 99,
                    "start" : "01 31 2010 13:09:05 +0600",
                    "end" : "01 31 2010 13:09:05 +0600"
                }
            },

"""

class subspacesupplydepot(MyBuilding):
    path = 'subspacesupplydepot'

    def __init__( self, client, body_id:int = 0, building_id:int = 0 ):
        super().__init__( client, body_id, building_id )

    @LacunaObject.set_empire_status
    @MyBuilding.call_building_meth
    def transmit_food( self, *args, **kwargs ):
        pass

    @LacunaObject.set_empire_status
    @MyBuilding.call_building_meth
    def transmit_energy( self, *args, **kwargs ):
        pass

    @LacunaObject.set_empire_status
    @MyBuilding.call_building_meth
    def transmit_ore( self, *args, **kwargs ):
        pass

    @LacunaObject.set_empire_status
    @MyBuilding.call_building_meth
    def transmit_water( self, *args, **kwargs ):
        pass

    @LacunaObject.set_empire_status
    @MyBuilding.call_building_meth
    def complete_build_queue( self, *args, **kwargs ):
        pass
