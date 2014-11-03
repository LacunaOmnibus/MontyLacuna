
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
        """ View list of mining-capable ships.

        All ships that can be used for mining are returned.  If a given ship's 
        task is 'Mining', it's currently shutting ore to and from your mining 
        platforms.  If its task is listed as 'Docked', it's available to be 
        added to your current mining fleet.

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

    @LacunaObject.set_empire_status
    @Building.call_building_meth
    def add_cargo_ship_to_fleet( self, ship_id:int, *args, **kwargs ):
        """ Adds a ship to the mining fleet.

        The "cargo ship" does not have to specifically be of type "cargo_ship", 
        it just has to be capable of carrying cargo (eg hulk_mega, 
        smuggler_ship, etc).  

        Requires "ship_id", the integer ID of the ship to add to the fleet.
        """
        pass

    @LacunaObject.set_empire_status
    @Building.call_building_meth
    def remove_cargo_ship_from_fleet( self, ship_id:int, *args, **kwargs ):
        """ Takes a single ship off mining duty; sends the ship a message to 
        return to base to perform the "Docked" task.

        After being removed from mining duty, the ship will need to travel 
        from the mining location back to your space port's planet, so it will 
        not be available for use immediately.

        Requires "ship_id", the integer ID of the ship to removed from the 
        fleet.
        """
        pass

    @LacunaObject.set_empire_status
    @Building.call_building_meth
    def abandon_platform( self, platform_id:int, *args, **kwargs ):
        """ Abandon one of your mining platforms.

        Requires "platform_id", the integer ID of the platform to abandon.

        Remember that you might have multiple platforms on a single asteroid.  
        When you abandon, you are abandoning the platform, not the asteroid, so 
        be careful to send the platform ID, not the ID of the asteroid itself.
        """
        pass


