
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

        **CHECK** - I need prisoners to test this.  I haven't got any prisoners, 
        so this method has not been tested.  I think that it *should* be fine, 
        but it has not been tested.

        If this comment still exists and you're wanting to use this method, 
        keep in mind that the ``grafts_list`` returned might not be as 
        advertised.  It should be, but check it before assuming it's correct. 

        And if you do that, let ``tmtowtdi`` know whether it worked or not.

        Returns a tuple:
            - grafts_list -- List of lacuna.buildings.geneticslab.Graft objects
            - survival_odds -- Integer percent odds of the victim surviving
            - graft_odds -- Integer percent odds of the graft working
            - essentia_cost -- Integer cost per experiment attempt
            - can_experiment -- Boolean; whether the lab can be used or not.

        - :class:`lacuna.buildings.callable.geneticslab.Graft`

        """
        grafts_list = []
        for i in kwargs['rslt']['grafts']:
            grafts_list.append( Graft(client, i) )
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

        Arguments:
            - spy_id -- Integer ID of the spy to experiment on.
            - affinity -- String name of the affinity to try to graft.

        Returns a single :class:`lacuna.buildings.callable.geneticslab.ExperimentResults` object.
        """
        return ExperimentResults( self.client, kwargs['rslt']['experiment'] )

    @lacuna.building.MyBuilding.call_returning_meth
    def rename_species( self, named_args:dict, *args, **kwargs ):
        """ Allows you to change your species name and description.

        Arguments:
            - named_args -- Dict.
              ``{ 'name': "New Species Name", 'description': -- "New Species Description" }``

        - ``name`` key requirements

          - 30 characters or fewer
          - Not blank
          - @, & <, >, ; are prohibited.

        - ``description`` key requirements

          - 1024 characters or fewer
          - <, > are prohibited.

        Returns a dict containing only the key ``success``, set to 1.  No status 
        is returned.

        - Raises :class:`lacuna.exceptions.ServerError` 1000 for bad species name.
        - Raises :class:`lacuna.exceptions.ServerError` 1005 for bad description.
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


class Graft(lacuna.bc.SubClass):
    """
    Attributes::

        spy                     lacuna.spy.Spy object
        species                 lacuna.empire.Species object of the spy
        graftable_affinities    List of affinity names that can be grafted from 
                                the spy to your empire

    - :class:`lacuna.spy.Spy`
    - :class:`lacuna.empire.Species`
    """
    def __init__(self, client, mydict:dict):
        self.client                 = client
        self.spy                    = lacuna.spy.Spy( self.client, mydict['spy'] )
        self.species                = lacuna.empire.Species( self.client, mydict['species'] )
        self.graftable_affinities   = mydict['graftable_affinities']

