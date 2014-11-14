
import lacuna.bc
import lacuna.building

### The TLE docs claim that the transmit_*() methods will return the same 
### ['building']['work'] block that complete_build_queue() does.
###
### On PT, that simply isn't happening.  The resources are being transmitted, 
### but I'm not getting a 'work' key back.  Those methods do successfully 
### transmit the resource they're meant to, they're just not returning the 
### right data.
### 
### Screw it.  Nobody's ever going to script this building anyway; the fact 
### that the methods at least transmit is close enough.

class subspacesupplydepot(lacuna.building.MyBuilding):
    path = 'subspacesupplydepot'

    def __init__( self, client, body_id:int = 0, building_id:int = 0 ):
        super().__init__( client, body_id, building_id )

    @lacuna.bc.LacunaObject.set_empire_status
    @lacuna.building.MyBuilding.call_building_meth
    def transmit_food( self, *args, **kwargs ):
        pass

    @lacuna.bc.LacunaObject.set_empire_status
    @lacuna.building.MyBuilding.call_building_meth
    def transmit_energy( self, *args, **kwargs ):
        pass

    @lacuna.bc.LacunaObject.set_empire_status
    @lacuna.building.MyBuilding.call_building_meth
    def transmit_ore( self, *args, **kwargs ):
        pass

    @lacuna.bc.LacunaObject.set_empire_status
    @lacuna.building.MyBuilding.call_building_meth
    def transmit_water( self, *args, **kwargs ):
        pass

    @lacuna.building.MyBuilding.call_returning_meth
    def complete_build_queue( self, *args, **kwargs ):
        """ Spends the SSD to complete the current build queue.

        Returns a dict:
            >>> 
            {
                "seconds_remaining" : 99,
                "start" : "01 31 2010 13:09:05 +0600",
                "end" : "01 31 2010 13:09:05 +0600"
            }

        Raises ServerError 1011 if there's not enough time on the SSD to 
        complete the queue.
        """
        return kwargs['building']['work']


class WorkOrder(lacuna.bc.SubClass):
    """
    Attributes:
        >>> 
        seconds_remaining   99,
        start               "01 31 2010 13:09:05 +0600",
        end                 "01 31 2010 13:09:05 +0600"
    """

