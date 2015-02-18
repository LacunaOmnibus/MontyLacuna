
import lacuna.bc
import lacuna.building
import lacuna.ship

class policestation(lacuna.building.MyBuilding):
    path = 'policestation'

    def __init__( self, client, body_id:int = 0, building_id:int = 0 ):
        super().__init__( client, body_id, building_id )


    @lacuna.building.MyBuilding.call_returning_meth
    def view_foreign_ships( self, page_number:int = 1, **kwargs ):
        """ Shows incoming ships, 25 at a time.

        "Foreign" ships include all ships.  Even if your empire is the owner of 
        the station, and your empire is the one sending ships, those ships will 
        show up as "foreign."

        Arguments:
            - page_number -- Optional page of results to view.  Defaults to 1.

        Returns a tuple:
            - ships -- list of :class:`lacuna.ship.IncomingShip` objects.
            - number -- total number of incoming ships.
        """
        mylist = []
        for i in kwargs['rslt']['ships']:
            mylist.append( lacuna.ship.IncomingShip(self.client, i) )
        return (mylist, kwargs['rslt']['number_of_ships'])


    @lacuna.building.MyBuilding.call_returning_meth
    def view_ships_orbiting( self, page_number:int = 1, **kwargs ):
        """ Shows incoming foreign ships, 25 at a time.

        Arguments:
            - page_number -- Optional page of results to view.  Defaults to 1.

        Returns a tuple:
            - ships -- list of :class:`lacuna.ship.ForeignOrbiting` objects.
            - number -- total number of incoming ships.
        """
        mylist = []
        for i in kwargs['rslt']['ships']:
            mylist.append( lacuna.ship.ForeignOrbiting(self.client, i) )
        return (mylist, kwargs['rslt']['number_of_ships'])


    @lacuna.building.MyBuilding.call_returning_meth
    def view_ships_travelling( self, page_number:int = 1, **kwargs ):
        """ Does not appear to do anything.

        This method's existence might be a copy/paste error.  ALL ships incoming 
        to a space station, even if they're sent by the station owner, are shown 
        by :meth:`view_foreign_ships`.

        This method doesn't display any incoming ships, regardless of owner, and 
        you can't send ships out from a Space Station.  So this never returns 
        anything but an empty list.

        Included for API completeness.

        Arguments:
            - page_number -- Optional page of results to view.  Defaults to 1.

        Returns a tuple:
            - ships -- list of :class:`lacuna.ship.IncomingShip` objects.
            - number -- total number of incoming ships.
        """
        mylist = []
        for i in kwargs['rslt']['ships_travelling']:
            mylist.append( lacuna.ship.IncomingShip(self.client, i) )
        return (mylist, kwargs['rslt']['number_of_ships_travelling'])


    @lacuna.building.MyBuilding.call_returning_meth
    def view_prisoners( self, page_number:int = 1, **kwargs ):
        """ Shows prisoners, 25 at a time.

        Arguments:
            - page_number -- Optional page of results to view.  Defaults to 1.

        Returns a list of :class:`lacuna.spy.Prisoner` objects.
        """
        mylist = []
        for i in kwargs['rslt']['prisoners']:
            mylist.append( lacuna.spy.Prisoner(self.client, i) )
        return mylist


    @lacuna.building.MyBuilding.call_returning_meth
    def execute_prisoner( self, prisoner_id:int, **kwargs ):
        """ Execute a captured spy

        Arguments:
            - prisoner_id -- Integer ID of the prisoner to execute.

        Returns True on success.
        """
        return True


    @lacuna.building.MyBuilding.call_returning_meth
    def release_prisoner( self, prisoner_id:int, **kwargs ):
        """ Release a captured spy

        This hasn't been tested.  I have not reason to believe it's a problem, 
        but I haven't confirmed otherwise.

        Arguments:
            - prisoner_id -- Integer ID of the prisoner to release.

        Returns True on success.
        """
        return True


    @lacuna.building.MyBuilding.call_returning_meth
    def view_foreign_spies( self, page_number:int = 1, **kwargs ):
        """ Shows foreign spies, 25 at a time.

        Arguments:
            - page_number -- Optional page of results to view.  Defaults to 1.

        Returns a list of :class:`lacuna.spy.ForeignAgent` objects.
        """
        mylist = []
        for i in kwargs['rslt']['spies']:
            mylist.append( lacuna.spy.ForeignAgent(self.client, i) )
        return mylist


