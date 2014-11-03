
from lacuna.bc import LacunaObject
from lacuna.building import MyBuilding

"""
    The TLE API docs claim that the view() method retval contains a 'building' 
    key. At least on PT, it does not.

    Other keys that are in the view() method retval:
        next_colony_cost:   integer cost in happy

        food:               dict of food income and storage
                                {   "algae_hour" : 24, "algae_stored" :1322,
                                    "bean_hour" : 1,   "bean_stored" :42,
                                    ..       },

        ore:                dict of ore income and storage, same format as for
                            food

        water and energy do not have their own storage dicts, since those are 
        both "single" storage types (there are multiple types of ore and food, 
        but only one type of water and one type of energy.).  See the planet 
        dict for info on water and energy storage numbers.

        planet:             dict of other planetary details:
                                    {
                                        "id" : "id-goes-here",
                                        "x" : -4,
                                        "y" : 10,
                                        "z" : 6,
                                        "star_id" : "id-goes-here",
                                        "orbit" : 3,
                                        "type" : "habitable planet",
                                        "name" : "Earth",
                                        "image" : "p13",
                                        "size" : 67,
                                        "water" : 900,
                                        "ore" : {
                                            "gold" : 3399,
                                            "bauxite" : 4000,
                                            ...
                                        },
                                        "building_count" : 7,
                                        "population" : 470000,
                                        "happiness" : 3939,
                                        "happiness_hour" : 25,
                                        "food_stored" : 33329,
                                        "food_capacity" : 40000,
                                        "food_hour" : 229,
                                        "energy_stored" : 39931,
                                        "energy_capacity" : 43000,
                                        "energy_hour" : 391,
                                        "ore_hour" 284,
                                        "ore_capacity" 35000,
                                        "ore_stored" 1901,
                                        "waste_hour" : 933,
                                        "waste_stored" : 9933,
                                        "waste_capacity" : 13000,
                                        "water_stored" : 9929,
                                        "water_hour" : 295,
                                        "water_capacity" : 51050
                                    }
"""

class planetarycommand(MyBuilding):
    path = 'planetarycommand'

    def __init__( self, client, body_id:int = 0, building_id:int = 0 ):
        super().__init__( client, body_id, building_id )

    @LacunaObject.set_empire_status
    @MyBuilding.call_building_meth
    def view_plans( self, *args, **kwargs ):
        """ Shows plans stored on the planet.

        Retval includes 'plans', a list of plan dicts:
                {       'extra_build_level': 0,
                        'level': 6,
                        'name': 'Warehouse',
                        'plan_type': 'Module_Warehouse',
                        'quantity': '50'        }
        """
        pass

    @LacunaObject.set_empire_status
    @MyBuilding.call_building_meth
    def view_incoming_supply_chains( self, *args, **kwargs ):
        """ Shows the supply chains coming in to this planet from elsewhere.

        Retval includes 'supply_chains', a list of supply chain dicts:
                        {
                            "id" : "id-goes-here",
                            "from_body" : {
                                "id" : "id-goes-here",
                                "name" : "Mars",
                                "x" : 0,
                                "y" : -123,
                                "image" : "station"
                            },
                            "resource_hour" : 10000000,
                            "resource_type" : 'water',
                            "percent_transferred" : 95,
                            "stalled" : 0,
                        },
        """
        pass

