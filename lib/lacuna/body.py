
import functools, re
import lacuna.buildings
import lacuna.bc
from lacuna.exceptions import \
    NoSuchBuildingError

class Body(lacuna.bc.LacunaObject):
    """
    Attributes:

    ::

        id                          "id-goes-here",
        x                           -4,
        y                           10,
        star_id                     "id-goes-here",
        star_name                   "Sol",
        orbit                       3,
        type                        "habitable planet",
        name                        "Earth",
        image                       "p13",
        size                        67,
        water                       900,
        ore                         {   "gold" : 3399,
                                        "bauxite" : 4000,
                                        etc
                                    },
        empire                      { # only exists if the body is inhabited
                                        "id" : "id-goes-here",
                                        "name" : "Earthlings",
                                        "alignment" : "ally",   # can be 'ally','self', or 'hostile'
                                        "is_isolationist" : 1
                                    },
        station                     { # only shows up if this planet is under the influence of a space station
                                        "id" : "id-goes-here",
                                        "x" : 143,
                                        "y" : -27,
                                        "name" : "The Death Star"
                                    },
        ### The following will only be set if you own the body in question.
        ### 
        needs_surface_refresh       1,  # indicates that the client needs to call get_buildings() because something has changed
        building_count              7,
        plots_available             60,
        happiness                   3939,
        happiness_hour              25,
        unhappy_date                "01 13 2014 16:11:21 +0600",  # Only given if happiness is below zero
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
        skip_incoming_ships         0,      # if set, then the following incoming data is missing.
        num_incoming_enemy          10,     # total number of incoming foreign ships
        num_incoming_ally           1,      # total number of incoming allied ships
        num_incoming_own            0,      # total number of incoming own ships from other colonies
        incoming_enemy_ships         [
                                        # will only be included when enemy ships are coming to 
                                        # your planet (only the first 20 will be shown)
                                        {
                                            "id" : "id-goes-here",
                                            "date_arrives" : "01 31 2010 13:09:05 +0600",
                                            "is_own" : 1,                                   # is this from one of our own planets
                                            "is_ally" : 1                                   # is this from a planet within our alliance
                                        },
                                        etc
                                    ],
        incoming_ally_ships         [
                                        # will only be included when allied ships are coming to 
                                        # your planet (only the first 10 will be shown)
                                        etc
                                    ],
        incoming_own_ships          [
                                        # will only be included when ships from your other 
                                        # colonies are coming to your planet (only the first 
                                        # 10 will be shown)
                                        etc  
                                    ],
        ### The following will only be set if the body is a space station.
        ### 
        alliance                    { 
                                        "id" : "id-goes-here",
                                        "name" : "Imperial Empire" 
                                    },
        influence                   {
                                        "total" : 0,
                                        "spent" : 0
                                    }

    """

    path = 'body'

    def __init__( self, client:object, attrs:dict = {} ):
        super().__init__( client )
        self.body_id = attrs['id']

        ### 'image' == 'p16-1' or so.  The "-1" indicates the size of the 
        ### image, which will depend on the size of the planet, and we don't 
        ### care about that at all.  Just get the planet type, the "p16", out 
        ### of that.
        if 'image' in attrs:
            mymatch = re.match( "^(p\d+)", attrs['image'] )
            if mymatch:
                attrs['surface_type'] = mymatch.group(1)

        for k, v in attrs.items():
            setattr(self, k, v)
        self._set_status_attr( attrs )

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
            for n, v in mydict.items():
                setattr( self, n, v )
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
    empire.

    Attributes:

    ::

        id                  "id-goes-here",
        x                   -4,
        y                   10,
        star_id             "id-goes-here",
        star_name           "Sol",
        orbit               3,
        type                "habitable planet",
        name                "Earth",
        image               "p13",
        size                67,
        water               900,
        ore                 {
                                "gold" : 3399,
                                "bauxite" : 4000,
                                etc
                            },
        empire                  {
                                    "id" : "id-goes-here",
                                    "name" : "Earthlings",
                                    "alignment" : "ally",   # can be 'ally','self', or 'hostile'
                                    "is_isolationist" : 1
                                },
        station                 { # only shows up if this planet is under the influence of a space station
                                    "id" : "id-goes-here",
                                    "x" : 143,
                                    "y" : -27,
                                    "name" : "The Death Star"
                                },
        needs_surface_refresh   1, # indicates that the client needs to call get_buildings() because something has changed
        building_count          7,
        plots_available         0,
        happiness               3939,
        happiness_hour          25,
        unhappy_date            "01 13 2014 16:11:21 +0600",  # Only given if happiness is below zero
        propaganda_boost        20,
        food_stored             33329,
        food_capacity           40000,
        food_hour               229,
        energy_stored           39931,
        energy_capacity         43000,
        energy_hour             391,
        ore_hour                284,
        ore_capacity            35000,
        ore_stored              1901,
        waste_hour              ,
        waste_stored            9933,
        waste_capacity          13000,
        water_stored            9929,
        water_hour              295,
        water_capacity          51050,   
        skip_incoming_ships     0,   # if set, then the following incoming data is missing.
        num_incoming_enemy      10,   # total number of incoming foreign ships
        num_incoming_ally       1,     # total number of incoming allied ships
        num_incoming_own : 0,   # total number of incoming own ships from other colonies
        incoming_enemy_ships    [ # will only be included when enemy ships are coming to your planet (only the first 20 will be shown)
                                    {
                                        "id" : "id-goes-here",
                                        "date_arrives" : "01 31 2010 13:09:05 +0600",
                                        "is_own" : 1,   # is this from one of our own planets
                                        "is_ally" : 1   # is this from a planet within our alliance
                                    },
                                    etc
                                ],
        incoming_ally_ships     [ # will only be included when allied ships are coming to your planet (only the first 10 will be shown)
                                    etc
                                ],
        incoming_own_ships      [ # will only be included when ships from your other colonies are coming to your planet (only the first 10 will be shown)
                                    etc  
                                ],
        ### The following will only be set if the body is a space station.
        ### 
        alliance                { 
                                    "id" : "id-goes-here",
                                    "name" : "Imperial Empire" 
                                },
        influence               {
                                    "total" : 0,
                                    "spent" : 0
                                }
        ### The *building dict*s mentioned below are dicts containing the 
        ### information represented by a building.MyBuilding's attributes.
        buildings_id            {
                                    building_id_1 = { building dict },
                                    building_id_2 = { building dict },
                                    etc,
                                }
        buildings_name          {
                                    'Apple Orchard' = [
                                        ### These are lists, as we're going to 
                                        ### have multiple instances of certain 
                                        ### building types.
                                        { building dict },
                                        { building dict },
                                        etc
                                    ],
                                    'Space Port' = [
                                        { building dict },
                                        { building dict },
                                        etc
                                    ],
                                    etc
                                }
    """

    def __init__( self, client:object, body_id:int, attrs:dict = {} ):
        attrs['id'] = body_id
        super().__init__( client, attrs )
        ### I want self to start out populated, which would require a call to 
        ### get_status().  But since all the other methods also require a 
        ### status block, I can call _set_buildings() instead (which is itself 
        ### calling get_buildings()) and get both the status data and the 
        ### building data in a single shot.
        self._set_buildings()

    @Body._set_body_status
    @lacuna.bc.LacunaObject.call_body_meth
    def get_status( self, blarg:int, *args, **kwargs ):
        """ Gets status of the current body.
        This both returns a dict of status information, and sets the MyBody 
        object's using that dict.  Since every call to every method in this 
        class also sets those attributes, there should never be a need to call 
        this method.
        """
        pass

    @Body._set_body_status
    @lacuna.bc.LacunaObject.call_body_meth
    def get_buildings( self, *args, **kwargs ):
        """ Returns dict with key 'buildings'.  This dict is keyed off 
        building IDs.  Values are building dicts as documented by 
        get_buildable().
        """
        pass

    def get_building_id( self, classname:str, id:int ):
        """ Given a building's ID, returns the object for that building."""
        bldg_str = "lacuna.buildings.{}( self.client, self.body_id, id )".format( classname )
        return eval(bldg_str)

    def get_building_coords( self, x:int, y:int ):
        """ Given a building's coordinates, returns the object for that building."""
        for bid, bdict in self.buildings_id.items():
            if int(bdict['x']) == x and int(bdict['y']) == y:
                classname = re.sub("^/(\w+)", "\g<1>", bdict['url'] )
                bldg_str = "lacuna.buildings.{}( self.client, self.body_id, bid )".format( classname )
                mybldg =  eval(bldg_str)
                return mybldg
        else:
            raise NoSuchBuildingError("No building was found at ({},{})".format(x,y))

    def get_new_building( self, classname:str ):
        """ Returns a building object of the requested classname.
        This is a Potential building.
        """
        bldg_str = "lacuna.buildings.{}( self.client, self.body_id )".format( classname )
        return eval(bldg_str)

    def _set_buildings( self ):
        """ Sets self.buildings_id and self.buildings_name.
        Called upon instantiation.
        """
        ### Instantiating a building object spends an RPC calling that 
        ### building's view() method.  We absolutely do not want to do that 
        ### for every building here, so leave both buildings_id and 
        ### buildings_name as dicts.

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

    @Body._set_body_status
    @lacuna.bc.LacunaObject.call_body_meth
    def repair_list( self, building_ids_to_repair:list, *args, **kwargs ):
        """ Repairs all buildings indicated by ID in the passed-in list.

        Requires a list of building IDs to be repaired.

        Returns a dict including the key 'buildings', containing:
            - id -- building dict
        """
        pass

    @Body._set_body_status
    @lacuna.bc.LacunaObject.call_body_meth
    def rearrange_buildings( self, arrangement:list, *args, **kwargs ):
        """ Moves one or more buildings to a new spot on the planet surface.

        Arguments:
            - arrangement -- A list of dicts describing your new surface arrangement

                ::

                    [
                        {
                            'id': integer ID of the building to move,
                            'x':  integer X coordinate to move to,
                            'y':  integer y coordinate to move to,
                        },
                        { another building to move, same format as above },
                        etc
                    ]

        Returns a dict including the key 'moved', which is a list of dicts of 
        buildings that were moved.  This returned list is identical to the 
        list you passed in except it also contains a 'name' key containing the 
        human-readable name of the moved building.

        Attempting to make an illegal move (moving a building out of -5..5 
        bounds, moving it on top of another building, moving the PCC at all, 
        etc) raises ServerError 1013 and no moves are made, even if others in 
        the list were legal.
        """
        pass

    @Body._set_body_status
    @lacuna.bc.LacunaObject.call_body_meth
    def get_buildable( self, x:int, y:int, tag:str = '', *args, **kwargs ):
        """ 
        Get a list of buildings that can be built on the indicated coords.

        Arguments:
            - x -- Required integer X coordinate where you want to place the building
            - y -- Required integer Y coordinate where you want to place the building
            - tag -- Optional string to limit what gets returned.

        Tags are analogous to the buttons and drop-down box that appear in the 
        build menu in the browser client, such as Now, Later, Happiness, Ore, 
        Resources, etc.

        A complete list of tags can be found at:
        https://us1.lacunaexpanse.com/api/Body.html#get_buildable_%28_session_id%2C_body_id%2C_x%2C_y%2C_tag_%29

        Sending an invalid tag is not an error, it simply returns zero 
        results.

        Returns a dict that includes the key 'buildable', which is a list of 
        dicts keyed off the human-readable building name:
 
            ::

                buildable = [
                    'Water Purification Plant': {
                        'build': {
                            'can': 1,
                            'cost': {
                                'energy': '64',
                                'food': '72',
                                'ore': '88',
                                'time': '15',
                                'waste': '16',
                                'water': '8'
                            },
                            'no_plot_use': '',
                            'reason': '',
                            'tags': [
                                'Resources', 
                                'Water', 
                                'Now'
                            ]
                        },
                        'image': 'waterpurification0',
                        'production': {
                            'energy_capacity': 0,
                            'energy_hour': '-3',
                            'food_capacity': 0,
                            'food_hour': '-1',
                            'happiness_hour': '0',
                            'ore_capacity': 0,
                            'ore_hour': '-3',
                            'waste_capacity': 0,
                            'waste_hour': '5',
                            'water_capacity': 0,
                            'water_hour': '31'
                        },
                        'url': '/waterpurification'
                    },
                ]

    Raises ServerError 1009 if the passed coords are illegal for any reason (already 
    occupied, out-of-bounds, etc)
    """
    pass

    @lacuna.bc.LacunaObject.call_body_meth
    def rename( self, name:str = '', *args, **kwargs ):
        """ Renames the current planet.

        For whatever reason, this returns int 1 on success.  Not a dict (like 
        every other method), just a bare int.
        """
        pass

    @lacuna.bc.LacunaObject.call_body_meth
    def abandon( self, *args, **kwargs ):
        """ Abandons the current planet. """
        pass

class Planet(lacuna.bc.SubClass):
    """
    Attributes:

    ::

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
        ore                 {
                                "gold" : 3399,
                                "bauxite" : 4000,
                                etc,
                            },
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
    """

class SpaceStation(lacuna.bc.SubClass):
    """
    Attributes:

    ::

        id                  "id-goes-here",
        name                "ISS",
        x                   -4,
        y                    10,
    """



