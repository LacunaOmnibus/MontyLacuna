
from lacuna.bc import LacunaObject

class Stats(LacunaObject):

    path = 'stats'

    @LacunaObject.call_guest_meth
    def credits( self ):
        """ Returns a list of structs of the game credits.

         This example is far from exhaustive but should give you the idea.
                [
                    { "Game Server" : ["JT Smith"]},
                    { "iPhone Client" : ["Kevin Runde"]},
                    { "Web Client" : ["John Rozeske"]},
                    { "Play Testers" : ["John Ottinger","Jamie Vrbsky"]},
                    ...
                ]

        This method does not require a logged-in client, so it doesn't return a stats
        block.
        """
        pass

    @LacunaObject.set_empire_status
    @LacunaObject.call_member_meth
    def alliance_rank( self, sort_by = 'influence desc,population desc', page_number = 1 ):
        """ Returns struct with keys:
                'total_alliances' - integer count.
                'page_number' - what page we're displaying (defaults to 1)
                'alliances' - list of structs, one alliance per struct.
                'status' - standard

            Returns 25 alliances per page.

            Allowed values for sort_by:
                influence
                population
                average_empire_size_rank
                offense_success_rate_rank
                defense_success_rate_rank
                dirtiest_rank

                CAVEAT
                    The docs for this are flat-out wrong, and appear to be the result
                    of a copy/paste error from find_alliance_rank.  

                    The point is that the published docs conflict with these docs.  
                    These are more righter.  Yeah, you heard me.

                    The default sort_by value in the server code is 
                    'influence desc,population desc'.  However, the code is checking
                    the incoming sort_by value against an array of legal choices, and 
                    'influenced desc,population desc' is not one of those legal choices.

                    Happily, if what you send is not a legal choice, the server code 
                    defaults to 'influenced desc,population desc'.  So you could send 
                    'influenced desc,population desc' and get 'influenced desc,population desc', 
                    but it wouldn't be for the reason you might think (because that's
                    what you fucking sent).  You could send "baseball" and you'd still
                    end up with 'influenced desc,population desc'.

                    Because this is all so confusing and goofy, the default sort_by 
                    value of this method is 'influenced desc,population desc'.  Again, 
                    it could be "tingly-wingly" and get the same result, but that might 
                    lead to a bit of confusion down the road.
        """
        pass

    @LacunaObject.set_empire_status
    @LacunaObject.call_member_meth
    def find_alliance_rank( self, sort_by = '', alliance_name = '' ):
        """
            sort_by
                same options as for alliance_rank()
            alliance_name
                Standard TLE search string - at least 3 letters.  Alliances whose 
                names =~ /^this_alliance_name_arg/ are returned.

            Returns struct with keys:
                alliances
                    list of structs, one per matching alliances
                            {
                                "alliance_id" : "id-goes-here",
                                "alliance_name" : "Earth Allies",
                                "page_number" : "54",
                            },
                            ...
                status
                    standard
        """
        pass

    @LacunaObject.set_empire_status
    @LacunaObject.call_member_meth
    def empire_rank( self, sort_by = 'empire_size_rank', page_number = 1 ):
        """ Returns struct with keys:
                'empires'           list of structs, one struct per empire
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
                'total_empires'     int
                'page_number'       int
                'status'            standard
            sort_by legal values:
                empire_size_rank (default)
                offense_success_rate_rank
                defense_success_rate_rank
                dirtiest_rank
        """
        pass

    @LacunaObject.set_empire_status
    @LacunaObject.call_member_meth
    def find_empire_rank( self, sort_by = '', empire_name = '' ):
        """ Returns struct with keys:
                'empires'   list of structs, one struct per empire
                                {
                                    "empire_id" : "id-goes-here",
                                    "empire_name" : "Earthlings",
                                    "page_number" : "54",
                                }
                'status'    standard

            sort_by         legal values same as for empire_rank().
            empire_name     standard TLE search value - >= 3 characters, matches front.
        """

    @LacunaObject.set_empire_status
    @LacunaObject.call_member_meth
    def colony_rank( self, sort_by = 'population_rank' ):
        """ Returns struct with keys:
                status      standard
                colonies    list of structs
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
            sort_by legal values:
                what thee fuck.  It defaults to "population_rank".  There is exactly one legal
                value, which is "population_rank".
        """
        pass

    @LacunaObject.set_empire_status
    @LacunaObject.call_member_meth
    def spy_rank( self, sort_by = 'level_rank' ):
        """ Returns struct with keys:
                status      standard
                spies    list of structs
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
            sort_by legal values:
                level_rank
                success_rate_rank
                dirtiest_rank
        """
        pass

    @LacunaObject.set_empire_status
    @LacunaObject.call_member_meth
    def weekly_medal_winners( self ):
        """ Returns struct with keys:
                status      standard
                winners    list of structs
                        {
                            "empire_id" : "id-goes-here",
                            "empire_name" : "Earthlings",
                            "medal_name" : "Dirtiest Player In The Game",
                            "medal_image" : "dirtiest1",
                            "times_earned" : 4,
                        },
        """
        pass

