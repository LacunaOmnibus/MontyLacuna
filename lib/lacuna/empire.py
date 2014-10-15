
import pprint, re
from lacuna.bc import LacunaObject

class Empire(LacunaObject):
    """A generic Empire object that can be used with a non-logged-in Guest."""

    path = 'empire'

    ### All of these relate to creating a new empire.  I don't see any burning 
    ### need to create a new empire with Python, and the thought of testing 
    ### this out by creating a bunch of new empires is making me sad.  So I'm 
    ### punting.
    def create(self, *args, **kwargs):
        raise NotImplementedError( "Creating an empire is not implemented." )
    def found(self, *args, **kwargs):
        raise NotImplementedError( "Founding an empire is not implemented." )
    def update_species(self, *args, **kwargs):
        raise NotImplementedError( "Updating a species is not implemented." )

    @LacunaObject.call_guest_meth
    def fetch_captcha( self ):
        """Returns dict containing 'guid' and 'url' keys
        DICT not OBJ, so rv['guid'], not rv.guid
        """
        pass


class MyEmpire( Empire ):
    """The Empire object belonging to the current Member's empire."""

    pp = pprint.PrettyPrinter( indent = 4 )

    ### These appear in users.py, not here:
    ###     login()
    ###     send_password_reset_message()
    ###
    ### Involves email, which the server isn't producing, so skipping:
    ###     reset_password()

    @LacunaObject.call_member_meth
    def logout( self ):
        pass

    @LacunaObject.set_status
    @LacunaObject.call_member_meth
    def get_status( self ):
        """rv['empire'] is a struct with these keys:
            name
            status_message
            planets
            rpc_count
            is_isolationist
            tech_level
            self_destruct_active
            self_destruct_date
            essentia
            home_planet_id
            id
            has_new_messages
        """
        pass

    @LacunaObject.set_status
    @LacunaObject.call_member_meth
    def get_invite_friend_url( self ):
        """See the 'referral_url' key in the returned dict."""
        pass

    @LacunaObject.set_status
    @LacunaObject.call_member_meth
    def invite_friend( self, email, message="" ):
        """Doesn't error, but doesn't send email either.  Since the 'forgot my password' feature
        is exhibiting the same behavior, I'm going to assume the server just isn't sending mail
        anymore."""
        pass

    @LacunaObject.set_status
    @LacunaObject.call_member_meth
    def view_profile( self ):
        """Throws 1015 (Sitters cannot modify preferences) if the user is logged in with 
        their sitter.
        Yes, I know - 'view' does not imply 'modify'.  That's still the exception thrown.
        """
        pass

    @LacunaObject.set_status
    @LacunaObject.call_member_meth
    def view_public_profile( self, empire_id:int ):
        """rv['profile'] contains the keys:
            description
            country
            status_message
            alliance
            medals
            skype
            known_colonies
            name
            player_name
            species
            date_founded
            city
            id
            last_login
            colony_count
        """
        pass

    @LacunaObject.call_member_meth
    def edit_profile( self, profile:dict ):
        """The rv does contain a 'status' dict, but it's in a different format from what's 
        expected, so skip the set_status decorator.

        Valid keys for profile dict (incoming arg):
            description
            email
            sitter_password
            status_message
            city
            country
            notes
            skype
            player_name
            public_medals (list of medal IDs to display)

            The following are all booleans, indicating whether to skip a given warning or
            game-generated mail.

            skip_happiness_warnings
            skip_resource_warnings
            skip_pollution_warnings
            skip_medal_messages
            skip_facebook_wall_posts
            skip_found_nothing
            skip_excavator_resources
            skip_excavator_glyph
            skip_excavator_plan
            skip_spy_recovery
            skip_probe_detected
            skip_attack_messages
            skip_incoming_ships
        """
        pass

    @LacunaObject.set_status
    @LacunaObject.call_member_meth
    def change_password( self, oldpw:str, newpw:str ):
        pass

    @LacunaObject.set_status
    @LacunaObject.call_member_meth
    def find( self, name_segment:str ):
        """name_segment must be at least three letters long.  All empires that match
        (where "match" means "whose names start with that string, case-INsensitive")
        will be returned.
        
        rv includes 'empires' key, which contains:
            {id: 1234, name: 'empire name 1'},
            {id: 5678, name: 'empire name 2'},
            ...
            {id: 9999, name: 'empire name N'},
            
        """
        pass

    @LacunaObject.set_status
    @LacunaObject.call_member_meth
    def set_status_message( self, message:str ):
        pass

    @LacunaObject.set_status
    @LacunaObject.call_member_meth
    def view_boosts( self ):
        """See the 'boosts' key in the retval."""
        pass

    @LacunaObject.set_status
    @LacunaObject.call_member_meth
    def boost_storage( self ):
        pass

    @LacunaObject.set_status
    @LacunaObject.call_member_meth
    def boost_food( self ):
        pass

    @LacunaObject.set_status
    @LacunaObject.call_member_meth
    def boost_water( self ):
        pass

    @LacunaObject.set_status
    @LacunaObject.call_member_meth
    def boost_energy( self ):
        pass

    @LacunaObject.set_status
    @LacunaObject.call_member_meth
    def boost_ore( self ):
        pass

    @LacunaObject.set_status
    @LacunaObject.call_member_meth
    def boost_happiness( self ):
        pass

    @LacunaObject.set_status
    @LacunaObject.call_member_meth
    def boost_building( self ):
        pass

    @LacunaObject.set_status
    @LacunaObject.call_member_meth
    def spy_training_boost( self ):
        pass

    ### Commenting this out because, right now, disable_self_destruct() does 
    ### not work, server side.  It's a known problem.  Being able to turn on 
    ### the suicide button but not being able to turn it back off again is a 
    ### tiny bit of a BIG FUCKING PROBLEM.
    #@LacunaObject.set_status
    #@LacunaObject.call_member_meth
    #def enable_self_destruct( self ):
    #    pass

    @LacunaObject.set_status
    @LacunaObject.call_member_meth
    def disable_self_destruct( self ):
        pass

    @LacunaObject.set_status
    @LacunaObject.call_member_meth
    def redeem_essentia_code( self, code ):
        ### Untested; I have no E codes to try this out with, and I'm not 
        ### spending money to test.
        pass

    @LacunaObject.set_status
    @LacunaObject.call_member_meth
    def redefine_species_limits( self ):
        """Just returns some info about the current limits on the current user's
        ability to redefine their species.

        'can': 1,
        'essentia_cost': 100,
        'max_orbit': '3',
        'min_growth': 1,
        'min_orbit': '3',
        'reason': None,

        'can' will be 0 if the user currently cannot redefine.
        I do not understand why the min/max settings exist.
        If 'can' is false, 'reason' will contain a string explaining why 
        not.  eg "You have already redefined in the past 30 days", etc.
        """
        pass

    @LacunaObject.set_status
    @LacunaObject.call_member_meth
    def redefine_species( self, params ):
        """Actually does the deed of redefining a player's species.
        Costs E, so untested.

        I assume that params are the items mentioned in redefine_species_limits().
        """
        pass

    @LacunaObject.set_status
    @LacunaObject.call_member_meth
    def view_species_stats( self ):
        """name, description, various affinities"""
        pass

    @LacunaObject.call_member_meth
    def get_species_templates( self ):
        """Returns the species templates that are presented to a new player upon
        initial species creation (Average, Warmonger, Resilient, Viral, etc)
        Does not return a status block, so no set_status decorator.
        """
        pass

