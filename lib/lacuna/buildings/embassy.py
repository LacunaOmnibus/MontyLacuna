
import lacuna.bc
import lacuna.building

class embassy(lacuna.building.MyBuilding):
    path = 'embassy'

    def __init__( self, client, body_id:int = 0, building_id:int = 0 ):
        super().__init__( client, body_id, building_id )

    @lacuna.building.MyBuilding.call_returning_meth
    def create_alliance( self, alliance_name:str, **kwargs ):
        """ Create a new alliance.

        Returns an embassy.AllianceData object.
        """
        return AllianceData(self.client, kwargs['rslt']['alliance'])

    @lacuna.bc.LacunaObject.set_empire_status
    @lacuna.building.MyBuilding.call_building_meth
    def dissolve_alliance( self, **kwargs ):
        """ Dissolves the current alliance.  This can only be called by the 
        alliance leader.  Any Space Stations still held by the alliance will 
        be converted to asteroids.
        """
        pass

    @lacuna.bc.LacunaObject.set_empire_status
    @lacuna.building.MyBuilding.call_building_meth
    def leave_alliance( self, **kwargs ):
        """ Leaves the current alliance.

        Raises ServerError 1010 if you are the leader of the alliance.  In 
        that case, you cannot leave.  Instead, you must either turn membership 
        over to another member or dissolve the alliance.

        CHECK untested as I can't create an empire on PT.  Should work.
        """
        pass

    @lacuna.building.MyBuilding.call_returning_meth
    def get_alliance_status( self, **kwargs ):
        """ Gets status of your alliance.

        Returns an empire.AllianceData object.
        """
        return AllianceData(self.client, kwargs['rslt']['alliance'])

    @lacuna.bc.LacunaObject.set_empire_status
    @lacuna.building.MyBuilding.call_building_meth
    def send_invite( self, invitee_id:int, message:str = '', **kwargs ):
        """ Invites a player, by ID, to your alliance.
        Raises ServerError 1010 if the invitee is already a member of your 
        alliance.
        The invite is sent in the form of an in-game mail message.  It will 
        appear in your mailbox's Sent tab.
        """
        pass

    @lacuna.building.MyBuilding.call_returning_meth
    def get_pending_invites( self, **kwargs ):
        """ Get list of sent, but not yet accepted, invites.

        Returns a list of InvitedGuest objects.
        """
        mylist = []
        for i in kwargs['rslt']['invites']:
            mylist.append( InvitedGuest(self.client, i) )
        return mylist

    @lacuna.bc.LacunaObject.set_empire_status
    @lacuna.building.MyBuilding.call_building_meth
    def withdraw_invite( self, invite_id:int, message:str = '', **kwargs ):
        """ Withdraws a pending alliance invite."""
        pass

    @lacuna.building.MyBuilding.call_returning_meth
    def get_my_invites( self, **kwargs ):
        """ Gets list of alliance invitations received by your empire.

        Returns a list of AllianceInvited objects.
        """
        mylist = []
        for i in kwargs['rslt']['invites']:
            mylist.append( AllianceInvited(self.client, i) )
        return mylist

    @lacuna.building.MyBuilding.call_returning_meth
    def accept_invite( self, invite_id:int, message:str = '', **kwargs ):
        """ Accepts an alliance invitation.

        Returns an embassy.AllianceData object.
        """
        return AllianceData(self.client, kwargs['rslt']['alliance'])

    @lacuna.bc.LacunaObject.set_empire_status
    @lacuna.building.MyBuilding.call_building_meth
    def reject_invite( self, invite_id:int, message:str = '', **kwargs ):
        """ Rejects an alliance invitation.
        This sends a mail back to the inviting empire letting them know that 
        you're not interested.
        """
        pass

    @lacuna.building.MyBuilding.call_returning_meth
    def assign_alliance_leader( self, empire_id:int, **kwargs ):
        """ Sets a new empire to be the leader of your alliance.  Can only be 
        called by the current alliance leader.

        Returns an embassy.AllianceData object.
        """
        return AllianceData(self.client, kwargs['rslt']['alliance'])

    @lacuna.building.MyBuilding.call_returning_meth
    def update_alliance( self, named_args:dict, **kwargs ):
        """ Updates some settings for your alliance.  Can only be called by the 
        alliance leader.

        Requires a single dict of arguments:
            - forum_uri -- 'http://www.example.com',
            - description -- 'This is a public description',
            - announcements -- 'This is only visible to alliance members',

        Returns an embassy.AllianceData object.
        """
        return AllianceData(self.client, kwargs['rslt']['alliance'])

    @lacuna.bc.LacunaObject.set_empire_status
    @lacuna.building.MyBuilding.call_building_meth
    def expel_member( self, empire_id:int, message:str = '', **kwargs ):
        """ Expels a member from your alliance.  Can only be called by the 
        alliance leader.
        CHECK untested as I can't create an empire on PT.  Should work.
        """
        pass

    @lacuna.building.MyBuilding.call_returning_meth
    def view_stash( self, **kwargs ):
        """ Shows what resources are in the alliance stash.

        Returns an embassy.Stash object.
        """
        return Stash(self.client, kwargs['rslt'])

    @lacuna.building.MyBuilding.call_returning_meth
    def donate_to_stash( self, donation:dict, **kwargs ):
        """ Donate items to the alliance stash.

        Requires a dictionary of items to donate:

::

                {   'apple': 10,
                    'burger': 20, 
                    ...     }

        Waste cannot be donated.

        An alliance stash can hold a maximum of 500,000 units of resources,
        in any combination.  Once the stash has 500,000 resources in it, 
        donation is no longer possible.  At that point, all additions to and 
        removals from the stash must be done by exchange_with_stash().

        Returns an embassy.Stash object.

        Raises ServerError 1009 if the donation would increase the stash to
        more than 500,000 resource units.
        """
        return Stash(self.client, kwargs['rslt'])

    @lacuna.building.MyBuilding.call_returning_meth
    def exchange_with_stash( self, donation:dict, request:dict, **kwargs ):
        """ Exchange equal amounts of your resources with resources currently 
        in the stash.

        The total quantity of resources you wish to donate much exactly match the 
        number of resources you request:

        This is fine:
        - donation = { 'apple': 10, 'burger': 10 }
        - request  = { 'bean': 20 }

        This is not fine:
        - donation = { 'apple': 10, 'burger': 10 }
        - request  = { 'bean': 19 }

        Returns an embassy.Stash object.

        Raises ServerError 1009 if the donation and request quantities do not 
        match, or if you do not have enough resources on hand to cover your 
        specified donation.

        Raises ServerError 1010 if the stash does not contain the requested res.
        """
        return Stash(self.client, kwargs['rslt'])


class AllianceData(lacuna.bc.SubClass):
    """
    Attributes:
        >>> 
        announcements   None,
        date_created    '21 10 2014 21:56:34 +0000',
        description     None,
        forum_uri       None,
        id              '1606',
        leader_id       '23598',
        members         [{'empire_id': '23598', 'name': 'tmtowtdi'}],
        name            'Test Alliance'     },
    """

class InvitedGuest(lacuna.bc.SubClass):
    """ This is an invite your alliance sends out to an empire.

    Attributes:
        >>> 
        id          5810                ID of the invite itself
        empire_id   1234                ID of the invited empire
        name        Invitee One         Name of the invited empire
    """

class AllianceInvited(lacuna.bc.SubClass):
    """ This is an invitation your empire has received from an alliance.

    Attributes:
        >>> 
        id              5810                ID of the invite itself
        alliance_id     1234                ID of the invited empire
        name            United Alliance     Name of the inviting alliance
    """

class Stash():
    """ The current contents of the alliance stash.

    Attributes:
        >>> 
        stash                       Dict of items currently in the stash
                                        {   "gold" : 4500,
                                            "water" : 1000,
                                            ...     }
        stored                      Dict of items currently stored on your planet; these
                                        items can be exchanged with the stash
                                            {   "bauxite" : 5500,
                                                "energy" : 9000,
                                    ...     }
        max_exchange_size           Integer limit you may include in a single 
                                    exchange
        exchanges_remaining_today   Integer number of exchanges you have left 
                                    for the day.
    """

    def __init__( self, client:object, mydict:dict ):
        self.client                     = client
        self.stash                      = mydict['stash']
        self.stored                     = mydict['stored']
        self.max_exchange_size          = mydict['max_exchange_size']
        self.exchanges_remaining_today  = mydict['exchanges_remaining_today']


