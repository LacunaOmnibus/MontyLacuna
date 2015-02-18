
import lacuna.bc
import lacuna.building
import lacuna.plan
import lacuna.resource

class planetarycommand(lacuna.building.MyBuilding):
    """ Planetary Command Center """

    path = 'planetarycommand'

    def __init__( self, client, body_id:int = 0, building_id:int = 0 ):
        super().__init__( client, body_id, building_id )


    @lacuna.building.MyBuilding.call_returning_meth
    def view( self, *args, **kwargs ):
        """ Get planet details.

        The TLE API claim that the view() method returned dict contains a 
        'building' key. At least on PT, it does not.

        Returns a tuple:
            - food -- List of :class:`lacuna.resource.PlanetaryFood` objects
            - ore -- List of :class:`lacuna.resource.PlanetaryOre` objects
            - planet -- Single :class:`lacuna.body.Planet` object
            - cost -- Cost of your next colony, in happiness
        """
        food    = lacuna.resource.PlanetaryFood(self.client, kwargs['rslt']['food'])
        ore     = lacuna.resource.PlanetaryOre(self.client, kwargs['rslt']['ore'])
        planet  = lacuna.body.Planet(self.client, kwargs['rslt']['planet'])
        return(
            food, 
            ore, 
            planet, 
            self.get_type(kwargs['rslt']['next_colony_cost'])
        )


    @lacuna.building.MyBuilding.call_returning_meth
    def view_plans( self, *args, **kwargs ):
        """ Shows plans stored on the planet.

        Retval includes 'plans', a list of plan dicts::

            {       'extra_build_level': 0,
                    'level': 6,
                    'name': 'Warehouse',
                    'plan_type': 'Module_Warehouse',
                    'quantity': '50'        }
        """
        mylist = []
        for i in kwargs['rslt']['plans']:
            mylist.append( lacuna.plan.OwnedPlan(self.client, i) )
        return mylist


    @lacuna.building.MyBuilding.call_returning_meth
    def view_incoming_supply_chains( self, *args, **kwargs ):
        """ Shows the supply chains coming in to this planet from elsewhere.

        Returns a list of :class:`lacuna.resource.SupplyChain` objects.
        """
        mylist = []
        for i in kwargs['rslt']['supply_chains']:
            mylist.append( lacuna.resource.SupplyChain(self.client, i) )
        return mylist

