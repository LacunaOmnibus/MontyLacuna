
import lacuna.bc

class Stats(lacuna.bc.LacunaObject):
    """ Provides access to game stats and rankings.  """

    path = 'stats'

    @lacuna.bc.LacunaObject.call_guest_meth
    def credits( self, *args, **kwargs ):
        """ Returns the game's credits.

        This method does not require a logged-in client.

        Returns a dict, with the keys being credit types and the values being 
        a list of people or entities having that credit::

            'Game Support'  [   'Plain Black Corporation / plainblack.com',
                                'Mary Hoerr',
                                'United Federation' 
                            ],
            'Game Design':  [
                                'JT Smith',
                                'Jamie Vrbsky'
                            ],
            etc
        """
        ### Why the retval from TLE is a list of dicts instead of just a 
        ### single dict is beyond me.  Let's simplify that a bit.
        mydict = {}
        for i in kwargs['rslt']:
            for k,v in i.items():
                mydict[k] = v
        return mydict

    @lacuna.bc.LacunaObject.call_returning_meth
    def alliance_rank( self, sort_by = 'influence desc,population desc', page_number = 1, *args, **kwargs ):
        """ Returns info on current alliance ranks.

        Arguments:
            - sort_by -- String.  What to sort the returned list on.  Defaults 
              to "influence desc, population desc".  Permitted values:

              - influence
              - population
              - average_empire_size_rank
              - offense_success_rate_rank
              - defense_success_rate_rank
              - dirtiest_rank

            - page_number -- Integer page number to return, 25 alliances per 
              page.  Defaults to 1.

        Return a tuple:
            - alliances -- List of :class:`lacuna.stats.AllianceInfo` objects
            - total_alliances -- Integer count.
            - page_number -- What page we're displaying (defaults to 1)

        """
        mylist = []
        for i in kwargs['rslt']['alliances']:
            mylist.append( AllianceInfo(self.client, i) )
        return(
            mylist,
            self.get_type(kwargs['rslt']['total_alliances']),
            self.get_type(kwargs['rslt']['page_number']),
        )

    @lacuna.bc.LacunaObject.call_returning_meth
    def find_alliance_rank( self, sort_by = '', alliance_name = '', *args, **kwargs ):
        """ Finds stats for a specific alliance.

        Arguments:
            - sort_by -- same options as for alliance_rank()
            - alliance_name -- Standard TLE search string

        Returns list of limited :class:`lacuna.stats.AllianceInfo` objects 
        containing only the attributes:
            - alliance_id
            - alliance_name
            - page_number
        
        This list will usually contain only a single alliance, but occasionally 
        more than one alliance will match your passed-in alliance_name.
        """
        mylist = []
        for i in kwargs['rslt']['alliances']:
            mylist.append( AllianceInfo(self.client, i) )
        return mylist

    @lacuna.bc.LacunaObject.call_returning_meth
    def empire_rank( self, sort_by = 'empire_size_rank', page_number = 1, *args, **kwargs ):
        """ Find empires sorted by various options.

        Arguments:
            - sort_by -- how the empires should be sorted.  Defaults to 'empire_size_rank'.
            - page_number -- which page to return.  Defaults to 1.

            sort_by legal values:
                - empire_size_rank (default)
                - offense_success_rate_rank
                - defense_success_rate_rank
                - dirtiest_rank
        
        Returns a tuple:
            - empires -- List of up to 25 :class:`lacuna.stats.EmpireInfo` objects.
            - empire count -- Integer total number of empires in the game.
            - page number -- Integer page we're looking at.  Should be the same 
              as the page_number argument you passed in.
        """
        mylist = []
        for i in kwargs['rslt']['empires']:
            mylist.append( EmpireInfo(self.client, i) )
        return (
            mylist,
            self.get_type(kwargs['rslt']['total_empires']),
            self.get_type(kwargs['rslt']['page_number']),
        )

    @lacuna.bc.LacunaObject.call_returning_meth
    def find_empire_rank( self, sort_by = '', empire_name = '', *args, **kwargs ):
        """ Returns info on specific empires in the ranks.

        Arguments:
            - sort_by -- String.  See empire_rank()
            - empire_name -- Standard TLE search string.

        Keep in mind that this method has the potential of returning multiple 
        empires; an empire_name argument of "inf" will return both "Infinate 
        Ones" and "Infinitus Imperium".

        So remember that this is returning is list, not a single object.

        Returns list of :class:`lacuna.stats.EmpireInfo` objects.
        """
        mylist = []
        for i in kwargs['rslt']['empires']:
            mylist.append( EmpireInfo(self.client, i) )
        return mylist

    @lacuna.bc.LacunaObject.call_returning_meth
    def colony_rank( self, sort_by = 'population_rank', *args, **kwargs ):
        """ Find colonies ranked by population

        Arguments:
            - Realistically, this accepts no arguments.
            - sort_by -- Optional string.  The API docs list this as a passable 
              argument, but the default of 'population_rank' is also the only 
              legal value.  Passing any unrecognized value falls back to using 
              the default.  So pretend this method takes no arguments.

        Returns a list of :class:`lacuna.stats.ColonyInfo` objects.
        """
        mylist = []
        for i in kwargs['rslt']['colonies']:
            mylist.append( ColonyInfo(self.client, i) )
        return mylist

    @lacuna.bc.LacunaObject.call_returning_meth
    def spy_rank( self, sort_by = 'level_rank', *args, **kwargs ):
        """ List spies ranked by various options.

        Accepts optional 'sort_by' argument.  Legal values are:
            - level_rank
            - success_rate_rank
            - dirtiest_rank

        Returns a list of :class:`lacuna.stats.SpyInfo` objects.

        **CAUTION**
        This method has been included only for API completeness; you should 
        probably never use it.

        Rankings of spies is well-known to be a problem area.  The list of spies 
        returned by this method does not appear to be sorted as requested, and 
        cannot possibly be the top spies in the game (I'm currently getting two
        level 3 spies show up when the list is sorted by "level_rank").

        Also, only 25 spies are returned, and there's no way to request any but 
        those first 25 spies.

        Your best bet is to pretend this doesn't exist.
        """
        mylist = []
        for i in kwargs['rslt']['spies']:
            mylist.append( SpyInfo(self.client, i) )
        return mylist

    @lacuna.bc.LacunaObject.call_returning_meth
    def weekly_medal_winners( self, *args, **kwargs ):
        """ View medal winners

        Returns a list of :class:`lacuna.stats.MedalWinner` objects.
        """
        mylist = []
        for i in kwargs['rslt']['winners']:
            mylist.append( MedalWinner(self.client, i) )
        return mylist

class EmpireInfo(lacuna.bc.SubClass):
    """
    Attributes::

        empire_id       "id-goes-here",
        empire_name     "Earthlings",
        page_number     "54",
    """

class AllianceInfo(lacuna.bc.SubClass):
    """
    Attributes::

        alliance_id             "id-goes-here",
        alliance_name           "Earthlings",
        member_count            "1",
        space_station_count     0,
        influence               0,
        colony_count            "1",
        population              "7000000000",       # number of citizens on all planets in the alliance
        average_empire_size     "7000000000",
        building_count          "50",               # number of buildings across all colonies 
        average_building_level  "20",               # average level of all buildings across all colonies
        offense_success_rate    "0.793",            # the offense rate of success of spies at all colonies
        defense_success_rate    "0.49312",          # the defense rate of success of spies at all colonies
        dirtiest                "7941"              # the number of times a spy has attempted to hurt another empire
    """

class ColonyInfo(lacuna.bc.SubClass):
    """
    Attributes::

        empire_id                   "id-goes-here",      # unique id
        empire_name                 "Earthlings",        # empire name
        planet_id                   "id-goes-here",      # unique id
        planet_name                 "Earth",             # name of the planet
        population                  "7000000000",        # number of citizens on planet
        building_count              "50",                # number of buildings at this colony
        average_building_level      "20",                # average level of all buildings at this colony
        highest_building_level      "26"                 # highest building t this colony
    """

class SpyInfo(lacuna.bc.SubClass):
    """
    Attributes::

        empire_id       "id-goes-here",         # unique id
        empire_name     "Earthlings",           # empire name
        spy_id          "id-goes-here",         # unique id
        spy_name        "Agent Null",           # the name of this spy
        age             "3693",                 # how old is this guy in seconds
        level           "18",                   # the level of this spy
        success_rate    "0.731",                # the rate of success this spy has had for both offense and defensive tasks
        dirtiest        "7941",                 # the number of times a spy has attempted to hurt another empire

    """

class MedalWinner(lacuna.bc.SubClass):
    """
    Attributes::

        empire_id       "id-goes-here",
        empire_name     "Earthlings",
        medal_name      "Dirtiest Player In The Game",
        medal_image     "dirtiest1",
        times_earned    4,
    """

