
from lacuna.bc import LacunaObject

class Map(LacunaObject):
    """All Map methods require a session ID, so these can only be used by a
    Member, not a Client.
    """

    path = 'map'

    @LacunaObject.set_empire_status
    @LacunaObject.call_member_named_meth
    def get_star_map( self, mydict, *args, **kwargs ):
        """The passed-in dict must contain the keys top, bottom, left, right.  
        Each must be an integer within the star map (so >= -1500 and <= 1500).

        rv['stars'] contains a list of dicts.
        Sample dict:
            {
                'color': 'red',
                'id': '15320',
                'name': 'Oot Yaeplie Oad',
                'x': '288',
                'y': '-1118',
                'zone': '1|-4'
            }
        """
        pass

    @LacunaObject.set_empire_status
    @LacunaObject.call_member_meth
    def get_stars( self, x1, x2, y1, y2, *args, **kwargs ):
        """ rv is the same as for get_star_map()."""
        pass

    @LacunaObject.set_empire_status
    @LacunaObject.call_member_meth
    def check_star_for_incoming_probe( self, star_id, *args, **kwargs ):
        """ rv['incoming_probe'] will be 1 for true, 0 for false."""
        pass

    @LacunaObject.set_empire_status
    @LacunaObject.call_member_meth
    def get_star( self, star_id, *args, **kwargs ):
        """ Returns a single dict (NOT a list of dicts like get_star() and 
        get_star_map()!)

        Retval contains 'star', a dict, which includes:

                'color': 'white',
                'id': '12345',
                'name': 'Sol',
                'station': {   'id': '98765',
                            'name': 'Seizing Space Station Name',
                            'x': '0',
                            'y': '0'},
                'x': '1',
                'y': '1',
                'zone': '0|0',

                'bodies': List of body dicts

            If you or an alliance mate have probed or oracled the star, 'bodies' 
            will be a list of dicts of the bodies orbiting that star:
                    {   'id': '12345',
                        'image': 'p35-4',
                        'name': 'Sol 1',
                        'orbit': '1',
                        'ore': {   'anthracite': 500,
                                 ...
                                 'zircon': 1    },
            This list of bodies is ordered by id, not name or orbit as you might 
            expect.
        """
        pass

    @LacunaObject.set_empire_status
    @LacunaObject.call_member_meth
    def get_star_by_name( self, star_name, *args, **kwargs ):
        """ star_name must be an exact name, not a partial.  rv is identical to 
        get_star().
        """
        pass

    @LacunaObject.set_empire_status
    @LacunaObject.call_member_meth
    def get_star_by_xy( self, x, y, *args, **kwargs ):
        """x and y must be exact coords, not a range.  rv is identical to get_star().  """
        pass

    @LacunaObject.set_empire_status
    @LacunaObject.call_member_meth
    def search_stars( self, partial_name, *args, **kwargs ):
        """ partial_name must be at least 3 characters.  Matches up to 25 stars whose names
        START with partial_name (NOT stars whose names just contain partial_name).
        rv is a list, identical to get_star_map().
        """
        pass

    @LacunaObject.call_member_named_meth
    def probe_summary_fissures( self, mydict, *args, **kwargs ):
        """ mydict must contain the key 'zone', with a value of the zone you want to check,
        expressed in standard TLE zone notation (0|0).

        I currently can't find a zone with a fissure in it to test, but the documented value 
        of 'fissures' when one or more is found is a dict:
            "fissures" : {
                    "345" : {
                        "name"   : "Mercury",
                        "id"     : 345,
                        "orbit"  : 1,
                        "x"      : -40,
                        "y"      : 29,
                        "type"   : "habitable planet",
                        "image"  : "p13",
                        "size"   : 58,
                    },
                    "735" : {
                    ...
                    }
                }

        When there's no fissure existing (or known to you or your allies), rv is documented
        as being an empty list:
            "fissures" : None

        BE CAREFUL WITH THIS!  It looks like we're getting back a struct on a positive 
        response, but an empty list on a negative response.  Sigh.
        """
        pass


