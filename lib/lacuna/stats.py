
import lacuna.bc

class Stats(lacuna.bc.LacunaObject):
    """ Provides access to game stats and rankings.  """

    path = 'stats'

    @lacuna.bc.LacunaObject.call_guest_meth
    def credits( self, *args, **kwargs ):
        """ Returns the game's credits.

        This method does not require a logged-in client.

        Returns a dict, with the keys being credit types and the values being a list of people or entities having that credit:
            >>> 
            'Game Support'  [   
                                'Plain Black Corporation / plainblack.com',
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
            - sort_by -- String.  What to sort the returned list on.  Defaults to "influence desc, population desc".
            - page_number -- Integer page number to return, 25 alliances per page.  Defaults to 1.

            Allowed values for sort_by (but see CAVEAT below):
                - influence
                - population
                - average_empire_size_rank
                - offense_success_rate_rank
                - defense_success_rate_rank
                - dirtiest_rank

        Return a tuple:
            - alliances -- List of AllianceInfo objects
            - total_alliances -- Integer count.
            - page_number -- What page we're displaying (defaults to 1)

        CAVEAT
            The docs for this are flat-out wrong, and appear to be the result
            of a copy/paste error from find_alliance_rank.  

            The point is that the published docs conflict with these docs.  

            The default sort_by value in the server code is 'influence 
            desc,population desc'.  However, the code is checking the incoming 
            sort_by value against an array of legal choices, and 'influenced 
            desc,population desc' is not one of those legal choices.

            Happily, if what you send is not a legal choice, the server 
            defaults to 'influenced desc,population desc'.  So you could send 
            'influenced desc,population desc' and get 'influenced 
            desc,population desc', but it wouldn't be for the reason you might 
            think (because that's what you sent).  You could send "Rajesh 
            Koothrapalli" and you'd still end up with 'influenced 
            desc,population desc'.
        """
        mylist = []
        for i in kwargs['rslt']['alliances']:
            mylist.append( AllianceInfo(self.client, i) )
        return(
            mylist,
            kwargs['rslt']['total_alliances'],
            kwargs['rslt']['page_number'],
        )

    @lacuna.bc.LacunaObject.call_returning_meth
    def find_alliance_rank( self, sort_by = '', alliance_name = '', *args, **kwargs ):
        """ Finds stats for a specific alliance.

        Arguments:
            - sort_by -- same options as for alliance_rank()
            - alliance_name -- Standard TLE search string

        Returns list of limited AllianceInfo objects containing only the attributes:
            - alliance_id
            - alliance_name
            - page_number
        
        This list will usually contain only a single alliance, but occasionally more than one alliance will match your passed-in alliance_name.
        """
        mylist = []
        for i in kwargs['rslt']['alliances']:
            mylist.append( AllianceInfo(self.client, i) )
        return mylist

    @lacuna.bc.LacunaObject.set_empire_status
    @lacuna.bc.LacunaObject.call_member_meth
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
        
        Returned dict contains:
            >>> 
                'total_empires'     int
                'page_number'       int
                'status'            standard
                'empires'           list of dicts:
                                    [
                                        {
                                            "empire_id" : "id-goes-here",                   # unique id
                                            "empire_name" : "Earthlings",                   # empire name
                                            "alliance_id" : "id-goes-here",                 # unique id
                                            "alliance_name" : "Earthlings Allied",          # alliance name
                                            "colony_count" : "1",                           # number of planets colonized
                                            "population" : "7000000000",                    # number of citizens on all planets in the empire
                                            "empire_size" : "7000000000",                   # size of entire empire
                                            "building_count" : "50",                        # number of buildings across all colonies
                                            "average_building_level" : "20",                # average level of all buildings across all colonies
                                            "offense_success_rate" : "0.793",               # the offense rate of success of spies at all colonies
                                            "defense_success_rate" : "0.49312",             # the defense rate of success of spies at all colonies
                                            "dirtiest" : "7941"                            # the number of times a spy has attempted to hurt another empire
                                        },
                                        { more of the same },
                                    ]
        """
        pass

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

        Returns list of stats.EmpireInfo objects.
        """
        mylist = []
        for i in kwargs['rslt']['empires']:
            mylist.append( EmpireInfo(self.client, i) )
        return mylist

    @lacuna.bc.LacunaObject.set_empire_status
    @lacuna.bc.LacunaObject.call_member_meth
    def colony_rank( self, sort_by = 'population_rank', *args, **kwargs ):
        """ Find planets sorted by various options.

        Accepts optional argument 'sort_by', which defaults to 
        'population_rank'.  'population_rank' is also the only legal value for 
        this argument.  No, I dunno either.

        Returns dict with keys:
            >>> 
            colonies    list of dicts
                [
                    {
                        "empire_id" : "id-goes-here",                   # unique id
                        "empire_name" : "Earthlings",                   # empire name
                        "planet_id" : "id-goes-here",                   # unique id
                        "planet_name" : "Earth",                        # name of the planet
                        "population" : "7000000000",                    # number of citizens on planet
                        "building_count" : "50",                        # number of buildings at this colony
                        "average_building_level" : "20",                # average level of all buildings at this colony
                        "highest_building_level" : "26"                 # highest building at this colony
                    },
                    { more of the same }
                ]
        """
        pass

    @lacuna.bc.LacunaObject.set_empire_status
    @lacuna.bc.LacunaObject.call_member_meth
    def spy_rank( self, sort_by = 'level_rank', *args, **kwargs ):
        """ List spies by various options

        Accepts optional 'sort_by' argument.  Legal values are:
            - level_rank
            - success_rate_rank
            - dirtiest_rank

        Returns dict with keys:
            >>> 
                'spies':  [
                        {
                            "empire_id" : "id-goes-here",                   # unique id
                            "empire_name" : "Earthlings",                   # empire name
                            "spy_id" : "id-goes-here",                      # unique id
                            "spy_name" : "Agent Null",                      # the name of this spy
                            "age" : "3693",                                 # how old is this guy in seconds
                            "level" : "18",                                 # the level of this spy
                            "success_rate" : "0.731",                       # the rate of success this spy has had for both offense and defensive tasks
                            "dirtiest" : "7941",                            # the number of times a spy has attempted to hurt another empire
                        },
                    ]
        """
        pass

    @lacuna.bc.LacunaObject.set_empire_status
    @lacuna.bc.LacunaObject.call_member_meth
    def weekly_medal_winners( self, *args, **kwargs ):
        """ View medal winners

        Returned dict includes:
            >>> 
            'winners': [
                        {
                            "empire_id" : "id-goes-here",
                            "empire_name" : "Earthlings",
                            "medal_name" : "Dirtiest Player In The Game",
                            "medal_image" : "dirtiest1",
                            "times_earned" : 4,
                        },
                    ]
        """
        pass

class EmpireInfo(lacuna.bc.SubClass):
    """
    Attributes:
        >>> 
        empire_id       "id-goes-here",
        empire_name     "Earthlings",
        page_number     "54",
    """

class AllianceInfo(lacuna.bc.SubClass):
    """
    Attributes:
        >>> 
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
