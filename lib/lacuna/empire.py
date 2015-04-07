
import pprint, re
import lacuna.bc

class Empire(lacuna.bc.LacunaObject):
    """ A generic Empire object that can be used with a non-logged-in Guest."""

    path = 'empire'

    ### All of these relate to creating a new empire.  I don't see any burning 
    ### need to create a new empire with Python, and the thought of testing 
    ### this out by creating a bunch of new empires is making me sad.  So I'm 
    ### punting.
    def create(self, *args, **kwargs):
        """ Unimplemented.  It's assumed nobody is going to use MontyLacuna to 
        create a new empire.
        """
        raise NotImplementedError( "Creating an empire is not implemented." )
    def found(self, *args, **kwargs):
        """ Unimplemented.  It's assumed nobody is going to use MontyLacuna to 
        create a new empire.
        """
        raise NotImplementedError( "Founding an empire is not implemented." )
    def update_species(self, *args, **kwargs):
        """ Unimplemented.  It's assumed nobody is going to use MontyLacuna to 
        create a new empire.
        """
        raise NotImplementedError( "Updating a species is not implemented." )

    @lacuna.bc.LacunaObject.call_guest_meth
    def fetch_captcha( self, *args, **kwargs ):
        """ Get location of a captcha puzzle to solve.
        
        There also exists a Captcha class, which requires the user to already 
        be logged in.  This fetch_captcha method exists to allow a brand new, 
        not-yet-logged-in user to get a captcha, the solution to which they 
        can pass to :meth:`create`.

        Since :meth:`create` is unimplemented, you should probably never use 
        this for anything.

        If you're looking for a captcha for anything other than new user 
        creation, go use the Captcha class.

        Returns dict containing 'guid' and 'url' keys.
        """
        return kwargs['rslt']


class MyEmpire( Empire ):
    """ The Empire object belonging to the current Member's empire.
    
    Object Attributes::

        id                      "xxxx",
        rpc_count               321,        # the number of calls made to the server
        is_isolationist         1,          # hasn't sent out probes or colony ships
        name                    "The Syndicate",
        status_message          "A spy's work is never done.",
        home_planet_id          "id-goes-here",
        has_new_messages        4,
        latest_message_id       1234,
        essentia                0,
        planets                 Dict of all of the bodies that belong to you, 
                                keyed off ID.  This includes both colonies and 
                                space stations.
                                {   "id-goes-here" : "Earth",
                                    "id-goes-here" : "Mars",  
                                    "id-goes-here" : "ISS",  
                                    "id-goes-here" : "Halo",  },
        planet_names            The reverse of planets; a dict keyed on the name.
        colonies                Dict of just your colonies, keyed off ID.
                                {   "id-goes-here" : "Earth",
                                    "id-goes-here" : "Mars",  },
        colony_names            The reverse of colonies; a dict keyed on the name.
        stations                Dict of just your space stations, keyed off ID.
                                {   "id-goes-here" : "ISS",
                                    "id-goes-here" : "Halo",  },
        station_names           The reverse of stations; a dict keyed on the name.
        tech_level"             20,         # Highest level university has gotten to.
        self_destruct_active    0,
        self_destruct_date      ""
    """

    pp = pprint.PrettyPrinter( indent = 4 )

    ### These appear in clients.py, not here:
    ###     login()
    ###     send_password_reset_message()
    ###
    ### Involves email, which the server isn't producing, so skipping:
    ###     reset_password()

    @lacuna.bc.LacunaObject.call_member_meth
    def logout( self, *args, **kwargs ):
        pass

    @lacuna.bc.LacunaObject.set_empire_status
    @lacuna.bc.LacunaObject.call_member_meth
    def get_status( self, *args, **kwargs ):
        """ Gets your empire's current status information.

        There shouldn't ever be a need to call this.  Empire status data gets 
        returned with every empire method call, and the current :class:`MyEmpire` 
        object's attributes get updated each time as a result.
        """
        pass

    @lacuna.bc.LacunaObject.set_empire_status
    @lacuna.bc.LacunaObject.call_member_meth
    def get_invite_friend_url( self, *args, **kwargs ):
        """ Get a unique URL you can send to a friend to use to sign up.  Your 
        empire will receive rewards for each friend who joins using such a 
        URL.
        
        Returns a dict including the key ``referral_url``.
        """
        pass

    @lacuna.bc.LacunaObject.set_empire_status
    @lacuna.bc.LacunaObject.call_member_meth
    def invite_friend( self, email:str, message:str = '', *args, **kwargs ):
        """ Sends email to a friend inviting them to join the game.

        Args:
            email (str): The email address to send the invitation to
            message (str):An optional personal message to include.
        Raises:
            lacuna.exceptions.ServerError: 1010 if you have not set 
                up an email address of your own in your profile.
        """
        pass

    @lacuna.bc.LacunaObject.call_returning_meth
    def view_profile( self, *args, **kwargs ):
        """ View your own empire's profile.  Requires login with your real, not 
        sitter, password,

        Returns:
            lacuna.empire.OwnProfile: Your profile
        Raises:
            lacuna.exceptions.ServerError: 1015 ("Sitters cannot 
                modify preferences") if the user is logged in with their sitter.
        """
        return OwnProfile(self.client, kwargs['rslt']['profile'])

    @lacuna.bc.LacunaObject.call_returning_meth
    def view_public_profile( self, empire_id:int, *args, **kwargs ):
        """ View public profile info on any empire.

        Args:
            empire_id (int): ID of the empire to view.
        Returns:
            lacuna.empire.PublicProfile: Requested empire's profile
        """
        return PublicProfile(self.client, kwargs['rslt']['profile'])

    @lacuna.bc.LacunaObject.call_member_meth
    def edit_profile( self, profile:dict, *args, **kwargs ):
        ### The rv does contain a 'status' dict, but it's in a different 
        ### format from what's expected, so skip the set_empire_status 
        ### decorator.
        """ Edit your empire's profile.  Requires that you're logged in with 
        your real, not sitter, password.

        Args:
            profile (dict): With the keys:

                - description
                - email
                - sitter_password
                - status_message
                - city
                - country
                - notes
                - skype
                - player_name
                - public_medals (list of medal IDs to display)
                - skip_happiness_warnings
                - skip_resource_warnings
                - skip_pollution_warnings
                - skip_medal_messages
                - skip_facebook_wall_posts
                - skip_found_nothing
                - skip_excavator_resources
                - skip_excavator_glyph
                - skip_excavator_plan
                - skip_spy_recovery
                - skip_probe_detected
                - skip_attack_messages
                - skip_incoming_ships

        The skip_* keys are booleans, and require 1 for "on" or 0 for "off".
        """
        pass

    @lacuna.bc.LacunaObject.set_empire_status
    @lacuna.bc.LacunaObject.call_member_meth
    def change_password( self, password:str, confirm:str, *args, **kwargs ):
        """ Changes your full password.

        Args:
            password (str): the desired new password
            confirm (str): the same string as 'password'
        """
        self.client.password = password

    @lacuna.bc.LacunaObject.call_returning_meth
    def find( self, name_segment:str, *args, **kwargs ):
        """ Find an empire by name.

        Args::
            name_segment (str): :ref:`Standard TLE search string <gloss_std_search_string>`.
        Returns:
            lacuna.empire.FoundEmpire: list
        """
        mylist = []
        for i in kwargs['rslt']['empires']:
            mylist.append( FoundEmpire(self.client, i) )
        return mylist

    @lacuna.bc.LacunaObject.set_empire_status
    @lacuna.bc.LacunaObject.call_member_meth
    def set_status_message( self, message:str, *args, **kwargs ):
        """ Sets your empire status message.

        Args:
            message (str): The message to set as your empire's profile's status.
        """
        self.status_message = message
        pass

    @lacuna.bc.LacunaObject.call_returning_meth
    def view_boosts( self, *args, **kwargs ):
        """ Shows your current boosts and their expiration dates.
        
        Returns:
            lacuna.empire.Boosts: Current boosts
        """
        return Boosts( self.client, kwargs['rslt']['boosts'] )

    @lacuna.bc.LacunaObject.set_empire_status
    @lacuna.bc.LacunaObject.call_member_meth
    def boost_storage( self, *args, **kwargs ):
        """ Spends 5 E to set a +25% storage boost for one week. """
        pass

    @lacuna.bc.LacunaObject.set_empire_status
    @lacuna.bc.LacunaObject.call_member_meth
    def boost_food( self, *args, **kwargs ):
        """ Spends 5 E to set a +25% food boost for one week. """
        pass

    @lacuna.bc.LacunaObject.set_empire_status
    @lacuna.bc.LacunaObject.call_member_meth
    def boost_water( self, *args, **kwargs ):
        """ Spends 5 E to set a +25% water boost for one week. """
        pass

    @lacuna.bc.LacunaObject.set_empire_status
    @lacuna.bc.LacunaObject.call_member_meth
    def boost_energy( self, *args, **kwargs ):
        """ Spends 5 E to set a +25% energy boost for one week. """
        pass

    @lacuna.bc.LacunaObject.set_empire_status
    @lacuna.bc.LacunaObject.call_member_meth
    def boost_ore( self, *args, **kwargs ):
        """ Spends 5 E to set a +25% ore boost for one week. """
        pass

    @lacuna.bc.LacunaObject.set_empire_status
    @lacuna.bc.LacunaObject.call_member_meth
    def boost_happiness( self, *args, **kwargs ):
        """ Spends 5 E to set a +25% happiness boost for one week. """
        pass

    @lacuna.bc.LacunaObject.set_empire_status
    @lacuna.bc.LacunaObject.call_member_meth
    def boost_building( self, *args, **kwargs ):
        """ Spends 5 E to set a +25% building speed boost for one week. """
        pass

    @lacuna.bc.LacunaObject.set_empire_status
    @lacuna.bc.LacunaObject.call_member_meth
    def boost_spy_training( self, *args, **kwargs ):
        """ Spends 5 E to set a +50% spy training boost for one week. """
        pass

    #@lacuna.bc.LacunaObject.set_empire_status
    #@lacuna.bc.LacunaObject.call_member_meth
    def enable_self_destruct( self, *args, **kwargs ):
        """ Sets the self destruct timer on your empire.  After 24 hours, your 
        empire will be deleted.  Such a deletion is *not recoverable*.

        While testing, it was discovered that the :meth:`disable_self_destruct` 
        method does not function, server-side.  So if you enable self destruct 
        on your empire, you cannot turn it off again yourself; you'd need to 
        find an admin to do it for you.  Admins are usually around, but it's 
        not unthinkable that a 24-hour period could pass during which you 
        could not find an admin.  If that were to happen, your empire would be 
        permanently deleted.

        :meth:`disable_self_destruct` appears to be working again, but I'm 
        leaving this method disabled anyway.  If you're making a complete 
        client using this module, see me about getting this fixed, but I tend 
        to doubt that's going to happen.
        """
        print( "Please don't ever call this." )
        quit()

    @lacuna.bc.LacunaObject.set_empire_status
    @lacuna.bc.LacunaObject.call_member_meth
    def disable_self_destruct( self, *args, **kwargs ):
        """ Simply does not work on the server side.  This is a known problem, 
        and the reason :meth:`enable_self_destruct` has been disabled.
        """
        pass

    @lacuna.bc.LacunaObject.set_empire_status
    @lacuna.bc.LacunaObject.call_member_meth
    def redeem_essentia_code( self, code: str, *args, **kwargs ):
        """ Redeems an essentia code.

        Args:
            code (str): An essentia code uuid, eg ``56cc359e-8ba7-4db7-b608-8cb861c65510``
        Raises:
            lacuna.exception.ServerError: 1010 if you try to redeem 
                a code that's already been redeemed.  The example code above is such 
                an already-redeemed code; you can use that to test the exception.

        Essentia codes can be obtained by purchasing essentia, or sometimes by 
        admins during contests.  Each code can only be used once, so if you have 
        one, don't share it with anybody; if they use it, the E represented by 
        that code will be gone.
        """
        pass

    @lacuna.bc.LacunaObject.set_empire_status
    @lacuna.bc.LacunaObject.call_member_meth
    def redefine_species_limits( self, *args, **kwargs ):
        """ Returns the limits to be imposed if you redefine your species.

        Returns:
            dict: species limits::

                'can':              1,
                'essentia_cost':    100,
                'max_orbit':        3,
                'min_growth':       1,
                'min_orbit':        3,
                'reason':           None,

        ``can`` will be 0 if the user currently cannot redefine.
        If ``can`` is 0, ``reason`` will contain a string explaining why not.  
        eg "You have already redefined in the past 30 days", etc.
        """
        pass

    @lacuna.bc.LacunaObject.set_empire_status
    @lacuna.bc.LacunaObject.call_member_meth
    def redefine_species( self, params: dict, *args, **kwargs ):
        """ Actually does the deed of redefining a player's species for 100 E.

        Args:
            params (dict): species settings::

                'name': String name of the species (required)
                'description': String
                'min_orbit': Integer 1-7 inclusive
                'max_orbit': Integer 1-7 inclusive.  Must be >= min_orbit.
                'manufacturing_affinity': Integer 1-7 inclusive.
                'deception_affinity': Integer 1-7 inclusive.
                'research_affinity': Integer 1-7 inclusive.
                'management_affinity': Integer 1-7 inclusive.
                'farming_affinity': Integer 1-7 inclusive.
                'mining_affinity': Integer 1-7 inclusive.
                'science_affinity': Integer 1-7 inclusive.
                'environmental_affinity': Integer 1-7 inclusive.
                'political_affinity': Integer 1-7 inclusive.
                'trade_affinity': Integer 1-7 inclusive.
                'growth_affinity': Integer 1-7 inclusive.
        """
        pass

    @lacuna.bc.LacunaObject.call_returning_meth
    def view_species_stats( self, *args, **kwargs ):
        """ Get information about your empire's species.
        
        Returns:
            lacuna.empire.Species: Your species' info
        """
        return Species(self.client, kwargs['rslt']['species'])

    @lacuna.bc.LacunaObject.call_returning_meth
    def get_species_templates( self, *args, **kwargs ):
        """ Get the species templates that are presented to a new player upon 
        initial species creation (Average, Warmonger, Resilient, Viral, etc).
        
        Returns:
            lacuna.empire.SpeciesTemplate: list of templates
        """
        mylist = []
        for i in kwargs['rslt']:
            mylist.append( SpeciesTemplate(self.client, i) )
        return mylist


class Species(lacuna.bc.SubClass):
    """ The attributes associated with an empire's species.

    Object Attributes::

        name                     "Human",
        description              "The descendants of Earth.",
        min_orbit                3,
        max_orbit                3,
        manufacturing_affinity   4,
        deception_affinity       4,
        research_affinity        4,
        management_affinity      4,
        farming_affinity         4,
        mining_affinity          4,
        science_affinity         4,
        environmental_affinity   4,
        political_affinity       4,
        trade_affinity           4,
        growth_affinity          4
    """
    ### This will usually be accessed from something like the Library of 10 
    ### colonies, and then 10 stations, just to show that they're separate.
    ### the idea of an empire that this seemed the best place for it.

    def to_dict(self):
        """ Returns the object's attributes as a dict, suitable for passing to 
        :class:`lacuna.empire.redefine_species`.
        """
        mydict = {}
        attribs = ( 'name', 'description', 'min_orbit', 'max_orbit', 'manufacturing_affinity',
            'deception_affinity', 'research_affinity', 'management_affinity', 'farming_affinity',
            'mining_affinity', 'science_affinity', 'environmental_affinity', 'political_affinity',
            'trade_affinity', 'growth_affinity' )
        for i in attribs:
            mydict[i] = getattr(self, i)
        return mydict

class SpeciesTemplate(lacuna.bc.SubClass):
    """
    These are the presets presented to a new player in the process of setting 
    up a new empire.

    Object Attributes::

        name                        "Average", 
        description                 "A race of average intellect, and weak constitution.',
        min_orbit                   3,
        max_orbit                   3,
        manufacturing_affinity      4,
        deception_affinity          4,
        research_affinity           4,
        management_affinity         4,
        farming_affinity            4,
        mining_affinity             4,
        science_affinity            4,
        environmental_affinity      4,
        political_affinity          4,
        trade_affinity              4,
        growth_affinity             4
    """



class OwnProfile(lacuna.bc.SubClass):
    """ This is the user's own profile info.  Another empire's public profile 
    will contain less data.

    Object Attributes::

        description                  "description goes here",
        status_message               "status message goes here",
        medals                       Dict:
                                        {   "Integer Medal ID" : {
                                                "name" : "Built Level 1 Building",
                                                "image" : "building1",
                                                "date" : "01 31 2010 13:09:05 +0600",
                                                "public" : 1,
                                                "times_earned" : 4       },
                                            ...       },
        city                         "Madison",
        country                      "USA",
        notes                        "notes go here",
        skype                        "joeuser47",
        player_name                  "Joe User",
        skip_happiness_warnings      0,
        skip_resource_warnings       0,
        skip_pollution_warnings      0,
        skip_medal_messages          0,
        skip_facebook_wall_posts     0,
        skip_found_nothing           0,
        skip_excavator_resources     0,
        skip_excavator_glyph         0,
        skip_excavator_plan          0,
        skip_spy_recovery            0,
        skip_probe_detected          0,
        skip_attack_messages         0,
        skip_incoming_ships          0,
        email                        "joe@example.com",
        sitter_password              "abcdefgh"    
    """

class PublicProfile(lacuna.bc.SubClass):
    """ This is the public profile of any empire.

    Object Attributes::

        id                      "empire-id-goes-here",
        name                    "Lacuna Expanse Corp",
        colony_count            1,
        status_message          "Looking for Essentia."
        description             "We are the original inhabitants of the Lacuna Expanse.",
        city                    "Madison",
        country                 "USA",
        skype                   "joeuser47",
        player_name             "Joe User",
        medals                  {   "id-goes-here" : {  "name" : "Built Level 1 Building",
                                                        "image" : "building1",
                                                        "date" : "01 31 2010 13:09:05 +0600",
                                                        "times_earned" : 4   },  },
        last_login              "01 31 2010 13:09:05 +0600",
        date_founded            "01 31 2010 13:09:05 +0600",
                         "Lacunan",
        alliance                {   "id" : "id-goes-here",
                                    "name" : "The Confederacy"   },
        known_colonies          [ {     "id" : "id-goes-here",
                                        "x" : "1",
                                        "y" : "-543",
                                        "name" : "Earth",
                                        "image" : "p12-3" },
                                    { more of the same },   ]
    """

class FoundEmpire(lacuna.bc.SubClass):
    """ 
    Object Attributes::

        id      Integer ID of the empire
        name    String name of the empire
    """

class OwningEmpire(lacuna.bc.SubClass):
    """ An empire that owns a given body.

    Object Attributes::

        id                  Integer ID of the empire
        name                String name of the empire
        alignment           'ally' # 'ally', 'self', or 'hostile'
        is_isolationist     1 or 0
    """

class Boosts(lacuna.bc.SubClass):
    """ 
    Object Attributes::

        food            "01 31 2010 13:09:05 +0600",
        ore             "01 31 2010 13:09:05 +0600",
        energy          "01 31 2010 13:09:05 +0600",
        water           "01 31 2010 13:09:05 +0600",
        happiness       "01 31 2010 13:09:05 +0600",
        storage         "01 31 2010 13:09:05 +0600",
        building        "01 31 2010 13:09:05 +0600",
        spy_training    "01 31 2010 13:09:05 +0600"
    """
