
import lacuna.bc
import lacuna.building

"""
Be aware of the ID arguments in these methods.  In some cases, the ID argument 
must be the ID of an empire (eg send_invite()), but in other cases, the ID 
argument is the ID of the invitation itself (eg withdraw_invite()).

"invitee_id" == the ID of an empire.  "invite_id" == the ID of an invitation 
itself.  

Invitation IDs can be obtained via get_pending_invites().
"""

class embassy(lacuna.building.MyBuilding):
    path = 'embassy'

    def __init__( self, client, body_id:int = 0, building_id:int = 0 ):
        super().__init__( client, body_id, building_id )

    @lacuna.bc.LacunaObject.set_empire_status
    @lacuna.building.MyBuilding.call_building_meth
    def create_alliance( self, alliance_name:str, **kwargs ):
        """ Create a new alliance.

        Retval contains key 'alliance':
            {       'announcements': None,
                    'date_created': '21 10 2014 21:56:34 +0000',
                    'description': None,
                    'forum_uri': None,
                    'id': '1606',
                    'leader_id': '23598',
                    'members': [{'empire_id': '23598', 'name': 'tmtowtdi'}],
                    'name': 'Test Alliance'     },

        Raises ServerError 1010 if you're already in an alliance.
        """
        pass

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

    @lacuna.bc.LacunaObject.set_empire_status
    @lacuna.building.MyBuilding.call_building_meth
    def get_alliance_status( self, **kwargs ):
        """ Gets status of your alliance.

        Retval includes key 'alliance':
                {   'announcements': None,
                    'date_created': '21 10 2014 22:01:02 +0000',
                    'description': None,
                    'forum_uri': '',
                    'id': '1607',
                    'leader_id': '23598',
                    'members': [{'empire_id': '23598', 'name': 'tmtowtdi'}],
                    'name': 'My Test Alliance'  },
        """
        pass

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

    @lacuna.bc.LacunaObject.set_empire_status
    @lacuna.building.MyBuilding.call_building_meth
    def get_pending_invites( self, **kwargs ):
        """ Get list of sent, but not yet accepted, invites.

        Retval contains key 'invites':
                [   {'empire_id': '1234', 'id': '5810', 'name': 'Invitee One'},
                    {'empire_id': '5678', 'id': '5811', 'name': 'Invitee Two'}   ]

            'id' is the ID of the invite itself, and is what must be passed to 
            withdraw_invite().
        """
        pass

    @lacuna.bc.LacunaObject.set_empire_status
    @lacuna.building.MyBuilding.call_building_meth
    def withdraw_invite( self, invite_id:int, message:str = '', **kwargs ):
        """ Withdraws a pending alliance invite."""
        pass

    @lacuna.bc.LacunaObject.set_empire_status
    @lacuna.building.MyBuilding.call_building_meth
    def get_my_invites( self, **kwargs ):
        """ Gets list of alliance invitations received by your empire.
        CHECK untested as I can't create an empire on PT.  Should work.
        """
        pass

    @lacuna.bc.LacunaObject.set_empire_status
    @lacuna.building.MyBuilding.call_building_meth
    def accept_invite( self, invite_id:int, message:str = '', **kwargs ):
        """ Accepts an alliance invitation.
        CHECK untested as I can't create an empire on PT.  Should work.
        """
        pass

    @lacuna.bc.LacunaObject.set_empire_status
    @lacuna.building.MyBuilding.call_building_meth
    def reject_invite( self, invite_id:int, message:str = '', **kwargs ):
        """ Rejects an alliance invitation.
        CHECK untested as I can't create an empire on PT.  Should work.
        """
        pass

    @lacuna.bc.LacunaObject.set_empire_status
    @lacuna.building.MyBuilding.call_building_meth
    def assign_alliance_leader( self, empire_id:int, **kwargs ):
        """ Sets a new empire to be the leader of your alliance.  Can only be 
        called by the current alliance leader.
        CHECK untested as I can't create an empire on PT.  Should work.
        """
        pass

    @lacuna.bc.LacunaObject.set_empire_status
    @lacuna.building.MyBuilding.call_building_meth
    def update_alliance( self, named_args:dict, **kwargs ):
        """ Updates some settings for your alliance.  Can only be called by the 
        alliance leader.

        named_args is a dict:
                {
                    'forum_uri': 'http://www.example.com',
                    'description': 'This is a public description',
                    'announcements': 'This is only visible to alliance members',
                }
        """
        pass

    @lacuna.bc.LacunaObject.set_empire_status
    @lacuna.building.MyBuilding.call_building_meth
    def expel_member( self, empire_id:int, message:str = '', **kwargs ):
        """ Expels a member from your alliance.  Can only be called by the 
        alliance leader.
        CHECK untested as I can't create an empire on PT.  Should work.
        """
        pass

    @lacuna.bc.LacunaObject.set_empire_status
    @lacuna.building.MyBuilding.call_building_meth
    def view_stash( self, **kwargs ):
        """ Shows what resources are in the alliance stash.

        Retval contains:
            'stash' - dict of resources in the stash now.
                { energy: 1000,
                    water: 2000,
                    ...     }
            'stored' - dict of resources currently on the planet where your 
            embassy is; these resources are available to be added to the stash.
        """
        pass

    @lacuna.bc.LacunaObject.set_empire_status
    @lacuna.building.MyBuilding.call_building_meth
    def donate_to_stash( self, donation:dict, **kwargs ):
        """ Donate items to the alliance stash.

        donation is a struct of resource: quantity:
                donation = { 'apple': 10, 'burger': 20, ... }

        Waste cannot be donated.

        An alliance stash can hold a maximum of 500,000 units of resources,
        in any combination.  Once the stash has 500,000 resources in it, 
        donation is no longer possible.  At that point, all additions to and 
        removals from the stash must be done by exchange_with_stash().

        Retval contains 'stash', as documented in view_stash().  The returned 
        stash includes your donation.

        Raises ServerError 1009 if the donation would increase the stash to
        more than 500,000 resource units.
        """
        pass

    @lacuna.bc.LacunaObject.set_empire_status
    @lacuna.building.MyBuilding.call_building_meth
    def exchange_with_stash( self, donation:dict, request:dict, **kwargs ):
        """ Exchange equal amounts of your resources with resources currently 
        in the stash.

        The total quantity of resources you wish to donate much exactly match the 
        number of resources you request:

            ### Fine
            donation = { 'apple': 10, 'burger': 10 }
            request  = { 'bean': 20 }

            ### Not Fine
            donation = { 'apple': 10, 'burger': 10 }
            request  = { 'bean': 19 }

        Raises ServerError 1009 if the donation and request quantities do not 
        match, or if you do not have enough resources on hand to cover your 
        specified donation.

        Raises ServerError 1010 if the stash does not contain the requested res.
        """
        pass


class CreatedAlliance(lacuna.bc.SubClass):
    """
    Attributes:
        announcements   None,
        date_created    '21 10 2014 21:56:34 +0000',
        description     None,
        forum_uri       None,
        id              '1606',
        leader_id       '23598',
        members         [{'empire_id': '23598', 'name': 'tmtowtdi'}],
        name            'Test Alliance'     },
    """




