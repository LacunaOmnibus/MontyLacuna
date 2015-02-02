
import lacuna.bc
import lacuna.body
import lacuna.building
import lacuna.plan
import lacuna.ship

class stationcommand(lacuna.building.MyBuilding):
    path = 'stationcommand'

    def __init__( self, client, body_id:int = 0, building_id:int = 0 ):
        super().__init__( client, body_id, building_id )


    @lacuna.building.MyBuilding.call_returning_meth
    def view( self, *args, **kwargs ):
        """ Get station details.

        Returns a single :class:`lacuna.body.Planet` object.
        """ 
        return lacuna.body.Planet(self.client, kwargs['rslt']['planet'])


    @lacuna.building.MyBuilding.call_returning_meth
    def view_plans( self, *args, **kwargs ):
        """ See what plans are already on the station.

        The TLE docs don't list 'quantity' as one of the returned attributes, 
        but it's there.

        Returns a single :class:`lacuna.plan.OwnedPlan` object.
        """ 
        mylist = []
        for i in kwargs['rslt']['plans']:
            mylist.append( lacuna.plan.OwnedPlan(self.client, i) )
        return mylist


    @lacuna.building.MyBuilding.call_returning_meth
    def view_incoming_supply_chains( self, *args, **kwargs ):
        """ Get incoming supply chains.

        Returns a list of :class:`lacuna.resource.SupplyChain` objects.
        """ 
        mylist = []
        for i in kwargs['rslt']['supply_chains']:
            mylist.append( lacuna.resource.SupplyChain(self.client, i) )
        return mylist


