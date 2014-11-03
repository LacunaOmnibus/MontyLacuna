
import lacuna.bc
import lacuna.building

class geneticslab(lacuna.building.MyBuilding):
    path = 'geneticslab'

    def __init__( self, client, body_id:int = 0, building_id:int = 0 ):
        super().__init__( client, body_id, building_id )

    @lacuna.bc.LacunaObject.set_empire_status
    @lacuna.building.MyBuilding.call_building_meth
    def prepare_experiment( self, *args, **kwargs ):
        """ Returns information needed to set up a genetics experiment.

        CHECK - My affinities are maxed, so I can't test this.  I get a false 
        value for "can_experiment", and "grafts" as an empty list, so much of 
        the docu below is just taken from the TLE API docu, not from testing.

        Retval includes:
            "survival_odds" : 31,   # Integer percent odds of the victim surviving
            "graft_odds" : 11,      # Integer percent odds of the graft working
            "essentia_cost" : 2,    # Integer cost per experiment attempt
            "can_experiment" : 1    # Boolean; whether the lab can be used or not.

            "grafts" : [
                {
                    "spy" : {
                        "id" : "id-goes-here",
                        "name" : "James Bond",
                        ...
                    },
                    "species" : {
                        "min_orbit" : 3,
                        "max_orbit" : 4,
                        "science_affinity" : 4,
                        ...
                    },
                    graftable_affinities : [
                        "min_orbit",
                        "management_affinity"
                    ]
                },
                ...
            ],
        """
        pass

    @lacuna.bc.LacunaObject.set_empire_status
    @lacuna.building.MyBuilding.call_building_meth
    def run_experiment( self, spy_id:int, affinity:str, *args, **kwargs ):
        """ Runs a genetics experiment on a spy in an attempt to graft one of 
        his affinities onto your species.

        CHECK - My affinities are maxed, so I can't test this.

        Retval contains 'experiment', a dict containing:
            "graft": 1          # Boolean; did the graft attempt succeed?
            "survive": 1        # Boolean; did the victim survive?
            "message": "yay!"   # String
            
        The retval also includes the same keys as returned by prepare_experiment().
        """
        pass

    @lacuna.building.MyBuilding.call_building_meth
    def rename_species( self, named_args:dict, *args, **kwargs ):
        """ Allows you to change your species name and description.

        Accepts a dict:
            "name": "My New Species Name",
            "description": "My New Species Description"

        Name:
            - 30 characters or fewer
            - Not blank
            - @, & <, >, ; are prohibited.

        Description:
            - 1024 characters or fewer
            - <, > are prohibited.

        Retval contains only 'success', set to 1.  No status is returned.

        Raises ServerError 1000 for bad species name.
        Raises ServerError 1005 for bad description.
        """
        pass
