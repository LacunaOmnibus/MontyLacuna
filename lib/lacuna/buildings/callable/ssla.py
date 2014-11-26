
from lacuna.bc import LacunaObject
from lacuna.building import MyBuilding
from lacuna.plan import *

class ssla(MyBuilding):
    path = 'ssla'

    def __init__( self, client, body_id:int = 0, building_id:int = 0 ):
        super().__init__( client, body_id, building_id )

    def _marshal_view(self, rv):
        """ All ssla methods return data in the same format, so they all call
        _marshal_view().
        """
        plans_list = []
        for i in rv['make_plan']['types']:
            plans_list.append( PotentialSSPlan(self.client, i) )

        costs_list = []
        for i in rv['make_plan']['level_costs']:
            costs_list.append( LevelCosts(self.client, i) )

        making = 'None'
        if 'making' in rv['make_plan']:
            making = rv['make_plan']['making']

        subsidy_cost = 'None'
        if 'subsidy_cost' in rv['make_plan']:
            subsidy_cost = rv['make_plan']['subsidy_cost']

        return(
            plans_list,
            costs_list,
            subsidy_cost,
            making
        )

    @MyBuilding.call_returning_meth
    def view( self, *args, **kwargs ):
        """ Returns info on plans that can be built and their costs.

        Returns a tuple:
            - plans -- List of PotentialSSPlan objects
            - costs -- List of LevelCosts objects
            - sub_cost -- Integer cost to subsidize a plan (always 2)
            - making -- Name of plan currently being made.  "None" if no plan is in the works.
        """
        return self._marshal_view( kwargs['rslt'] )

    @MyBuilding.call_returning_meth
    def make_plan( self, type:str, level:int, *args, **kwargs ):
        """ Starts a plan building.

        Keep in mind that you must send the plan type, NOT its name.

        Returns the same tuple as view().
        """
        return self._marshal_view( kwargs['rslt'] )

    @MyBuilding.call_returning_meth
    def subsidize_plan( self, *args, **kwargs ):
        """ Spends 2 E to subsidize the currently-building plan.

        Returns the same tuple as view().
        """
        return self._marshal_view( kwargs['rslt'] )

