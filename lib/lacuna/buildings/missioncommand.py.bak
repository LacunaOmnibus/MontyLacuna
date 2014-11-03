
from lacuna.bc import LacunaObject
from lacuna.building import Building

class missioncommand(Building):
    path = 'missioncommand'

    def __init__( self, client, body_id:int = 0, building_id:int = 0 ):
        super().__init__( client, body_id, building_id )

    @Building.call_returning_meth
    def get_missions( self, *args, **kwargs ):
        """ Returns a list of available missions.
        
        Retval is a list of Mission objects.
        """
        m_list = []
        for m in kwargs['rslt']['missions']:
            m_list.append( Mission(m) )
        return m_list

    @LacunaObject.set_empire_status
    @Building.call_building_meth
    def complete_mission( self, mission_id:int, *args, **kwargs ):
        """ Completes a mission.  Delivers rewards to your mission command 
        planet immediately, and causes this mission to not show up again for 30 
        days.

        Requires 'mission_id', integer ID of the mission to complete.

        If you have not completed the tasks, or have on hand the resources, 
        required by the listed objectives of the mission, calling this will 
        fail by raising ServerError 1002.

        Otherwise, returns a standard status dict.
        """
        pass

    @LacunaObject.set_empire_status
    @Building.call_building_meth
    def skip_mission( self, mission_id:int, *args, **kwargs ):
        """ Skips a mission, removing it from the list and keeping it from 
        showing up again for 30 days.

        Requires 'mission_id', integer ID of the mission to complete.

        Returns a standard status dict.
        """
        pass


class Mission():
    """ A mission has the attributes:
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
    def __init__( self, miss:dict ):
        for n, v in miss.items():
            setattr(self, n, v)

