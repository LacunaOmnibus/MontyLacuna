
import lacuna.bc
import lacuna.building
import lacuna.spy

class security(lacuna.building.MyBuilding):
    path = 'security'

    def __init__( self, client, body_id:int = 0, building_id:int = 0 ):
        super().__init__( client, body_id, building_id )

    @lacuna.building.MyBuilding.call_returning_meth
    def view_prisoners( self, page_number:int = 1, *args, **kwargs ):
        """ Lists prisoners currently in jail, 25 per page.

        Arguments:
            - page_number -- Integer ID of the page to view.  Defaults to 1.

        Returns a list of :class:`lacuna.spy.Prisoner` objects.
        """
        prisoner_list = []
        for i in kwargs['rslt']['prisoners']:
            prisoner_list.append( lacuna.spy.Prisoner(self.client, i) )
        return prisoner_list

    @lacuna.bc.LacunaObject.set_empire_status
    @lacuna.building.MyBuilding.call_building_meth
    def release_prisoner( self, prisoner_id:int, *args, **kwargs ):
        """ Releases a prisoner from jail.

        Arguments:
            - prisoner_id -- Integer ID of the prisoner to release.
        """
        pass

    @lacuna.bc.LacunaObject.set_empire_status
    @lacuna.building.MyBuilding.call_building_meth
    def execute_prisoner( self, prisoner_id:int, *args, **kwargs ):
        """ Executes a captured prisoner.

        Arguments:
            - prisoner_id -- Integer ID of the prisoner to execute.

        """
        pass

    @lacuna.building.MyBuilding.call_returning_meth
    def view_foreign_spies( self, page_number:int = 1, *args, **kwargs ):
        """ Lists uncaptured foreign spies, 25 per page.

        Arguments:
            - page_number -- Integer ID of the page to view.  Defaults to 1.

        Lists foreign spies that are on your planet but which you have not 
        captured.  Will only list spies whose level is lower than that of 
        your Security Ministry.  Higher-level spies will remain hidden.

        Returns a list of :class:`lacuna.spy.ForeignAgent` objects.
        """
        foreign_list = []
        for i in kwargs['rslt']['spies']:
            foreign_list.append( lacuna.spy.ForeignAgent(self.client, i) )
        return foreign_list


