
import lacuna.bc
import lacuna.building
import lacuna.resource

class distributioncenter(lacuna.building.MyBuilding):
    path = 'distributioncenter'

    def __init__( self, client, body_id:int = 0, building_id:int = 0 ):
        super().__init__( client, body_id, building_id )

    @lacuna.building.MyBuilding.call_returning_meth
    def view(self, *args, **kwargs):
        """ Returns a single Reserve object.  """
        return Reserve( self.client, kwargs['rslt']['reserve'] )

    @lacuna.building.MyBuilding.call_returning_meth
    def reserve( self, resources:list, **kwargs ):
        """ Reserves some resources for a set period of time.

        Once resources are reserved, you can't just add more resources to the 
        existing reserve; each call to reserve() must specify all the resources 
        to be reserved.  So this...
        >>> dist.reserve( [{'type':'apple', quantity:300}] )
        >>> dist.reserve( [{'type':'bean',  quantity:100}] )

        ...would result in only 100 bean being reserved.

        Requires a list of dicts of resources to reserve.  Each dict requires:
            - type -- The type of res to reserve, eg 'water'
            - quantity -- Integer quantity to reserve, eg 100

        Returns a single Reserve object.
        """
        return Reserve( self.client, kwargs['rslt']['reserve'] )

    @lacuna.building.MyBuilding.call_returning_meth
    def get_stored_resources( self, **kwargs ):
        """ Returns a list of resources you currently have on this planet.

        This is NOT a list of resources currently reserved in the distribution 
        center; this is a total list of all available resources on the planet; 
        these resources are available to be reserved in the distribution 
        center.

        Returns a tuple:
            - resources -- A single resources.StoredResources object
            - cargo_space -- Amount of cargo space units occupied by each individual resource.  Always '1'.
        """
        return (
            lacuna.resource.StoredResources(self.client, kwargs['rslt']['resources']),
            kwargs['rslt']['cargo_space_used_each']
        )

    @lacuna.building.MyBuilding.call_returning_meth
    def release_reserve( self, **kwargs ):
        """ Releases any resources currently being reserved.

        Returns a single Reserve object.

        Raises ServerError 1010 if there are currently no resources being 
        reserved.
        """
        return Reserve( self.client, kwargs['rslt']['reserve'] )

class Reserve(lacuna.bc.SubClass):
    """
    Attributes:
        >>> 
        seconds_remaining       0, # time until reserved resources will automatically be released
        can                     1,
        max_reserve_duration    "7200", # max length resources can be kept in reserve
        max_reserve_size        100000, # max amount of resources that can be reserved
        resources               A resource.StoredResources object.
    """
    ### mydict['resources'] is coming to us as:
        # [       # resources currently in reserve
        #     {
        #         "type" : "water",
        #         "quanity" : 2000
        #     },
        #     {
        #         "type" : "apples",
        #         "quanity" : 2000
        #     }
        #     ...
        # ]

    def __init__(self, client, mydict:dict):
        resdict = {}
        if 'resources' in mydict:
            for i in mydict['resources']:
                resdict[ i['type'] ] = i['quantity']
        mydict['resources'] = lacuna.resource.StoredResources(client, resdict)
        super().__init__(client, mydict)

