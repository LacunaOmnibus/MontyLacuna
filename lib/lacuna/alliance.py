
from lacuna.bc import LacunaObject
from lacuna.exceptions import GDIError

class Alliance(LacunaObject):

    path = 'alliance'

    @LacunaObject.set_empire_status
    @LacunaObject.call_member_meth
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

    @LacunaObject.set_empire_status
    @LacunaObject.call_member_meth
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
    """This allows an empire that's part of an alliance to get info on his
    own alliance without needing to know his own alliance's ID off the top 
    of his head.
            my_all = MyAlliance( client )
    ...etc.  All of the keys returned by Alliance.view_profile() are available.

    The users.Member class has a nice sugar method to make this more OOP-y:
            my_all = client.get_my_alliance()

    Either way, you've now got access to info on your own alliance:
            print( my_all.id )
            print( my_all.name )
        ...etc...
    """

    def __init__( self, client:object ):
        super().__init__(client)

        ### This has always been confusing.
        ###
        ### An Empire object does not know its own alliance.  You've got to 
        ### call the view_public_profile() method, sending the Empire object's 
        ### ID as argument.
        ###
        ### The rv of that view_public_profile() call _will_ contain the 
        ### alliance ID.

        empire_pub = self.client.empire.view_public_profile( self.client.empire.id )
        if 'alliance' not in empire_pub['profile']:
            raise GDIError("Client empire is not in an alliance, so cannot access the MyAlliance class.")
        ally_id = empire_pub['profile']['alliance']['id']

        ally = Alliance( self.client )
        ally_profile = ally.view_profile( ally_id )['profile']

        self.id = ally_profile['id']
        self.name = ally_profile['name']
        self.description = ally_profile['description']
        self.leader_id = ally_profile['leader_id']
        self.date_created = ally_profile['date_created']
        self.members = ally_profile['members']
        self.space_stations = ally_profile['space_stations']
        self.influence = ally_profile['influence']

