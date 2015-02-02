
import lacuna.bc
import lacuna.building
import lacuna.ship

class shipyard(lacuna.building.MyBuilding):
    path = 'shipyard'

    def __init__( self, client, body_id:int = 0, building_id:int = 0 ):
        super().__init__( client, body_id, building_id )

    @lacuna.building.MyBuilding.call_returning_meth
    def view_build_queue( self, *args, **kwargs ):
        """ Returns a list of ships currently building, how many there are, and 
        how much E it'll cost to subsidize them.

        Returns a tuple consisting of:
            - ships -- List of lacuna.ship.BuildingShip objects
            - number -- Integer number of ships currently building
            - cost -- Integer cost in E to subsidize the whole queue

        - :class:`lacuna.ship.BuildingShip`
        """
        ship_list = []
        for i in kwargs['rslt']['ships_building']:
            ship_list.append( lacuna.ship.BuildingShip(self.client, i) )
        return( 
            ship_list, 
            self.get_type(kwargs['rslt']['number_of_ships_building']), 
            self.get_type(kwargs['rslt']['cost_to_subsidize']) 
        )

    @lacuna.bc.LacunaObject.set_empire_status
    @lacuna.building.MyBuilding.set_building_status
    @lacuna.building.MyBuilding.call_building_meth
    def subsidize_build_queue( self, *args, **kwargs ):
        """ Spends E to subsidize the current build queue.

        Multiple shipyard buildings share resources and abilities to some 
        extent, but subsidizing the build is not one of them.  This method only 
        applies to the current shipyard; other shipyards' queues will remain.
        """
        pass

    @lacuna.bc.LacunaObject.set_empire_status
    @lacuna.building.MyBuilding.set_building_status
    @lacuna.building.MyBuilding.call_named_meth
    def subsidize_ship( self, named_arguments:dict, *args, **kwargs ):
        """ Spends E to subsidize a single ship in the build queue.

        Arguments:
            - named_arguments -- Dict of named arguments containing only
              ``{ 'ship_id': 12345 }``

        Subsidizes the build of a specific ship for 1 E.
        """
        pass

    @lacuna.building.MyBuilding.call_returning_meth
    def get_buildable( self, tag:str = '', *args, **kwargs ):
        """ Gets information on what ships are available to be built.

        Arguments:
            - tag -- Optional string indicating the type of ship you want 
              returned.  Defaults to no tag, which will return a list of 
              all buildable ships.  Valid tag values are: ``Colonization``,
              ``Exploration``, ``Intelligence``, ``Mining``, ``Trade``, ``War``

        Returns a tuple:
            - ships -- list of lacuna.ship.PotentialShip objects
            - docks_available -- Integer count of spaceport docks available 
              for new ships
            - build_queue_max -- Maximum number of ships that can be added to 
              the build queue across all shipyards on this planet.  However, 
              no matter how big this number gets, a single shipyard can only 
              ever queue a maximum of 50 ships.
            - build_queue_used -- Number of ships currently in build queues 
              across all shipyards on this planet.

        - :class:`lacuna.ship.PotentialShip`
        """
        ship_list = []
        for name, mydict in kwargs['rslt']['buildable'].items():
            mydict['type'] = name
            ship_list.append( lacuna.ship.PotentialShip(self.client, mydict) )
        return( 
            ship_list, 
            self.get_type(kwargs['rslt']['docks_available']), 
            self.get_type(kwargs['rslt']['build_queue_max']),
            self.get_type(kwargs['rslt']['build_queue_used'])
        )

    @lacuna.building.MyBuilding.call_returning_meth
    def build_ship( self, type:str, quantity:int = 1, *args, **kwargs ):
        """ Adds one or more ships of a given type to the build queue.

        Arguments:
            - type -- String, type of ship to build.  Available ship types can 
              be found by calling :meth:`get_buildable` and checking the 
              ``type`` attribute of the returned list of ships.
            - quantity -- Integer number of ships to build.  Defaults to 1.

        Returns a tuple consisting of:
            - ships -- List of lacuna.ship.BuildingShip objects (the ships now 
              being built)
            - number -- Integer number of ships currently building
            - cost -- Integer cost in E to subsidize the whole queue

        - :class:`lacuna.ship.BuildingShip`
        """
        ship_list = []
        for i in kwargs['rslt']['ships_building']:
            ship_list.append( lacuna.ship.BuildingShip(self.client, i) )
        return( 
            ship_list, 
            self.get_type(kwargs['rslt']['number_of_ships_building']),
            self.get_type(kwargs['rslt']['cost_to_subsidize'])
        )

