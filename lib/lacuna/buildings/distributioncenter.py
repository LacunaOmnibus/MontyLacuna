
import lacuna.bc
import lacuna.building
import lacuna.resource

class distributioncenter(lacuna.building.MyBuilding):
    path = 'distributioncenter'

    def __init__( self, client, body_id:int = 0, building_id:int = 0 ):
        super().__init__( client, body_id, building_id )

    @lacuna.bc.LacunaObject.set_empire_status
    @lacuna.building.MyBuilding.call_building_meth
    def reserve( self, resources:list, **kwargs ):
        """ Reserves some resources for a set period of time.

        resources is a list of dicts of resources to reserve:
                res = [
                    { 'type': 'water', 'quantity': 100 },
                    { 'type': 'energy', 'quantity': 200 },
                ]

        Once resources are reserved, you can't just add more resources.  A 
        second call to reseve, eg:
                res = [
                    { 'type': 'apple', 'quantity': 300 },
                ]
        ...will result in ONLY the 300 apple being stored.

        So each call to reserve() must contain the complete list of all 
        resources you wish to reserve.

        Retval includes key 'reserve':
            {   'can': 0,
                'max_reserve_duration': 7200,
                'max_reserve_size': 125892,
                'resources': [   {'quantity': 100, 'type': 'water'},
                                {'quantity': 200, 'type': 'energy'}   ],
                'seconds_remaining': 7200   }

            'can' being set to false means that the dist center currently 
            cannot reserve resources.  This is misleading, it certainly can.  
            But again, re-calling reserve() will REPLACE the 
            currently-reserved resources with the new list.
        """
        pass

    #@lacuna.bc.LacunaObject.set_empire_status
    #@lacuna.building.MyBuilding.call_building_meth
    @lacuna.building.MyBuilding.call_returning_meth
    def get_stored_resources( self, **kwargs ):
        """ Returns a list of resources you currently have on this planet.

        This is NOT a list of resources currently reserved in the distribution 
        center; this is a total list of all available resources on the planet; 
        these resources are available to be reserved in the distribution 
        center.

        Returns a tuple:
            resources       A single resources.StoredResources object
            cargo_space     Amount of cargo space units occupied by each 
                            individual resource.  Always '1'.
        """
        return (
            lacuna.resources.StoredResources(self.client, kwargs['rslt']['resources']),
            kwargs['rslt']['cargo_space_used_each']
        )

    @lacuna.bc.LacunaObject.set_empire_status
    @lacuna.building.MyBuilding.call_building_meth
    def release_reserve( self, **kwargs ):
        """ Releases any resources currently being reserved.

        Retval contains key 'reserve':
                {   'can': 1,
                    'max_reserve_duration': 7200,
                    'max_reserve_size': 125892      },

        Raises ServerError 1010 if there are currently no resources being 
        reserved.
        """
        pass

