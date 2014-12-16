
import lacuna.bc
import lacuna.alliance
import lacuna.body
import re

class Map(lacuna.bc.LacunaObject):
    """ Provides access to the starmap.  """

    path = 'map'

    @lacuna.bc.LacunaObject.call_named_returning_meth
    def get_star_map( self, stars:dict, *args, **kwargs ):
        """ Get a list of stars occupying a region of space.
        
        Accepts a single dict of arguments containing the keys:
            - left -- Coordinate
            - top -- Coordinate
            - right -- Coordinate
            - bottom -- Coordinate

        Each coordinate must be an integer within the star map (so >= -1500 
        and <= 1500).  The total area covered by these coordinates must be <= 
        3001 units.  The TLE documentation states 1001 units, but thats old 
        information; the limit has been raised to 3001 units.

        Returns a list of map.Star objects.

        Raises ServerError 1003 if your selected area is too large.
        """
        mylist = []
        for i in kwargs['rslt']['stars']:
            mylist.append( Star(self.client, i) )
        return mylist

    @lacuna.bc.LacunaObject.call_returning_meth
    def get_stars( self, left:int, top:int, right:int, bottom:int, *args, **kwargs ):
        """ Get a list of stars occupying a region of space.

        More or less Deprecated.

        This is not officially deprecated, but there's no good reason to use it.  
        get_star_map() is using the newer named arguments calling method, and it 
        allows you a range of 3001 units, whereas this method uses the old 
        positional arguments calling method, and allows a range of only 900 
        units.

        Arguments:
            - left -- Coordinate
            - top -- Coordinate
            - right -- Coordinate
            - bottom -- Coordinate

        Returns a list of map.Star objects.

        Raises ServerError 1003 if your selected area is too large.
        """
        mylist = []
        for i in kwargs['rslt']['stars']:
            mylist.append( Star(self.client, i) )
        return mylist

    @lacuna.bc.LacunaObject.call_returning_meth
    def check_star_for_incoming_probe( self, star_id, *args, **kwargs ):
        """ Check if you have a probe en route to a star.

        Arguments
            - star_id -- Integer ID of the star to check

        Returns
            - incoming_probe -- This will be the date of arrival of the incoming probe, or 0 if no probe is on its way.
        """
        return kwargs['rslt']['incoming_probe'] if 'incoming_probe' in kwargs['rslt'] else 0

    @lacuna.bc.LacunaObject.call_returning_meth
    def get_star( self, star_id:int, *args, **kwargs ):
        """ Find a star by its ID.

        Arguments:
            - star_id -- Integer ID of the star

        Returns a map.Star object.  
        """
        star = Star( self.client, kwargs['rslt']['star'] )
        return(star)

    @lacuna.bc.LacunaObject.call_returning_meth
    def get_star_by_name( self, star_name:str, *args, **kwargs ):
        """ Find a star by its name.

        Arguments:
            - star_name -- String name of the star.  This is NOT a "standard 
              TLE search string", but the full name of the star.

        Returns a map.Star object.  
        """
        star = Star( self.client, kwargs['rslt']['star'] )
        return star

    @lacuna.bc.LacunaObject.call_returning_meth
    def get_star_by_xy( self, x:int, y:int, *args, **kwargs ):
        """ Find a star by its x, y coordinates.

        Arguments:
            - x -- Integer X coordinate
            - y -- Integer Y coordinate

        Returns a map.Star object.  
        """
        star = Star( self.client, kwargs['rslt']['star'] )
        return star

    @lacuna.bc.LacunaObject.call_returning_meth
    def search_stars( self, partial_name:str, *args, **kwargs ):
        """ Return a list of stars matching a string.

        Arguments
            - search_string -- A standard TLE search string.  See 
              :ref:`glossary`.

        Returns a list of map.Star objects.
        """
        mylist = []
        for i in kwargs['rslt']['stars']:
            mylist.append( Star(self.client, i) )
        return mylist

    @lacuna.bc.LacunaObject.call_named_returning_meth
    def probe_summary_fissures( self, mydict:dict, *args, **kwargs ):
        """ Provides info on fissures in a zone.

        Requires a single dict argument containing the key:
            - zone -- '0|0'

        Returns a list of map.Fissure objects.
        """
        ### kwargs['rslt']['fissures'] is either a dict
        ### (fissure_id: fissure_dict) OR it points to nothing.  Not an empty 
        ### dict, just nothing.  fissure_dict, btw, _does_ contain the fissure 
        ### id again.
        mylist = []
        if kwargs['rslt']['fissures']:
            for f_id, f_dict in kwargs['rslt']['fissures'].items():
                mylist.append( Fissure(self.client, f_dict) )
        return mylist

    ### 
    ### Non-API methods
    ###

    def get_orbiting_planet( self, star_name:str, planet_name:str ):
        """ Get the info of any planet you can see in your star map.

        Arguments
            - star_name -- String name of a star
            - planet_name -- String name of a planet orbiting that star

        Returns a body.Body object
        """
        my_map = self.client.get_map()
        star = my_map.get_star_by_name(star_name)
        target_planet = ''
        for i in star.bodies:
            if i.name == planet_name:
                target_planet = i
        if not target_planet:
            raise KeyError("Unable to find target planet", planet_name, ".")
        return target_planet


class Star(lacuna.bc.SubClass):
    """ 
    Attributes::

        color       'red',
        id          '12345',
        name        'Clou Oghofr Oap',
        x           '100',
        y           '-100',
        zone        '0|0',
        bodies:     List of body.Body objects.  If you don't have the star 
                    probed or oracled, this list will be empty.
        station:    lacuna.map.Station object (only if this star is under control of a station)
    """
    def __init__( self, client, star_dict:dict, *args, **kwargs ):
        if 'status' in star_dict:
            del( star_dict['status'] )

        body_objs = []
        if 'bodies' in star_dict:
            for b in star_dict['bodies']:
                body_objs.append( lacuna.body.Body(self, b) )
            del( star_dict['bodies'] )
        self.bodies = body_objs

        if 'station' in star_dict and type(star_dict['station']) is dict:
            star_dict['station'] = Station(client, star_dict['station'])

        super().__init__(client, star_dict)


    ### There's no actual Star class on the server, and trying to shoehorn 
    ### this class under Map or Body just so we can use the decorators there 
    ### is bogus, so we're making the actual server call here rather than 
    ### using a decorator.
    def view_laws(self, *args, **kwargs):
        """ View the laws affecting this star.

        If the star is not under the control of a space station, a single 
        'law' with the name "Not controlled by a station" will be returned.

        Note - I don't see any reason why a station couldn't pass a writ named 
        "Not controlled by a station", so be careful about just looking for a 
        law with that name and assuming it means that the star is really not 
        controlled by a station.

        Returns a list of lacuna.alliance.Law objects.
        """
        myargs = (self.client.session_id, self.id)
        rslt = self.client.send( 'map', 'view_laws', myargs )

        mylist = []
        for i in rslt['laws']:
            mylist.append( lacuna.alliance.Law(self.client, i) )
        return mylist

    def view_nonseizure_laws(self, *args, **kwargs):
        """ View the laws affecting this star other than seizure laws.

        The bulk of the laws passed by most stations will be star seizure 
        laws, and these are almost always *not* what you're interested in when 
        checking laws.  So this method filters out the seizure laws and just 
        returns you the good stuff.

        Returns a list of lacuna.alliance.Law objects.
        """
        laws = self.view_laws()
        interesting_laws = []
        for l in laws:
            if not re.match('^Seize', l.name):
                interesting_laws.append(l)
        return interesting_laws


class StationStar(lacuna.bc.SubClass):
    """ A star in the jurisdiction of a space station, as returned by 
    ``lacuna.buildings.parliament.get_stars_in_jurisdiction()``.

    Attributes::

        name        "Sol",
        color       "yellow",
        x           -41,
        y           27,
        zone        "0|1",
    """


class Station(lacuna.bc.SubClass):
    """
    Attributes::

        id          "id-goes-here",
        x           143,
        y           -27,
        name        "The Death Star"
        alliance    lacuna.alliance.SeizingAlliance object.
    """
    def __init__(self, client, mydict):
        if 'alliance' in mydict:
            mydict['alliance'] = lacuna.alliance.SeizingAlliance(client, mydict['alliance'])
        super().__init__(client, mydict)

    def view_laws( self, *args, **kwargs ):
        """ Returns a list of lacuna.parliament.Law objects.  Otherwise returns 
        an empty list.

        DOES NOT WORK if your alliance doesn't own the station.
        """
        ### This is still hokey.  See the comments in 
        ### lacuna.body.Body.view_laws().  This is a copy/paste of that.
        ###
        ### As of 12/03/2014, this is in the production docs as working, but 
        ### it doesn't work (and that fact has been known and commented on as 
        ### long as four months ago.  That's what I get for believing docs.  
        ### Sigh.)
        ###
        ### For whatever reason, Python won't let this Station class inherit 
        ### from lacuna.body.Body - it tells me that the 'lacuna' object has 
        ### no attribute 'body'.  I think Python is sniffing glue.  Anyway, 
        ### I'm done fucking around with trying to figure out why that's 
        ### breaking, so here's a pasted (and then massaged) method.
        mylist = []
        myargs = (self.client.session_id, self.id)
        rslt = self.client.send( 'parliament', 'view_laws', myargs )
        for i in rslt['laws']:
            mylist.append( lacuna.buildings.ss_modules.parliament.Law(self.client, i) )
        return mylist



class Fissure(lacuna.bc.SubClass):
    """
    Attributes::

        name     "Mercury",
        id       345,
        orbit    1,
        x        -40,
        y        29,
        type     "habitable planet",
        image    "p13",
        size     58,
    """

