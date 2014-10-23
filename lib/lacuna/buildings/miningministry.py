
from lacuna.bc import LacunaObject
from lacuna.building import Building

class miningministry(Building):
    path = 'miningministry'

    def __init__( self, client, body_id:int = 0, building_id:int = 0 ):
        super().__init__( client, body_id, building_id )

    @LacunaObject.set_empire_status
    @Building.call_building_meth
    def view_platforms( self, *args, **kwargs ):
        """ Views your current platform status

        Retval includes:
            "max_platforms":    Integer max platforms this min min can support
            "platforms":        List of platform dicts
                        {
                            "id" : "id-goes-here",
                            "asteroid" : {
                                "id" : "id-goes-here",
                                "name" : "Kuiper",
                                "x" : 0,
                                "y" : -444,
                                "image" : "a1-5",
                                ...
                            },
                            "rutile_hour" : 10,
                            "chromite_hour" : 10,
                            "chalcopyrite_hour" : 10,
                            "galena_hour" : 10,
                            "gold_hour" : 10,
                            "uraninite_hour" : 10,
                            "bauxite_hour" : 10,
                            "goethite_hour" : 10,
                            "halite_hour" : 10,
                            "gypsum_hour" : 10,
                            "trona_hour" : 10,
                            "kerogen_hour" : 10,
                            "methane_hour" : 10,
                            "anthracite_hour" : 10,
                            "sulfur_hour" : 10,
                            "zircon_hour" : 10,
                            "monazite_hour" : 10,
                            "fluorite_hour" : 10,
                            "beryl_hour" : 10,
                            "magnetite_hour" : 10,  
                            "shipping_capacity" : 51 
                        },
        """
        pass

    @LacunaObject.set_empire_status
    @Building.call_building_meth
    def view_ships( self, *args, **kwargs ):
        """ View list of ships currently mining.

        Retval includes 'ships', a list of ship dicts:
                {
                    "name" : "CS4",
                    "id" : "id-goes-here",
                    "task" : "Mining",
                    "speed" : 350,
                    "hold_size" : 5600
                },
        """
        pass


