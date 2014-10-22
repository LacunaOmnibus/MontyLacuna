
import pprint, re
from lacuna.bc import LacunaObject

"""
    An Empire object is not logged in, and is meant for use only by new users 
    who need to fetch a captcha or check if a given empire name is available 
    in the process of creating an account.

    Most of the time, your Empire object will be a MyEmpire object, which will 
    contain the following attributes:

        "id" : "xxxx",
        "rpc_count" : 321, # the number of calls made to the server
        "is_isolationist" : 1, # hasn't sent out probes or colony ships
        "name" : "The Syndicate",
        "status_message" : "A spy's work is never done.",
        "home_planet_id" : "id-goes-here",
        "has_new_messages" : 4,
        "latest_message_id" : 1234,
        "essentia" : 0,
        "planets" : {
            "id-goes-here" : "Earth",
            "id-goes-here" : "Mars
        },
        "tech_level"           : 20,  # Highests level university has gotten to.
        "self_destruct_active" : 0,
        "self_destruct_date" : ""
"""

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

        There also exists a Captcha class, which requires the user to already 
        be logged in.  This fetch_captcha method exists to allow a brand new, 
        not-yet-logged-in user to get a captcha, the solution to which they 
        can pass to create().

        If you're looking for a captcha for anything other than new user 
        creation, go use the Captcha class.
        """
        pass



"""
TBD

It might be nice to have a class object "station_re" or some such:
    station_re = '^\wASS'

...and then have a method to separate known stations from planets:
    def get_planets_not_stations:
        for id, name in self.planets.items():
            if re.match(self.station_re, name):
                continue
            print( "{} is id {}".format(name, id) )

"""

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
    def logout( self, *args, **kwargs ):
        pass

    @LacunaObject.set_empire_status
    @LacunaObject.call_member_meth
    def get_status( self, *args, **kwargs ):
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

    @LacunaObject.set_empire_status
    @LacunaObject.call_member_meth
    def get_invite_friend_url( self, *args, **kwargs ):
        """See the 'referral_url' key in the returned dict."""
        pass

    @LacunaObject.set_empire_status
    @LacunaObject.call_member_meth
    def invite_friend( self, email, message="", *args, **kwargs ):
        """Doesn't error, but doesn't send email either.  Since the 'forgot my password' feature
        is exhibiting the same behavior, I'm going to assume the server just isn't sending mail
        anymore."""
        pass

    @LacunaObject.set_empire_status
    @LacunaObject.call_member_meth
    def view_profile( self, *args, **kwargs ):
        """Throws 1015 (Sitters cannot modify preferences) if the user is logged in with 
        their sitter.
        Yes, I know - 'view' does not imply 'modify'.  That's still the exception thrown.
        """
        pass

    @LacunaObject.set_empire_status
    @LacunaObject.call_member_meth
    def view_public_profile( self, empire_id:int, *args, **kwargs ):
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
    def edit_profile( self, profile:dict, *args, **kwargs ):
        """The rv does contain a 'status' dict, but it's in a different format from what's 
        expected, so skip the set_empire_status decorator.

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

    @LacunaObject.set_empire_status
    @LacunaObject.call_member_meth
    def change_password( self, oldpw:str, newpw:str, *args, **kwargs ):
        pass

    @LacunaObject.set_empire_status
    @LacunaObject.call_member_meth
    def find( self, name_segment:str, *args, **kwargs ):
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

    @LacunaObject.set_empire_status
    @LacunaObject.call_member_meth
    def set_status_message( self, message:str, *args, **kwargs ):
        pass

    @LacunaObject.set_empire_status
    @LacunaObject.call_member_meth
    def view_boosts( self, *args, **kwargs ):
        """See the 'boosts' key in the retval."""
        pass

    @LacunaObject.set_empire_status
    @LacunaObject.call_member_meth
    def boost_storage( self, *args, **kwargs ):
        pass

    @LacunaObject.set_empire_status
    @LacunaObject.call_member_meth
    def boost_food( self, *args, **kwargs ):
        pass

    @LacunaObject.set_empire_status
    @LacunaObject.call_member_meth
    def boost_water( self, *args, **kwargs ):
        pass

    @LacunaObject.set_empire_status
    @LacunaObject.call_member_meth
    def boost_energy( self, *args, **kwargs ):
        pass

    @LacunaObject.set_empire_status
    @LacunaObject.call_member_meth
    def boost_ore( self, *args, **kwargs ):
        pass

    @LacunaObject.set_empire_status
    @LacunaObject.call_member_meth
    def boost_happiness( self, *args, **kwargs ):
        pass

    @LacunaObject.set_empire_status
    @LacunaObject.call_member_meth
    def boost_building( self, *args, **kwargs ):
        pass

    @LacunaObject.set_empire_status
    @LacunaObject.call_member_meth
    def spy_training_boost( self, *args, **kwargs ):
        pass

    ### Commenting this out because, right now, disable_self_destruct() does 
    ### not work, server side.  It's a known problem.  Being able to turn on 
    ### the suicide button but not being able to turn it back off again is a 
    ### tiny bit of a BIG FUCKING PROBLEM.
    #@LacunaObject.set_empire_status
    #@LacunaObject.call_member_meth
    #def enable_self_destruct( self, *args, **kwargs ):
    #    pass

    @LacunaObject.set_empire_status
    @LacunaObject.call_member_meth
    def disable_self_destruct( self, *args, **kwargs ):
        pass

    @LacunaObject.set_empire_status
    @LacunaObject.call_member_meth
    def redeem_essentia_code( self, code, *args, **kwargs ):
        ### Untested; I have no E codes to try this out with, and I'm not 
        ### spending money to test.
        pass

    @LacunaObject.set_empire_status
    @LacunaObject.call_member_meth
    def redefine_species_limits( self, *args, **kwargs ):
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

    @LacunaObject.set_empire_status
    @LacunaObject.call_member_meth
    def redefine_species( self, params, *args, **kwargs ):
        """Actually does the deed of redefining a player's species.
        Costs E, so untested.

        I assume that params are the items mentioned in redefine_species_limits().
        """
        pass

    @LacunaObject.set_empire_status
    @LacunaObject.call_member_meth
    def view_species_stats( self, *args, **kwargs ):
        """name, description, various affinities"""
        pass

    @LacunaObject.call_member_meth
    def get_species_templates( self, *args, **kwargs ):
        """Returns the species templates that are presented to a new player upon
        initial species creation (Average, Warmonger, Resilient, Viral, etc)
        Does not return a status block, so no set_empire_status decorator.
        """
        pass

