
import lacuna.bc
import lacuna.building

class embassy(lacuna.building.MyBuilding):
    path = 'embassy'

    def __init__( self, client, body_id:int = 0, building_id:int = 0 ):
        super().__init__( client, body_id, building_id )

    @lacuna.building.MyBuilding.call_returning_meth
    def create_alliance( self, alliance_name:str, **kwargs ):
        """ Create a new alliance.

        Arguments:
            alliance_name (str): String name of the new alliance.

        Returns:
            alliance (lacuna.buildings.callable.embassy.AllianceData):
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

        Raises:
            (lacuna.exceptions.ServerError) 1010 if you are the leader of the 
            alliance.  In that case, you cannot leave.  Instead, you must 
            either turn membership over to another member or dissolve the 
            alliance.
        """
        pass

    @lacuna.building.MyBuilding.call_returning_meth
    def get_alliance_status( self, **kwargs ):
        """ Gets status of your alliance.

        Returns:
            status (AllianceData):
        """
        return AllianceData(self.client, kwargs['rslt']['alliance'])

    @lacuna.bc.LacunaObject.set_empire_status
    @lacuna.building.MyBuilding.call_building_meth
    def send_invite( self, invitee_id:int, message:str = '', **kwargs ):
        """ Invites a player, by ID, to your alliance.

        Arguments:
            invite_id (int): ID of the player to invite.  

        Raises:
            Error (:class:`lacuna.exceptions.ServerError`): 1010 if
                                                            the invitee is already a member of your 
                                                            alliance.  The invite is sent in the 
                                                            form of an in-game mail message.  It 
                                                            will appear in your mailbox's Sent tab.
        """
        pass

    @lacuna.building.MyBuilding.call_returning_meth
    def get_pending_invites( self, **kwargs ):
        """ Get list of sent, but not yet accepted, invites.

        Returns:
            invites (InvitedGuest): list of objects.
        """
        mylist = []
        for i in kwargs['rslt']['invites']:
            mylist.append( InvitedGuest(self.client, i) )
        return mylist

    @lacuna.bc.LacunaObject.set_empire_status
    @lacuna.building.MyBuilding.call_building_meth
    def withdraw_invite( self, invite_id:int, message:str = '', **kwargs ):
        """ Withdraws a pending alliance invite.

        Arguments:
            invite_id (int): ID of the invitation to withdraw.
            message (str): message that will be sent to the user explaining why their invite was
                           withdrawn.

        See also :py:meth:`get_my_invites`
        """
        pass

    @lacuna.building.MyBuilding.call_returning_meth
    def get_my_invites( self, **kwargs ):
        """ Gets list of alliance invitations received by your empire.

        Returns:
            invites (AllianceInvited): list of objects
        """
        mylist = []
        for i in kwargs['rslt']['invites']:
            mylist.append( AllianceInvited(self.client, i) )
        return mylist

    @lacuna.building.MyBuilding.call_returning_meth
    def accept_invite( self, invite_id:int, message:str = '', **kwargs ):
        """ Accepts an alliance invitation.

        Arguments:
            invite_id (int): ID of the invitation to accept.  See
                             :py:meth:`get_my_invites`

        Returns:
            alliance (AllianceData):
        """
        return AllianceData(self.client, kwargs['rslt']['alliance'])

    @lacuna.bc.LacunaObject.set_empire_status
    @lacuna.building.MyBuilding.call_building_meth
    def reject_invite( self, invite_id:int, message:str = '', **kwargs ):
        """ Rejects an alliance invitation.

        Arguments:
            invite_id (int): ID of the invitation to reject.
            message (str): message to be sent to the alliance leader about why you're rejecting the
                           invitation.

        This sends a mail back to the inviting empire letting them know that 
        you're not interested.
        """
        pass

    @lacuna.building.MyBuilding.call_returning_meth
    def assign_alliance_leader( self, empire_id:int, **kwargs ):
        """ Sets a new empire to be the leader of your alliance.  Can only be 
        called by the current alliance leader.

        Arguments:
            empire_id (int): ID of the empire that should become the new leader.

        Returns:
            alliance (AllianceData):
        """
        return AllianceData(self.client, kwargs['rslt']['alliance'])

    @lacuna.building.MyBuilding.call_returning_meth
    def update_alliance( self, named_args:dict, **kwargs ):
        """ Updates some settings for your alliance.  Can only be called by the 
        alliance leader.

        Arguments:
            args (dict): Containing the keys ``forum_uri``, ``description``, and ``annonucements``.
        Returns:
            alliance (AllianceData):
        """
        return AllianceData(self.client, kwargs['rslt']['alliance'])

    @lacuna.bc.LacunaObject.set_empire_status
    @lacuna.building.MyBuilding.call_building_meth
    def expel_member( self, empire_id:int, message:str = '', **kwargs ):
        """ Expels a member from your alliance.  Can only be called by the 
        alliance leader.

        Arguments:
            empire_id (int): ID of the empire to expel.
            message (str): message about why the member is being removed from the alliance.
        """
        pass

    @lacuna.building.MyBuilding.call_returning_meth
    def view_stash( self, **kwargs ):
        """ Shows what resources are in the alliance stash.

        Returns:
            stash (Stash):
        """
        return Stash(self.client, kwargs['rslt'])

    @lacuna.building.MyBuilding.call_returning_meth
    def donate_to_stash( self, donation:dict, **kwargs ):
        """ Donate items to the alliance stash.

        Arguments:
            donation (dict): items to donate.  Key is the string name of the item, value is the
                             integer quantity to donate.
        Returns:
            stash (Stash):
        Raises:
            Error (:class:`lacuna.exceptions.ServerError`): 1009 if the donation would increase the
                                                            stash to more than 500,000 resource 
                                                            units.

        Waste cannot be donated.

        An alliance stash can hold a maximum of 500,000 units of resources,
        in any combination.  Once the stash has 500,000 resources in it, 
        donation is no longer possible.  At that point, all additions to and 
        removals from the stash must be done by :py:meth:`exchange_with_stash`.
        """
        return Stash(self.client, kwargs['rslt'])

    @lacuna.building.MyBuilding.call_returning_meth
    def exchange_with_stash( self, donation:dict, request:dict, **kwargs ):
        """ Exchange equal amounts of your resources with resources currently 
        in the stash.

        Arguments:
            donation (dict): ``str name => int quantity`` (to donate)
            request (dict): ``str name => int quantity`` (to receive)
        Returns:
            stash (Stash):
        Raises:
            1009 (:class:`lacuna.exceptions.ServerError`): if the donation and request quantities do
                                                           not match, or if you do not have enough 
                                                           resources on hand to cover your specified 
                                                           donation.
            1010 (:class:`lacuna.exceptions.ServerError`): if the stash does not contain the
                                                           requested res.

        The total quantity of resources you wish to donate much exactly match the number of 
        resources you request:

        This is fine:
            - ``donation = { 'apple': 10, 'burger': 10 }``
            - ``request  = { 'bean': 20 }``

        This is not fine:
            - ``donation = { 'apple': 10, 'burger': 10 }``
            - ``request  = { 'bean': 19 }``

        """
        return Stash(self.client, kwargs['rslt'])


class AllianceData(lacuna.bc.SubClass):
    """
    Object Attributes::

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

    Object Attributes::

        id          Integer ID of the invite itself
        empire_id   Integer ID of the invited empire
        name        Name of the invited empire
    """

class AllianceInvited(lacuna.bc.SubClass):
    """ This is an invitation your empire has received from an alliance.

    Object Attributes::

        id              Integer ID of the invite itself
        alliance_id     Integer ID of the invited empire
        name            Name of the inviting alliance
    """

class Stash():
    """ The current contents of the alliance stash.

    Object Attributes::

        stash                       Dict of items currently in the stash.  Key
                                    is item name ("gold", "water", etc), value 
                                    is integer quantity stored.
        stored                      Dict of items currently stored on your
                                    planet that can be exchanged with the 
                                    stash.  ``Item_name => quantity``.
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


