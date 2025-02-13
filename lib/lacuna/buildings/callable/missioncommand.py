
import lacuna.bc
import lacuna.building

class missioncommand(lacuna.building.MyBuilding):
    path = 'missioncommand'

    def __init__( self, client, body_id:int = 0, building_id:int = 0 ):
        super().__init__( client, body_id, building_id )

    @lacuna.building.MyBuilding.call_returning_meth
    def get_missions( self, *args, **kwargs ):
        """ Returns a list of available missions.
        
        Returns a list of :class:`lacuna.buildings.callable.missioncommand.Mission`
        objects.
        """
        m_list = []
        for m in kwargs['rslt']['missions']:
            m_list.append( Mission(self.client, m) )
        return m_list

    @lacuna.bc.LacunaObject.set_empire_status
    @lacuna.building.MyBuilding.call_building_meth
    def complete_mission( self, mission_id:int, *args, **kwargs ):
        """ Completes a mission.  Delivers rewards to your mission command 
        planet immediately, and causes this mission to not show up again for 30 
        days.

        Arguments:
            - mission_id -- Integer ID of the mission to complete.

        If you have not completed the tasks, or have on hand the resources, 
        required by the listed objectives of the mission, calling this will 
        fail by raising :class:`lacuna.exceptions.ServerError` 1002.
        """
        pass

    @lacuna.bc.LacunaObject.set_empire_status
    @lacuna.building.MyBuilding.call_building_meth
    def skip_mission( self, mission_id:int, *args, **kwargs ):
        """ Skips a mission, removing it from the list and keeping it from 
        showing up again for 30 days.

        Arguments:
            - mission_id -- Integer ID of the mission to skip.
        """
        pass


class Mission(lacuna.bc.SubClass):
    """ 
    Attributes::

        id                      Integer ID of the mission.
        name                    String.
        description             String.
        date_posted             Datetime string 
                                eg '24 10 2014 20:03:27 +0000'
        max_university_level    Integer.  Empires with a higher uni level 
                                cannot complete this mission.
        objectives              List of string descriptions of all tasks 
                                that must be completed.
        rewards
                                List of string descriptions of the rewards 
                                for completing the mission

    """
