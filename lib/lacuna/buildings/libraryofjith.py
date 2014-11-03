
from lacuna.bc import LacunaObject
from lacuna.building import MyBuilding

class libraryofjith(MyBuilding):
    path = 'libraryofjith'

    def __init__( self, client, body_id:int = 0, building_id:int = 0 ):
        super().__init__( client, body_id, building_id )


    @LacunaObject.set_empire_status
    @MyBuilding.call_building_meth
    def research_species( self, empire_id:int, *args, **kwargs ):
        """ Returns information on the species of the indicated empire.

        Retval includes 'species', a dict:
                {
                    "name" : "Human",
                    "description" : "The descendants of Earth.",
                    "min_orbit" : 3,
                    "max_orbit" : 3,
                    "manufacturing_affinity" : 4,
                    "deception_affinity" : 4,
                    "research_affinity" : 4,
                    "management_affinity" : 4,
                    "farming_affinity" : 4,
                    "mining_affinity" : 4,
                    "science_affinity" : 4,
                    "environmental_affinity" : 4,
                    "political_affinity" : 4,
                    "trade_affinity" : 4,
                    "growth_affinity" : 4
                },
        """
        pass
