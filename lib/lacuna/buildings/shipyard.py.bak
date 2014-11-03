
from lacuna.bc import LacunaObject
from lacuna.building import Building
from lacuna.ship import BuildingShip, PotentialShip

class shipyard(Building):
    path = 'shipyard'

    def __init__( self, client, body_id:int = 0, building_id:int = 0 ):
        super().__init__( client, body_id, building_id )

    @Building.call_returning_meth
    def view_build_queue( self, *args, **kwargs ):
        """ Returns a list of ships currently building, how many there are, and 
        how much E it'll cost to subsidize them.
            ships, number, cost = sy.view_build_queue()

        Returns a tuple consisting of:
            ships   List of BuildingShip objects (see ship.py)
            number  Integer number of ships currently building
            cost    Integer cost in E to subsidize the whole queue
        """
        ship_list = []
        for i in kwargs['rslt']['ships_building']:
            ship_list.append( BuildingShip(self.client, i) )
        return( 
            ship_list, 
            kwargs['rslt']['number_of_ships_building'], 
            kwargs['rslt']['cost_to_subsidize'] 
        )

    @LacunaObject.set_empire_status
    @Building.set_building_status
    @Building.call_building_meth
    def subsidize_build_queue( self, *args, **kwargs ):
        """ Spends E to subsidize the current build queue.

        Multiple shipyard buildings share resources and abilities to some 
        extent, but subsidizing the build is not one of them.  This method only 
        applies to the current shipyard; other shipyards' queues will remain.
        """
        pass

    @LacunaObject.set_empire_status
    @Building.set_building_status
    @Building.call_named_meth
    def subsidize_ship( self, named_arguments:dict, *args, **kwargs ):
        """ Spends E to subsidize a single ship in the build queue.
        """
        pass

    @Building.call_returning_meth
    def get_buildable( self, tag:str = '', *args, **kwargs ):
        """ Gets information on what ships are available to be built.
                ships, docks, q_max, q_used = sy.get_buildable()

        Accepts an optional 'tag' string to limit the shiptypes returned.  
        Valid values:
            Colonization, Exploration, Intelligence, Mining, Trade, War
        Defaults to no tag, returning all buildable ships.

        Retval is a tuple:
            ships               list of PotentialShip objects (see ship.py)
            docks_available     Integer count of spaceport docks available for new 
                                ships
            build_queue_max     Maximum number of ships that can be added to the 
                                build queue across all shipyards on this planet.  
                                However, no matter how big this number gets, a 
                                single shipyard can only ever queue a maximum of 
                                50 ships.
            build_queue_used    Number of ships currently in build queues across 
                                all shipyards on this planet.
        """
        ship_list = []
        for name, mydict in kwargs['rslt']['buildable'].items():
            mydict['type'] = name
            ship_list.append( PotentialShip(self.client, mydict) )
        return( 
            ship_list, 
            kwargs['rslt']['docks_available'], 
            kwargs['rslt']['build_queue_max'],
            kwargs['rslt']['build_queue_used']
        )

    @Building.call_returning_meth
    def build_ship( self, type:str, quantity:int = 1, *args, **kwargs ):
        """ Adds one or more ships of a given type to the build queue.

        Arguments:
            type        String, type of ship to build.  Available ship types 
                        can be found by calling get_buildable() and checking 
                        the 'type' attribute of the returned list of ships.
            quantity    Integer number of ships to build.  Defaults to 1.

        Retval is the same tuple as returned by view_build_queue():
            ships   List of BuildingShip objects (see ship.py)
            number  Integer number of ships currently building
            cost    Integer cost in E to subsidize the whole queue
        """
        ship_list = []
        for i in kwargs['rslt']['ships_building']:
            ship_list.append( BuildingShip(self.client, i) )
        return( 
            ship_list, 
            kwargs['rslt']['number_of_ships_building'], 
            kwargs['rslt']['cost_to_subsidize'] 
        )

