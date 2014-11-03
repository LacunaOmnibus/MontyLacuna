
from lacuna.bc import LacunaObject
from lacuna.building import Building

class development(Building):
    path = 'development'

    def __init__( self, client, body_id:int = 0, building_id:int = 0 ):
        super().__init__( client, body_id, building_id )

    @LacunaObject.set_empire_status
    @Building.call_building_meth
    def subsidize_build_queue( self, **kwargs ):
        """ Spends E to immediately finish all buildings currently in the 
        build queue.
        Retval contains key 'essentia_spent' - integer cost of the subsidy.
        """
        pass

    @LacunaObject.set_empire_status
    @Building.call_named_meth
    def subsidize_one_build( self, named_args:dict, **kwargs ):
        """ Spends E to immediately finish a single build in the build queue.

        It's usually cheaper per building to subsidize the entire build queue 
        than to subsidize a single building.  So if your build queue only 
        contains a single building being upgraded, call build_queue() instead 
        of subsidize_one_build().

        named_args must contain 'scheduled_id', the integer ID of the building 
        whose upgrade is scheduled to be subsidized.

        Retval contains key 'essentia_spent' - integer cost of the subsidy.
        """
        pass

    @LacunaObject.set_empire_status
    @Building.call_named_meth
    def cancel_build( self, named_args:dict, **kwargs ):
        """ Removes a single building upgrade from the build queue.
        Any resources that were spent to start the upgrade are lost.

        named_args must contain 'scheduled_id', the integer ID of the building 
        whose upgrade is scheduled to be subsidized.

        Retval contains:
            'build_queue' - list of dicts of buildings remaining in the build 
            queue:
                [ {     'building_id': '4390067',
                        'name': 'Space Port',
                        'seconds_remaining': 50695,
                        'subsidy_cost': 10,
                        'to_level': 29,
                        'x': '1',
                        'y': '-1'   },
                    { ... }         ],

            'subsidy_cost' - integer cost to subsidize the entire remaining 
            build queue, now that this building's upgrade has been cancelled.
        """
        pass

