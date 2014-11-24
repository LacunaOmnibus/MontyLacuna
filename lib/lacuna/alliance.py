
import lacuna.bc
from lacuna.exceptions import GDIError

class Alliance(lacuna.bc.LacunaObject):
    """ Represents an alliance's publicly-viewable information.
    """

    path = 'alliance'

    @lacuna.bc.LacunaObject.call_returning_meth
    def view_profile( self, alliance_id: int, *args, **kwargs ):
        """ Get publicly-available information on an alliance.

        Requires an integer alliance ID.

        Returns a lacuna.alliance.Profile object.
        """
        return Profile(self.client, kwargs['rslt']['profile'])

    @lacuna.bc.LacunaObject.call_returning_meth
    def find( self, partial_name: str, *args, **kwargs ):
        """ Find alliances by name.

        Requires a standard TLE search string.  See :ref:`glossary`.

        Returns a list of alliance.FoundAlliance objects.
        """
        mylist = []
        for i in kwargs['rslt']['alliances']:
            mylist.append( FoundAlliance(self.client, i) )
        return mylist


class MyAlliance(Alliance):
    """ This is the alliance of which the current empire is a member.

    You'll normally get at this via the clients.Member's get_my_alliance() 
    method:
    ``my_alliance = my_client.get_my_alliance()``

    Attributes::

        id              12345
        name            United Union of Federated Allied Groups
        description     We're an alliance.
        leader_id       67890
        date_created    "01 31 2010 13:09:05 +0000",
        influence       0
        members         List of alliance.Member objects
        space_stations  List of lacuna.body.SpaceStation objects
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
        ally_profile = ally.view_profile( ally_id )

        for i in ['id', 'name', 'description', 'leader_id', 'date_created', 'influence', 'members', 'space_stations' ]:
            setattr(self, i, eval('ally_profile.'+i) )

class FoundAlliance(lacuna.bc.SubClass):
    """ An alliance as returned by find().

    Attributes::

        id          1234
        name        United Union of Federated Allied Groups
    """


class Member(lacuna.bc.SubClass):
    """ An alliance member.

    Attributes::

        id          5810
        name        Member One
    """


class Influence(lacuna.bc.SubClass):
    """ The amount of influence a Space Station has.

    Attributes::

        total   50
        spent   25
    """

class Profile(lacuna.bc.SubClass):
    """
    Attributes::

        id              "id-goes-here",
        name            "Lacuna Expanse Allies",
        description     "Blah blah blah blah...",
        leader_id       "id-goes-here",
        date_created    "01 31 2010 13:09:05 +0600",
        members         List of alliance.Member objects,
        space_stations  List of ship.SpaceStation objects,
        influence       0
    """
    def __init__(self, client, mydict:dict):
        member_list = []
        for i in mydict['members']:
            member_list.append( Member(client, i) )
        mydict['members'] = member_list

        ss_list = []
        for i in mydict['space_stations']:
            ss_list.append( lacuna.body.SpaceStation(client, i) )
        mydict['space_stations'] = ss_list

        super().__init__(client, mydict)

