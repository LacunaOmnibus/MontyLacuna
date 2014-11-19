
import lacuna.bc
import lacuna.building
import lacuna.ship

class policestation(lacuna.building.MyBuilding):
    path = 'policestation'

    def __init__( self, client, body_id:int = 0, building_id:int = 0 ):
        super().__init__( client, body_id, building_id )

    @lacuna.building.MyBuilding.call_returning_meth
    def view_foreign_ships( self, page_number:int = 1, **kwargs ):
        """ Shows incoming foreign ships, 25 at a time.

        Arguments:
            - page_number -- the page of results to view

        Returns a list of ship.IncomingShip objects.
        """
        mylist = []
        for i in kwargs['rslt']['ships']:
            mylist.append( lacuna.ship.IncomingShip(self.client, i) )
        return mylist
