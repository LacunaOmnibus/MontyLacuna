
import lacuna.bc
from lacuna.exceptions import GDIError

class Alliance(lacuna.bc.LacunaObject):

    path = 'alliance'

    @lacuna.bc.LacunaObject.set_empire_status
    @lacuna.bc.LacunaObject.call_member_meth
    def view_profile( self, alliance_id:int, *args, **kwargs ):
        """Returns publicly-accessible data about the alliance.

        rv['profile'] = {
            "id" : "id-goes-here",
            "name" : "Lacuna Expanse Allies",
            "description" : "Blah blah blah blah...",
            "leader_id" : "id-goes-here",
            "date_created" : "01 31 2010 13:09:05 +0600",
            "members" : [
                {
                    "id" : "id-goes-here",
                    "name" : "Lacuna Expanse Corp"
                },
                ...
            ],
            "space_stations" : [
                {
                    "id" : "id-goes-here",
                    "name" : "The Life Star",
                    "x" : -342,
                    "y" : 128
                },
                ...
            ],
            "influence" : 0
        }
        """
        pass

    @lacuna.bc.LacunaObject.set_empire_status
    @lacuna.bc.LacunaObject.call_member_meth
    def find( self, partial_name:str, *args, **kwargs ):
        """partial_name must be at least 3 characters.  Matches alliances whose names
        START with partial_name (NOT those whose names just contain partial_name).

        TLE documentation does not mention a limit on number of alliances returned.
        A limit of 25 is common with the TLE API, but the docs don't mention it in
        this case, and there's currently no three letter string that would match 
        more than 25 alliances so there's no way to test.

        rv['alliances'] is a list of structs:
            [
                {
                    "id": "1234",
                    "name": "Some alliance name"
                },
                ...etc...
            ]
        """
        pass


class MyAlliance(Alliance):
    """ This is the alliance of which the current empire is a member.

    You'll normally get at this via the clients.Member's get_my_alliance() 
    method:
            my_alliance = my_client.get_my_alliance()

    Attributes:
        id              12345
        name            United Union of Federated Allied Groups
        description     We're an alliance.
        leader_id       67890
        date_created    "01 31 2010 13:09:05 +0000",
        influence       0
        members         List of alliance.Member objects
        space_stations  List of alliance.SpaceStation objects
    """

    def __init__( self, client:object ):
        super().__init__(client)

        ### This has always been confusing.
        ###
        ### An Empire object does not know its own alliance.  You've got to 
        ### call Empire.view_public_profile() method, sending the Empire 
        ### object's ID as argument.
        ###
        ### The rv of that view_public_profile() call _will_ contain the 
        ### alliance ID.

        empire_pub = self.client.empire.view_public_profile( self.client.empire.id )
        if not hasattr(empire_pub, 'alliance'):
            raise GDIError("Client empire is not in an alliance, so cannot access the MyAlliance class.")
        ally_id = empire_pub.alliance['id']

        ally = Alliance( self.client )
        ally_profile = ally.view_profile( ally_id )['profile']

        for i in ['id', 'name', 'description', 'leader_id', 'date_created', 'influence' ]:
            setattr(self, i, ally_profile[i])

        member_list = []
        for i in ally_profile['members']:
            member_list.append( Member(self.client, i) )
        self.members = member_list

        ss_list = []
        for i in ally_profile['space_stations']:
            ss_list.append( SpaceStation(self.client, i) )
        self.space_stations = ss_list

class Member(lacuna.bc.SubClass):
    """ An alliance member.

    Attributes:
        id          5810
        name        Invitee One
    """

class SpaceStation(lacuna.bc.SubClass):
    """ An alliance-owned space station.

    Attributes:
        id          12345
        name        Satellite of Love
        x           10
        y           -10
    """



