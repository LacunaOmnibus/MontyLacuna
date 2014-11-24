
import lacuna.bc
import lacuna.building
import lacuna.plan
import lacuna.resource

"""
    The TLE API docs claim that the view() method retval contains a 'building' 
    key. At least on PT, it does not.
"""

class planetarycommand(lacuna.building.MyBuilding):
    path = 'planetarycommand'

    def __init__( self, client, body_id:int = 0, building_id:int = 0 ):
        super().__init__( client, body_id, building_id )


    @lacuna.building.MyBuilding.call_returning_meth
    def view( self, *args, **kwargs ):
        """
        Returns a tuple:
            - food -- List of lacuna.resource.PlanetaryFood objects
            - ore -- List of lacuna.resource.PlanetaryOre objects
            - planet -- Single lacuna.body.Planet object
            - cost -- Cost of your next colony, in happiness
        """
        food    = lacuna.resource.PlanetaryFood(self.client, kwargs['rslt']['food'])
        ore     = lacuna.resource.PlanetaryOre(self.client, kwargs['rslt']['ore'])
        planet  = lacuna.body.Planet(self.client, kwargs['rslt']['planet'])
        return(
            food, 
            ore, 
            planet, 
            kwargs['rslt']['next_colony_cost']
        )


    @lacuna.building.MyBuilding.call_returning_meth
    def view_plans( self, *args, **kwargs ):
        """ Shows plans stored on the planet.

        Retval includes 'plans', a list of plan dicts:

::

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

        Returns a list of SupplyChain objects.
        """
        mylist = []
        for i in kwargs['rslt']['supply_chains']:
            mylist.append( SupplyChain(self.client, i) )
        return mylist

class SupplyChain(lacuna.bc.SubClass):
    """
    Attributes::

        id                      "id-goes-here",
        from_body               {   "id" : "id-goes-here",
                                    "name" : "Mars",
                                    "x" : 0,
                                    "y" : -123,
                                    "image" : "station",
                                    ...      },
        resource_hour           10000000,
        resource_type           'water',
        percent_transferred     95,
        stalled                 0,
    """

