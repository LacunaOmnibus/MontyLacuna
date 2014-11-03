
import lacuna
from lacuna.bc import LacunaObject
from lacuna.building import MyBuilding

class observatory(MyBuilding):
    path = 'observatory'

    def __init__( self, client, body_id:int = 0, building_id:int = 0 ):
        super().__init__( client, body_id, building_id )

    @MyBuilding.call_returning_meth
    def get_probed_stars( self, *args, **kwargs ):
        """ Returns a list of probed stars, as well as stats on how many probes 
        you have out and available.

        Retval includes:
            star_count:     Integer number of stars you have probed.
            max_probes:     Integer number of the maximum probes you can have 
                            out from this observatory.
            travelling:     Integer number of how many probes are currently 
                            travelling from your planet to a star.
            stars:
                            List of lacuna.map.Star objects.  These are the 
                            stars at which your observatory currently has 
                            probes.
        """
        star_list = []
        for s in kwargs['rslt']['stars']:
            star_list.append( lacuna.map.Star(self.client, s) )
        kwargs['rslt']['stars'] = star_list
        return kwargs['rslt']

    @LacunaObject.set_empire_status
    @MyBuilding.call_building_meth
    def abandon_probe( self, star_id:int, *args, **kwargs ):
        """ Abandons a single probe.

        Requires 'star_id', integer ID of the star whose probe you wish to 
        abandon.

        You are abandoning by the ID of the star you have probed, NOT by the ID 
        of the probe ship itself - don't hurt yourself looking for the probe's 
        ID.
        """
        pass

    @LacunaObject.set_empire_status
    @MyBuilding.call_building_meth
    def abandon_all_probes( self, *args, **kwargs ):
        """ Abandons all of this observatory's probes.  """
        pass


