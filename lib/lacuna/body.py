
import functools, re
import lacuna.bc
import lacuna.alliance
import lacuna.building
import lacuna.buildings
import lacuna.buildings.ss_modules.parliament
import lacuna.empire
import lacuna.exceptions as err
import lacuna.map
import lacuna.resource
import lacuna.ship
from lacuna.exceptions import \
    NoSuchBuildingError

class Body(lacuna.bc.LacunaObject):
    """
    Object Attributes::

        id              "id-goes-here",
        x               -4,
        y               10,
        star_id         "id-goes-here",
        star_name       "Sol",
        orbit           3,
        type            "habitable planet",
        name            "Earth",
        image           "p13-3",
        surface_type    "p13",      # derived from 'image'
        size            67,
        water           900,
        ore             lacuna.resource.AvailableOre object
        empire          lacuna.empire.OwningEmpire object
                        Only exists if the body is inhabited
        station         lacuna.map.Station object
                        Only exists if the body is under the control of a space station.

    - :class:`lacuna.resource.AvailableOre`
    - :class:`lacuna.empire.OwningEmpire`
    - :class:`lacuna.map.Station`
    """

    path = 'body'

    def __init__( self, client:object, attrs:dict = {} ):
        self.body_id = int(attrs['id'])

        super().__init__( client, attrs )
        self._set_status_attr( attrs )
        ### Depending upon how the Body object was created, we may or may not 
        ### have an image attribute.  If we do, this will set the surface_type 
        ### attribute as well.
        self._derive_surface_type()

        ### CHECK see libsend_excavs.py.  Search for "UF".
        if not hasattr( self, 'star_name' ):
            self.client.module_logger.info( "Body ID {} has no star_name attribute.".format(self.id))


    def _derive_surface_type(self):
        ### 'image' == 'p16-1' or so.  The "-1" indicates the size of the 
        ### image, which will depend on the size of the planet, and we don't 
        ### care about that at all.  Just get the planet type, the "p16", out 
        ### of that.
        ### Roids will be 'a12-3', and GGs are 'pg10-3' (the numbers vary, the 
        ### format and letters do not.)
        if hasattr(self, 'image'):
            mymatch = re.match( "^((p|a)g?\d+)", self.image )
            if mymatch:
                self.surface_type = mymatch.group(1)
            else:
                self.surface_type = 'Unknown'

    def _set_body_status( func ):
        """ Decorator.
        Much like LacunaObject.set_empire_status.  Most of the Body server 
        methods return both empire status and body status.  So we'll still 
        decorate with LacunaObject.set_empire_status to get the empire status, 
        but we'll also decorate with this to set the body status.
        """
        @functools.wraps(func)
        def inner(*args, **kwargs):
            rv = func( *args, **kwargs )
            self = args[0]
            ### We _must_ check for 'status' before checking for body.
            ###
            ### In every case that includes a 'status' key, that's the status 
            ### dict we're looking for.
            ###
            ### But in at least one server method (get_buildings), there's a 
            ### 'body' key that is NOT the status dict we're looking for.  In 
            ### other cases (get_status), the 'body' key IS the status dict 
            ### we're looking for.
            ### So check 'status' first, then check 'body'.
            mydict = {}
            if 'status' in rv:
                if 'body' in rv['status']:
                    mydict = rv['status']['body']
                    del( rv['status']['body'] )
            elif 'body' in rv:
                mydict = rv['body']
                del( rv['body'] )

            if 'empire' in mydict:
                self.empire = lacuna.empire.OwningEmpire(self.client, mydict['empire'] )
                del mydict['empire']

            if 'station' in mydict:
                self.station = lacuna.map.Station(self.client, mydict['station'] )
                del mydict['station']

            if 'ore' in mydict:
                self.ore = lacuna.resource.AvailableOre(self.client, mydict['ore'] )
                del mydict['ore']

            if 'incoming_enemy_ships' in mydict:
                self.incoming_enemy_ships = []
                for i in mydict['incoming_enemy_ships']:
                    self.incoming_enemy_ships.append( lacuna.ship.IncomingToBodyShip(self.client, i) )
                del mydict['incoming_enemy_ships']

            if 'incoming_ally_ships' in mydict:
                self.incoming_ally_ships = []
                for i in mydict['incoming_ally_ships']:
                    self.incoming_ally_ships.append( lacuna.ship.IncomingToBodyShip(self.client, i) )
                del mydict['incoming_ally_ships']

            if 'incoming_own_ships' in mydict:
                self.incoming_own_ships = []
                for i in mydict['incoming_own_ships']:
                    self.incoming_own_ships.append( lacuna.ship.IncomingToBodyShip(self.client, i) )
                del mydict['incoming_own_ships']

            if 'alliance' in mydict:
                self.alliance = lacuna.alliance.FoundAlliance(self.client, mydict['alliance'] )
                del mydict['alliance']

            if 'influence' in mydict:
                self.influence = lacuna.alliance.Influence(self.client, mydict['influence'] )
                del mydict['influence']


            for n, v in mydict.items():
                setattr( self, n, self.get_type(v) )

            return rv
        return inner

    @_set_body_status
    def _set_status_attr( self, my_attrs:dict = {}, *args, **kwargs ):
        """ Fake up a status dict in the expected format, so the 
        _set_body_status decorator can properly set our attributes.
        """
        status = { 'body': my_attrs }
        return status


class MyBody(Body):
    """ A MyBody object is a planet or space station owned by the current 
    empire.  It has all of the attributes of a :class:`lacuna.body.Body` object, plus::

        needs_surface_refresh       1,  # client needs to call get_buildings() 
                                        # because something has changed
        building_count              7,
        plots_available             60,
        happiness                   3939,
        happiness_hour              25,
        unhappy_date                "01 13 2014 16:11:21 +0600",  
                                    # Only given if happiness is below zero
        propaganda_boost            20,
        food_stored                 33329,
        food_capacity               40000,
        food_hour                   229,
        energy_stored               39931,
        energy_capacity             43000,
        energy_hour                 391,
        ore_hour                    284,
        ore_capacity                35000,
        ore_stored                  1901,
        waste_hour                  933,
        waste_stored                9933,
        waste_capacity              13000,
        water_stored                9929,
        water_hour                  295,
        water_capacity              51050,   
        skip_incoming_ships         0,      # if set, the 'incoming' data below is missing.
        num_incoming_enemy          10,     # total incoming foreign ships
        num_incoming_ally           1,      # total incoming allied ships
        num_incoming_own            0,      # total incoming own ships
        incoming_enemy_ships        List of lacuna.ship.IncomingToBodyShip objects
                                    Will only be included when enemy ships are incoming
        incoming_ally_ships         List of lacuna.ship.IncomingToBodyShip objects
                                    Will only be included when allied ships are incoming
        incoming_own_ships          List of lacuna.ship.IncomingToBodyShip objects
                                    Will only be included when own ships are incoming
        buildings_id                {   building_id_1 = { building dict },
                                        building_id_2 = { building dict },   }
        buildings_name              {   'Apple Orchard' = [     { building dict },
                                                                { building dict },   ],
                                        'Space Port'    = [     { building dict },
                                                                { building dict },   ],
                                        'etc'           = [     { more of the same}, ]     }
        ### The following will only be set if the body is a space station.
        ### 
        alliance                    Lacuna.alliance.FoundAlliance object
        influence                   Lacuna.alliance.Influence object

    The ``building_dict`` dictionaries look like::

        'efficiency':   '100'
        'name':         'Police Station'
        'image':        'policestation'
        'level':        '25'
        'url':          '/policestation'
        'id':           '1234567'
        'y':            '3'
        'x':            '2'

    - :class:`lacuna.ship.IncomingToBodyShip`
    - :class:`lacuna.alliance.FoundAlliance`
    - :class:`lacuna.alliance.Influence`
    """
    ###
    ### The flow here, because it's mildly confusing:
    ###
    ###     - user calls client.get_body_byname('Earth')
    ###         - This is almost always how a MyBody will be constructed.
    ###         - At that point, the client only has 'name' and 'id' for the 
    ###           body.  The client calls MyBody's constructor with just those 
    ###           two bits of data.
    ### 
    ###     - MyBody's constructor calls _set_buildings
    ###         - which calls get_buildings
    ###             - This gets a status block which gets added as MyBody 
    ###               attributes
    ###             - Gets building dicts, does not instantiate them.
    ###                 - Creates buildings_id and buildings_name attrs
    ###             - So it's not till now that we've got a full MyBody object 
    ###               with actual data in it.
    ###
    ###     - So we usually can't _derive_surface_type (eg 'p35' from the 
    ###       image attribute (eg 'p35-2') until after we call 
    ###       _set_buildings().)
    ###       

    def __init__( self, client:object, attrs:dict = {} ):
        super().__init__( client, attrs )
        ### I want self to start out populated, which would require a call to 
        ### get_status().  But since all the other methods also require a 
        ### status block, I can call _set_buildings() instead (which is itself 
        ### calling get_buildings()) and get both the status data and the 
        ### building data in a single shot.
        self._set_buildings()
        self._derive_surface_type()

    @Body._set_body_status
    @lacuna.bc.LacunaObject.call_body_meth
    def get_status( self, blarg:int, *args, **kwargs ):
        """ Gets the status of the current body.
        This both returns a dict of status information, and sets the MyBody 
        object's attributes using that dict.
        
        Since every call to every method in this class also sets those 
        attributes, there should **never be a need to call this method.**
        """
        pass


    @Body._set_body_status
    @lacuna.bc.LacunaObject.call_body_meth
    def get_buildings( self, *args, **kwargs ):
        """ Returns all buildings on the planet.

        There shouldn't be any need to call this, as your MyBody object already 
        contains the information returned by this method (see the 
        ``buildings_id`` and ``buildings_name`` MyBody attributes).

        So this hasn't been cleaned up at all.  It returns a dict that includes 
        the with key ``buildings``.  This dict is keyed off building IDs, the 
        values are building dicts.
        """
        pass


    def get_building_id( self, classname:str, id:int ):
        """ Returns a building object by ID.

        Unless you're sure you want this and you know why, you don't want this.
        See ``get_building_coords()`` or ``get_buildings_bytype()`` instead.

        Args:
            classname (str): Name of the class of building
            building_id (int): Integer ID of the building
        Returns:
            lacuna.buildings.<TYPE>: An object of the requested building type.
        """
        bldg_str = "lacuna.buildings.{}( self.client, self.body_id, id )".format( classname )
        return eval(bldg_str)


    def get_building_coords( self, x:int, y:int ):
        """ Given a building's coordinates, returns the object for that building.

        Args:
            x (int): X coordinate on your planet's surface
            y (int): Y coordinate on your planet's surface
        Returns:
            lacuna.buildings.<BLDG>: the building object found on the requested coordinates.  The 
            class of object returned will vary depending on which building type 
            exists on those coords.
        Raises:
            lacuna.exceptions.NoSuchBuildingError: if no building exists on the requested coords.
        """
        for bid, bdict in self.buildings_id.items():
            if int(bdict['x']) == x and int(bdict['y']) == y:
                classname = re.sub("^/(\w+)", "\g<1>", bdict['url'] )
                bldg_str = "lacuna.buildings.{}( self.client, self.body_id, bid )".format( classname )
                mybldg =  eval(bldg_str)
                return mybldg
        else:
            raise NoSuchBuildingError("No building was found at ({},{})".format(x,y))


    def get_buildings_bytype( self, btype:str, min_level:int = 1, limit:int = 0, efficiency:int = 0 ):
        """ Get buildings of a specific type and minimum level.

        Args:
            btype (str): The type of building you want.  The type as given must 
                match *either* the "human name" of the building (eg "Ship Yard", 
                "Space Port"), or the classname of the building (eg "shipyard", 
                "spaceport").
            min_level (int): Minimum level of the building to return.  
                Defaults to 1.
            limit (int): Max number of this building you want returned.  
                Defaults to 0 (returns all buildings of this type).
            efficiency (int): Minimum efficiency of the buildings to 
                return.  If you're planning on actually using the buildings, 
                you'll want to set this to 100.  Defaults to 0.
        Returns:
            lacuna.buildings.<TYPE>: list.  *Note* a list is returned even if
                ``limit`` was set to 1.
        Raises:
            lacuna.exceptions.NoSuchBuildingError: if you don't have 
                any buildings of the requested type and level.

        Each building returned will have its ``view()`` method called 
        automatically.  So if you're going to get 10 buildings back, that's 
        10 ``view()`` calls that need to be made, and that's going to slow 
        things down a bit.  So keep that in mind, and turn caching on.
        """
        mylist = []
        for bid in sorted( self.buildings_id.keys() ):  # get the building IDs back in the same order every time - helps with caching.
            bdict = self.buildings_id[ bid ]
            classname = re.sub("^/(\w+)", "\g<1>", bdict['url'] )
    ### TEST
            if classname == btype:
                print( "Got a matching {}.  Its level is {}.  Min level is {}.".format(classname, bdict['level'], min_level) )
    ### TEST

            if bdict['name'] == btype or classname == btype and int(bdict['level']) >= min_level and int(bdict['efficiency']) >= efficiency:
                bldg_str = "lacuna.buildings.{}( self.client, self.body_id, bid )".format( classname )
                mylist.append( eval(bldg_str) )
                if limit and len(mylist) >= limit:
                    break
        if not len(mylist):
            raise err.NoSuchBuildingError("You don't have a {} building on {}.".format(btype, self.name))
        return mylist


    def get_new_building( self, classname:str ):
        """ Get a "new" building.

        Args:
            classname (str): Name of the class of building to build.  This 
                must be the classname, *not* the human readable name.  So 
                "spaceport" rather than "Space Port".
        Returns:
            lacuna.buildings.<classname>: A single object.

        This is a building that does not exist yet, but which you're getting 
        ready to build.
        """
        bldg_str = "lacuna.buildings.{}( self.client, self.body_id )".format( classname )
        return eval(bldg_str)


    def _set_buildings( self ):
        """ Called upon instantiation.  This derives the buildings_id and 
        buildings_name attributes.

        And since this is calling get_buildings(), which is decorated to update 
        the MyBody attributes based on the status block, this also creates 
        almost all of the other body attributes as well.
        """

        ### Instantiating a building object spends an RPC calling that 
        ### building's view() method.  We absolutely do not want to do that 
        ### for every building here, so leave both buildings_id and 
        ### buildings_name as dicts.  Don't get clever and turn those dicts 
        ### into objects.

        rv = self.get_buildings()
        self.buildings_id = rv['buildings']

        self.buildings_name = {}
        for id, bldg_dict in self.buildings_id.items():
            name = bldg_dict['name']
            if not name in self.buildings_name:
                self.buildings_name[name] = []
            ### Since we're causing this new dict to be keyed off name, we 
            ### have to make sure that the id is part of the dict now (it 
            ### wasn't before, because it was the key).
            bldg_dict['id'] = id
            self.buildings_name[name].append( bldg_dict )

    @lacuna.bc.LacunaObject.call_returning_body_meth
    def repair_list( self, ids_to_repair:list, *args, **kwargs ):
        """ Repairs all buildings indicated by ID in the passed-in list.

        Args:
            ids_to_repair (list of ints): IDs of buildings to attempt to 
                repair.
        Returns:
            lacuna.building.Building: list
        """
        pass
        mylist = []
        for bid, mydict in kwargs['rslt']['buildings'].items():
            mylist.append( lacuna.building.Building(self.client, mydict) )
        return mylist

    @lacuna.bc.LacunaObject.call_returning_body_meth
    def rearrange_buildings( self, arrangement:list, *args, **kwargs ):
        """ Moves one or more buildings to a new spot on the planet surface.

        Args:
            arrangement (list of dicts): describing your new surface arrangement::

                'id': integer ID of the building to move,
                'x':  integer X coordinate to move to,
                'y':  integer y coordinate to move to,
        Returns:
            lacuna.body.SimpleBody: list

        Attempting to make an illegal move (moving a building out of -5..5 
        bounds, moving it on top of another building, moving the PCC at all, 
        etc) raises ServerError 1013 and no moves are made, even if others in 
        the list were legal.
        """
        mylist = []
        for i in kwargs['rslt']['moved']:
            mylist.append( SimpleBody(self.client, i) )
        return mylist


    ### To view the laws from a planet, we have to pass the ID of the station 
    ### controlling the planet, not the ID of the planet itself, and none of 
    ### the existing decorators work that way.  Don't try to force some new 
    ### bogus one-off decorator, just make the call from here.
    def view_laws( self, *args, **kwargs ):
        """ View the laws affecting this planet.

        If the planet is not under the control of a space station, a single 
        'law' with the name "Not controlled by a station" will be returned.

        Note - I don't see any reason why a station couldn't pass a writ named 
        "Not controlled by a station", so be careful about just looking for a 
        law with that name and assuming it means that the star is really not 
        controlled by a station.

        Returns:
            lacuna.alliance.Law: list
        """
        mylist = [
            lacuna.alliance.Law(self.client, {
                'id':           0,
                'name':         'Not controlled by a station',
                'description':  'This planet is not under the control of a space station',
                'date_enacted': '12 31 1969 23:59:59 +0000',
            })
        ]
        if not hasattr(self, 'station'):
            return mylist

        myargs  = (self.client.session_id, self.station.id)
        mylist  = []
        rslt    = self.client.send( 'body', 'view_laws', myargs )

        for i in rslt['laws']:
            mylist.append( lacuna.alliance.Law(self.client, i) )
        return mylist


    def view_nonseizure_laws(self, *args, **kwargs):
        """ View the laws affecting this planet other than seizure laws.

        The bulk of the laws passed by most stations will be star seizure 
        laws, and these are almost always *not* what you're interested in when 
        checking laws.  So this method filters out the seizure laws and just 
        returns you the good stuff.

        Returns:
            lacuna.alliance.Law: list
        """
        laws = self.view_laws()
        interesting_laws = []
        for l in laws:
            if not re.match('^Seize', l.name):
                interesting_laws.append(l)
        return interesting_laws


    @lacuna.bc.LacunaObject.call_returning_body_meth
    def get_buildable( self, x:int, y:int, tag:str = '', *args, **kwargs ):
        """ 
        Get a list of buildings that can be built on the indicated coords.

        Args:
            x (int): X coordinate where you want to place the building
            y (int): Y coordinate where you want to place the building
            tag (optional str): Limit what gets returned.
        Returns:
            lacuna.body.Buildable: list
        Raises:
            ServerError: 1009 if the passed coords are illegal for any reason 
                (already occupied, out-of-bounds, etc)

        See :class:`lacuna.body.Buildable` for a list of valid tags.  Passing 
        an invalid tag as an argument is not an error, but zero results will be 
        returned.
        """
        mylist = []
        for name, subdict in kwargs['rslt']['buildable'].items():
            mylist.append( Buildable(self.client, name, subdict) )
        return mylist

    @lacuna.bc.LacunaObject.call_body_meth
    def rename( self, name:str = '', *args, **kwargs ):
        """ Renames the current planet.
        """
        ### For whatever reason, the server returns int 1 on success.  Not a 
        ### dict, just a bare int.
        pass

    @lacuna.bc.LacunaObject.call_body_meth
    def abandon( self, *args, **kwargs ):
        """ Abandons the current planet. """
        pass

class Planet(lacuna.bc.SubClass):
    """
    Object Attributes::

        id                  "id-goes-here",
        x                   -4,
        y                    10,
        z                   6,
        star_id             "id-goes-here",
        orbit               3,
        type                "habitable planet",
        name                "Earth",
        image               "p13",
        size                67,
        water               900,
        ore                 lacuna.resource.AvailableOre object
        building_count      7,
        population          470000,
        happiness           3939,
        happiness_hour      25,
        food_stored         33329,
        food_capacity       40000,
        food_hour           229,
        energy_stored       39931,
        energy_capacity     43000,
        energy_hour         391,
        ore_hour            284,
        ore_capacity        35000,
        ore_stored          1901,
        waste_hour          933,
        waste_stored        9933,
        waste_capacity      13000,
        water_stored        9929,
        water_hour          295,
        water_capacity      51050

    - :class:`lacuna.resource.AvailableOre`
    """
    def __init__(self, client, mydict:dict):
        if 'ore' in mydict:
            self.ore = lacuna.resource.AvailableOre(client, mydict['ore'] )
            del mydict['ore']
        super().__init__(client, mydict)


class JurisdictionPlanet(lacuna.bc.SubClass):
    """ A planet you don't necessarily own, that's orbiting a star in the 
    jurisdiction of one of your Space Stations, as returned by 
    ``lacuna.buildings.parliament.get_bodies_for_star_in_jurisdiction()``.

    Object Attributes::

        id          "id-goes-here" 
        star_id     "star-id-goes-here"
        star_name   "Sol"
        x           0
        y           1
        size        45
        image       'a18-1',
        ore         lacuna.resource.StoredResources object
        zone        '0|0'
        orbit       '3'
        name        'Earth'
        type        'asteroid'
        ### 
        ### 'station' will only appear if the planet's star has been seized by 
        ### a space station.
        station     lacuna.map.Station object

    - :class:`lacuna.resource.AvailableOre`
    - :class:`lacuna.map.Station`

    """
    def __init__(self, client, mydict:dict):
        mydict['station']   = lacuna.map.Station(client, mydict['station'])
        mydict['ore']       = lacuna.resource.StoredResources(client, mydict['ore'])
        super().__init__(client, mydict)

class Buildable(lacuna.bc.SubClass):
    """ A building to be built on a given plot.

    Object Attributes::

        name                Wheat Farm
        url                 /wheat
        building_class      wheat
        image               wheat1
        can_build           1 or 0
        reason              Only shows up if 'can_build' is 0, in which case 
                            this will be a string explaining why the building 
                            cannot be built.
        extra_level         7,
                            Only shows up for some plan types, skips level 1 
                            and goes straight to this level
        tags                List of build tags applying to this building (see below)
        cost                lacuna.resource.BuildCost object
        production          lacuna.resource.Production object

    - :class:`lacuna.resource.BuildCost`
    - :class:`lacuna.resource.Production`

    Possible build tags:
        - **Now** -- Can be built right now.
        - **Soon** -- Could be built right now if only there were enough resources in storage.
        - **Later** -- Will eventually become available once you've completed the necessary prerequisites.
        - **Plan** -- This building will be built using a Plan, which means it will cost no resources to build.
        - **Infrastructure** -- Everything that is not a resource building.

          - **Intelligence** -- This building helps you gain information.
          - **Happiness** -- This building helps you gain favor with your citizens.
          - **Ships** -- This building helps you build ships.
          - **Colonization** -- This building helps you colonize other worlds.
          - **Construction** -- This building helps in some way building buildings on your planet surface.
          - **Trade** -- This building allows you to trade good or resources with other players, or assists in trade in some way.

        - **Resources** -- Everything that is not infrastructure.

          - **Food** -- This building either produces or stores food.
          - **Ore** -- This building either produces or stores ore.
          - **Water** -- This building either produces or stores water.
          - **Energy** -- This building either produces or stores energy.
          - **Waste** -- This building either consumes or stores waste.
          - **Storage** -- This building provides storage for one or more of the five resources.

    """
    def __init__(self, client, name, mydict):
        self.client = client
        self.name   = name

        mymatch = re.match( "^/(\w+)", mydict['url'] )
        if mymatch:
            self.building_class = mymatch.group(1)
        else:
            self.building_class = 'Unknown'

        self.can_build  = mydict['build']['can']
        self.tags       = mydict['build']['tags']
        self.reason     = mydict['build']['reason']

        if 'cost' in mydict['build']:
            self.cost = lacuna.resource.BuildCost( client, mydict['build']['cost'] )

        if 'production' in mydict['build']:
            self.production = lacuna.resource.Production( client, mydict['build']['production'] )

        if 'extra_level' in mydict['build']:
            self.extra_level = mydict['build']['extra_level']


class SpaceStation(lacuna.bc.SubClass):
    """
    Object Attributes::

        id          "id-goes-here",
        name        "Earth"
        x           100
        y           -250
    """


class SimpleBody(lacuna.bc.SubClass):
    """
    Object Attributes::

        id          "id-goes-here",
        name        "Earth"
        x           100
        y           -250
        image       "p35"
    """


class ShipDest(lacuna.bc.SubClass):
    """ Where a ship is travelling to or from.

    Object Attributes::

        id          "id-goes-here",
        type        "body"
        name        "Earth"
    """


class ShipHub(lacuna.bc.SubClass):
    """ The body an orbiting ship is orbiting.

    Object Attributes::
        id          "id-goes-here",
        type        "body"
        name        "Earth"
        x           100
        y           250
    """

