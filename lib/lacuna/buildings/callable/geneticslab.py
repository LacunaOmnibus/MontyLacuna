
import lacuna.bc
import lacuna.building
import lacuna.empire
import lacuna.spy

class geneticslab(lacuna.building.MyBuilding):
    path = 'geneticslab'

    def __init__( self, client, body_id:int = 0, building_id:int = 0 ):
        super().__init__( client, body_id, building_id )

    @lacuna.building.MyBuilding.call_returning_meth
    def prepare_experiment( self, *args, **kwargs ):
        """ Returns information needed to set up a genetics experiment.

        CHECK
        grafts_list should be an object, not a list of dicts.

        Returns a tuple:
            - grafts_list -- List of dicts
            - survival_odds -- Integer percent odds of the victim surviving
            - graft_odds -- Integer percent odds of the graft working
            - essentia_cost -- Integer cost per experiment attempt
            - can_experiment -- Boolean; whether the lab can be used or not.

        The dicts in grafts_list each describe one prisoner who's available to 
        do experiments on:
        - spy -- spy.Spy object
        - species -- empire.Species object
        - graftable_affinities -- List of affinity names; these are affinities of the prisoner's that are higher than your own, eg ["min_orbit", "management_affinity", ... ]
        """
        grafts_list = []
        for i in kwargs['rslt']['grafts']:
            grafts_list.append({
                'spy':                  lacuna.spy.Spy( self.client, i['spy'] ),
                'species':              lacuna.empire.Species( self.client, i['species'] ),
                'graftable_affinities': i['graftable_affinities'],
            })
        return (
            grafts_list,
            self.get_type(kwargs['rslt']['survival_odds']),
            self.get_type(kwargs['rslt']['graft_odds']),
            self.get_type(kwargs['rslt']['essentia_cost']),
            self.get_type(kwargs['rslt']['can_experiment']),
        )

    @lacuna.building.MyBuilding.call_returning_meth
    def run_experiment( self, spy_id:int, affinity:str, *args, **kwargs ):
        """ Runs a genetics experiment on a spy in an attempt to graft one of 
        his affinities onto your species.

        Returns a single geneticslab.ExperimentResults object.
        """
        return ExperimentResults( self.client, kwargs['rslt']['experiment'] )

    @lacuna.building.MyBuilding.call_returning_meth
    def rename_species( self, named_args:dict, *args, **kwargs ):
        """ Allows you to change your species name and description.

        Argument is a single dict:
            - name -- "My New Species Name",
            - description -- "My New Species Description"

            name requirements:
            - 30 characters or fewer
            - Not blank
            - @, & <, >, ; are prohibited.

            description requirements:
            - 1024 characters or fewer
            - <, > are prohibited.

        Retval contains only 'success', set to 1.  No status is returned.

        Raises ServerError 1000 for bad species name.
        Raises ServerError 1005 for bad description.
        """
        return self.get_type(kwargs['rslt']['success'])


class ExperimentResults(lacuna.bc.SubClass):
    """
    Attributes::
        
        graft       Integer.  1 for success, 0 for failure
        survive     Integer.  1 for success, 0 for failure
        message     String.   eg "The graft was a success, and the prisoner 
                    did not survive the experiment."
    """
    pass


