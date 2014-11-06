
import pprint, re
import lacuna.bc

"""
    An Empire object is not logged in, and is meant for use only by new users 
    who need to fetch a captcha or check if a given empire name is available 
    in the process of creating an account.

    Most of the time, your Empire object will be a MyEmpire object
"""

class Empire(lacuna.bc.LacunaObject):
    """ A generic Empire object that can be used with a non-logged-in Guest."""

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

    @lacuna.bc.LacunaObject.call_guest_meth
    def fetch_captcha( self ):
        """ Returns dict containing 'guid' and 'url' keys
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
CHECK

It might be nice to have an attribute "station_re" or some such:
    station_re = '^\wASS'

...and then have a method to separate known stations from planets:
    def get_planets_not_stations:
        for id, name in self.planets.items():
            if re.match(self.station_re, name):
                continue
            print( "{} is id {}".format(name, id) )

"""

class MyEmpire( Empire ):
    """ The Empire object belonging to the current Member's empire.
    
    Attributes:
        id                      "xxxx",
        rpc_count               321, # the number of calls made to the server
        is_isolationist         1, # hasn't sent out probes or colony ships
        name                    "The Syndicate",
        status_message          "A spy's work is never done.",
        home_planet_id          "id-goes-here",
        has_new_messages        4,
        latest_message_id       1234,
        essentia                0,
        planets                 {
                                    "id-goes-here" : "Earth",
                                    "id-goes-here" : "Mars
                                },
        tech_level"             20,  # Highests level university has gotten to.
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
        """ There shouldn't ever be a need to call this.  An empire status 
        block gets returned with every call, and the MyEmpire object's 
        attributes get set each time as a result.
        """
        pass

    @lacuna.bc.LacunaObject.set_empire_status
    @lacuna.bc.LacunaObject.call_member_meth
    def get_invite_friend_url( self, *args, **kwargs ):
        """ See the 'referral_url' key in the returned dict. """
        pass

    @lacuna.bc.LacunaObject.set_empire_status
    @lacuna.bc.LacunaObject.call_member_meth
    def invite_friend( self, email, message="", *args, **kwargs ):
        """ Doesn't error, but doesn't send email either.  Since the 'forgot 
        my password' feature is exhibiting the same behavior, I'm going to 
        assume the server just isn't configured to send mail anymore.
        """
        pass

    @lacuna.bc.LacunaObject.call_returning_meth
    def view_profile( self, *args, **kwargs ):
        """ View your own empire's profile.  Requires login with your real, not 
        sitter, password,

        Returns an empire.OwnProfile object.

        Throws 1015 (Sitters cannot modify preferences) if the user is 
        logged in with their sitter.
        """
        return OwnProfile(self.client, kwargs['rslt']['profile'])

    @lacuna.bc.LacunaObject.call_returning_meth
    def view_public_profile( self, empire_id:int, *args, **kwargs ):
        """ View public profile info on any empire.

        Arguments:
            empire_id   Integer ID of the empire to view.

        Returns an empire.PublicProfile object.
        """
        return PublicProfile(self.client, kwargs['rslt']['profile'])

    @lacuna.bc.LacunaObject.call_member_meth
    def edit_profile( self, profile:dict, *args, **kwargs ):
        ### The rv does contain a 'status' dict, but it's in a different 
        ### format from what's expected, so skip the set_empire_status 
        ### decorator.
        """ Edit your empire's profile.  Requires that you're logged in with 
        your real, not sitter, password.

        Arguments:
            profile     Dict of profile settings:
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

                        The following are all booleans, indicating whether to 
                        skip a given warning or game-generated mail.
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

    @lacuna.bc.LacunaObject.set_empire_status
    @lacuna.bc.LacunaObject.call_member_meth
    def change_password( self, oldpw:str, newpw:str, *args, **kwargs ):
        """ Changes your full password.

        Arguments
            password        String; the desired new password
            confirmation    Must be the same string as 'password'
        """
        pass

    @lacuna.bc.LacunaObject.call_returning_meth
    def find( self, name_segment:str, *args, **kwargs ):
        """ Find an empire by name.

        Arguments:
            name    Standard TLE search string

        Returns a list of empire.FoundEmpire objects.
        """
        mylist = []
        for i in kwargs['rslt']['empires']:
            mylist.append( FoundEmpire(self.client, i) )
        return mylist

    @lacuna.bc.LacunaObject.set_empire_status
    @lacuna.bc.LacunaObject.call_member_meth
    def set_status_message( self, message:str, *args, **kwargs ):
        """ Sets your empire status message.  """
        pass

    @lacuna.bc.LacunaObject.call_returning_meth
    def view_boosts( self, *args, **kwargs ):
        """ Shows your current boosts and their expiration dates.
        
        Returns an empire. Boosts object.
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
    def spy_training_boost( self, *args, **kwargs ):
        """ Spends 5 E to set a +50% spy training boost for one week. """
        pass

    ### Commenting this out because, right now, disable_self_destruct() does 
    ### not work, server side.  It's a known problem.  Being able to turn on 
    ### the suicide button but not being able to turn it back off again is 
    ### fraught.
    #@lacuna.bc.LacunaObject.set_empire_status
    #@lacuna.bc.LacunaObject.call_member_meth
    #def enable_self_destruct( self, *args, **kwargs ):
    #    pass

    @lacuna.bc.LacunaObject.set_empire_status
    @lacuna.bc.LacunaObject.call_member_meth
    def disable_self_destruct( self, *args, **kwargs ):
        pass

    @lacuna.bc.LacunaObject.set_empire_status
    @lacuna.bc.LacunaObject.call_member_meth
    def redeem_essentia_code( self, code, *args, **kwargs ):
        ### Untested; I have no E codes to try this out with, and I'm not 
        ### spending money to test.
        pass

    @lacuna.bc.LacunaObject.set_empire_status
    @lacuna.bc.LacunaObject.call_member_meth
    def redefine_species_limits( self, *args, **kwargs ):
        """ Returns the limits to be imposed if you redefine your species.

        Returns a dict:
            'can':              1,
            'essentia_cost':    100,
            'max_orbit':        3,
            'min_growth':       1,
            'min_orbit':        3,
            'reason':           None,

        'can' will be 0 if the user currently cannot redefine.
        I do not understand why the min/max settings exist.
        If 'can' is false, 'reason' will contain a string explaining why 
        not.  eg "You have already redefined in the past 30 days", etc.
        """
        pass

    @lacuna.bc.LacunaObject.set_empire_status
    @lacuna.bc.LacunaObject.call_member_meth
    def redefine_species( self, params, *args, **kwargs ):
        """ Actually does the deed of redefining a player's species.
        Costs E, so untested.

        Arguments:
            params  Dict of species settings:
                    name                    String name of the species (required)
                    description             String
                    min_orbit               Integer 1-7 inclusive
                    max_orbit               Integer 1-7 inclusive.  Must be >= min_orbit.
                    manufacturing_affinity  Integer 1-7 inclusive.
                    deception_affinity      Integer 1-7 inclusive.
                    research_affinity       Integer 1-7 inclusive.
                    management_affinity     Integer 1-7 inclusive.
                    farming_affinity        Integer 1-7 inclusive.
                    mining_affinity         Integer 1-7 inclusive.
                    science_affinity        Integer 1-7 inclusive.
                    environmental_affinity  Integer 1-7 inclusive.
                    political_affinity      Integer 1-7 inclusive.
                    trade_affinity          Integer 1-7 inclusive.
                    growth_affinity         Integer 1-7 inclusive.
        """
        pass

    @lacuna.bc.LacunaObject.call_returning_meth
    def view_species_stats( self, *args, **kwargs ):
        """ Returns information about your empire's species.
        
        Returns a single empire.Species object.
        """
        return Species(self.client, kwargs['rslt']['species'])

    @lacuna.bc.LacunaObject.call_returning_meth
    def get_species_templates( self, *args, **kwargs ):
        """ Returns the species templates that are presented to a new player 
        upon initial species creation (Average, Warmonger, Resilient, Viral, 
        etc).
        
        Returns a list of empire.SpeciesTemplate objects.
        """
        mylist = []
        for i in kwargs['rslt']:
            mylist.append( SpeciesTemplate(self.client, i) )
        return mylist

class Species(lacuna.bc.SubClass):
    """ The attributes associated with an empire's species.

    Attributes:
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
    ### This will usually be accessed from something like the Library of 
    ### Jith's research_species() method, but it's closely-enough related to 
    ### the idea of an empire that this seemed the best place for it.
    pass

class SpeciesTemplate(lacuna.bc.SubClass):
    """
    These are the presets presented to a new player in the process of setting 
    up a new empire.

    Attributes:
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

    Attributes:
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

    Attributes:
        id                      "empire-id-goes-here",
        name                    "Lacuna Expanse Corp",
        colony_count            1,
        status_message          "Looking for Essentia."
        description             "We are the original inhabitants of the Lacuna Expanse.",
        city                    "Madison",
        country                 "USA",
        skype                   "joeuser47",
        player_name             "Joe User",
        medals                  {
                                    "id-goes-here" : {
                                        "name" : "Built Level 1 Building",
                                        "image" : "building1",
                                        "date" : "01 31 2010 13:09:05 +0600",
                                    "times_earned" : 4
                                    },
                                    ...
                                },
        last_login              "01 31 2010 13:09:05 +0600",
        date_founded            "01 31 2010 13:09:05 +0600",
        species                 "Lacunan",
        alliance                {
                                    "id" : "id-goes-here",
                                    "name" : "The Confederacy"
                                },
        known_colonies          [
                                    {
                                        "id" : "id-goes-here",
                                        "x" : "1",
                                        "y" : "-543",
                                        "name" : "Earth",
                                        "image" : "p12-3"
                                    },
                                    ...
                                ]
    """

class FoundEmpire(lacuna.bc.SubClass):
    """ 
    Attributes:
        id      Integer ID of the empire
        name    String name of the empire
    """

class Boosts(lacuna.bc.SubClass):
    """ 
    Attributes:
        Each pair is the name of the boost and the date it expires.

        food            "01 31 2010 13:09:05 +0600",
        ore             "01 31 2010 13:09:05 +0600",
        energy          "01 31 2010 13:09:05 +0600",
        water           "01 31 2010 13:09:05 +0600",
        happiness       "01 31 2010 13:09:05 +0600",
        storage         "01 31 2010 13:09:05 +0600",
        building        "01 31 2010 13:09:05 +0600",
        spy_training    "01 31 2010 13:09:05 +0600"
    """
