

"""

    BODY OBJECT ATTRIBUTES {#{{{

        "id" : "id-goes-here",
        "x" : -4,
        "y" : 10,
        "star_id" : "id-goes-here",
        "star_name" : "Sol",
        "orbit" : 3,
        "type" : "habitable planet",
        "name" : "Earth",
        "image" : "p13",
        "size" : 67,
        "water" : 900,
        "ore" : {
            "gold" : 3399,
            "bauxite" : 4000,
            ...
        },
        "empire" : { # this section only exists if an empire occupies it
            "id" : "id-goes-here",
            "name" : "Earthlings",
            "alignment" : "ally",   # can be 'ally','self', or 'hostile'
            "is_isolationist" : 1
        },
        "station" : { # only shows up if this planet is under the influence of a space station
            "id" : "id-goes-here",
            "x" : 143,
            "y" : -27,
            "name" : "The Death Star"
        },

        ### The following will only be set if you own the body in question.

        "needs_surface_refresh" : 1, # indicates that the client needs to call get_buildings() because something has changed
        "building_count" : 7,
        "plots_available" :60,
        "happiness" : 3939,
        "happiness_hour" : 25,
        "unhappy_date" : "01 13 2014 16:11:21 +0600",  # Only given if happiness is below zero
        "propaganda_boost" : 20,
        "food_stored" : 33329,
        "food_capacity" : 40000,
        "food_hour" : 229,
        "energy_stored" : 39931,
        "energy_capacity" : 43000,
        "energy_hour" : 391,
        "ore_hour" 284,
        "ore_capacity" 35000,
        "ore_stored" 1901,
        "waste_hour" : 933,
        "waste_stored" : 9933,
        "waste_capacity" : 13000,
        "water_stored" : 9929,
        "water_hour" : 295,
        "water_capacity" : 51050,   
        "skip_incoming_ships" : 0,   # if set, then the following incoming data is missing.
        "num_incoming_enemy" : 10,   # total number of incoming foreign ships
        "num_incoming_ally" : 1,     # total number of incoming allied ships
        "num_incoming_own : 0,       # total number of incoming own ships from other colonies
        "incoming_enemy_ships" : [ # will only be included when enemy ships are coming to your planet (only the first 20 will be shown)
            {
                "id" : "id-goes-here",
                "date_arrives" : "01 31 2010 13:09:05 +0600",
                "is_own" : 1,                                   # is this from one of our own planets
                "is_ally" : 1                                   # is this from a planet within our alliance
            },
            ...
        ],
        "incoming_ally_ships" : [ # will only be included when allied ships are coming to your planet (only the first 10 will be shown)
            ...
        ],
        "incoming_own_ships" : [ # will only be included when ships from your other colonies are coming to your planet (only the first 10 will be shown)
            ...  
        ],
        
        ----- if the body is a station the following information will be included
        "alliance" : { 
            "id" : "id-goes-here",
            "name" : "Imperial Empire" 
        },
        "influence" : {
            "total" : 0,
            "spent" : 0
        }

    }#}}}

    Upon instantiation, the body's buildings are queried, and they end 
    up in two other attributes: buildings_id and buildings_name.

    "building dict", mentioned below, is documented in building.py.

    self.buildings_id is keyed off the individual building ID.
        self.buildings_id = {
            building_id_1 = { building dict },
            building_id_2 = { building dict },
            ...
        }

    self.buildings_name is keyed off the building's human-readable name.  
    Since most buildings can appear more than once on a given body, the value 
    is a list of buildings of this name.
        self.buildings_name = {
            'Apple Orchard' = [
                { building dict },
                { building dict },
                ...
            ],
            'Space Port' = [
                { building dict },
                { building dict },
                ...
            ],
            ...
        }

        The dicts in self.buildings_name are identical to the normal building 
        dict, except that an 'id' key has been added.

"""

import re
import lacuna.buildings
from lacuna.bc import LacunaObject
from lacuna.exceptions import \
    NoSuchBuildingError

class Body(LacunaObject):
    path = 'body'

    def __init__( self, client:object, body_id:int ):
        super().__init__( client )
        self.body_id = body_id

class MyBody(Body):

    def __init__( self, client:object, body_id:int ):
        super().__init__( client )
        ### I want self to start out populated, which would require a call to 
        ### get_status().  But since all the other methods also require a 
        ### status block, I can call set_buildings() instead (which is 
        ### decorated with get_buildings()) and get both the status data and 
        ### the building data in a single shot.
        self.set_buildings()

    def set_body_status( func ):
        """Decorator.
        Much like LacunaObject.set_empire_status.  Most of the Body server 
        methods return both empire status and body status.  So we'll still 
        decorate with LacunaObject.set_empire_status to get the empire status, 
        but we'll also decorate with this to set the body status.
        """
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

    def call_member_meth(func):
        """Decorator.  
        Just like LacunaObject.call_member_meth(), except that this version automatically
        sends the body_id.
        """
        def inner(self, *args, **kwargs):
            myargs = (self.client.session_id, self.body_id) + args
            rslt = self.client.send( self.path, func.__name__, myargs )
            kwargs['rslt'] = rslt
            func( self, *args, **kwargs )
            return rslt
        return inner

    @LacunaObject.set_empire_status
    @set_body_status
    @call_member_meth
    def get_status( self, *args, **kwargs ):
        pass

    @LacunaObject.set_empire_status
    @set_body_status
    @call_member_meth
    def get_buildings( self, *args, **kwargs ):
        """ Returns struct with key 'buildings'.  This struct is keyed off 
        building IDs.  Values are building structs as documented top of this 
        doc.
        """
        pass

    def get_building_id( self, classname:str, building_id:int ):
        """ Given a building's ID, returns the object for that building."""
        bldg_str = "lacuna.buildings.{}( self.client, self.body_id, building_id )".format( classname )
        return eval(bldg_str)

    def get_building_coords( self, x:int, y:int ):
        """ Given a building's coordinates, returns the object for that building."""
        for bid, bdict in self.buildings_id.items():
            if int(bdict['x']) == x and int(bdict['y']) == y:
                classname = re.sub("^/(\w+)", "\g<1>", bdict['url'] )
                bldg_str = "lacuna.buildings.{}( self.client, self.body_id, bid )".format( classname )
                return eval(bldg_str)
        else:
            raise NoSuchBuildingError("No building was found at ({},{})".format(x,y))

    def get_new_building( self, classname:str ):
        """ Returns a building object of the requested classname.
        This is a Potential building.
        """
        bldg_str = "lacuna.buildings.{}( self.client, self.body_id )".format( classname )
        return eval(bldg_str)

    def set_buildings( self ):
        """ Sets self.buildings_id and self.buildings_name.
        Called upon instantiation.
        """
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

    @LacunaObject.set_empire_status
    @set_body_status
    @call_member_meth
    def repair_list( self, building_ids_to_repair:list, *args, **kwargs ):
        """ Repairs all buildings indicated by ID in the passed-in list.

        Per the API docs, this should return a struct including key 
        'buildings', itself a struct of building_id => building_struct.  This 
        'buildings' struct will only contain buildings passed in 
        building_ids_to_repair.

        CHECK I haven't got any broken buildings handy to actually test this 
        retval, so I haven't been able to verify the paragraph above yet.
        """
        pass

    @LacunaObject.set_empire_status
    @set_body_status
    @call_member_meth
    def rearrange_buildings( self, arrangment_dicts:list, *args, **kwargs ):
        """ Moves one or more buildings to a new spot on the planet surface.

        arrangement_dicts is formatted as:
            [
                {
                    'id': integer ID of the building to move,
                    'x':  integer X coordinate to move to,
                    'y':  integer y coordinate to move to,
                },
                { another building to move, same format as above },
                ...
            ]

        Retval includes a key 'moved', which is a list of dicts of buildings 
        that were moved.  This returned list is identical to the list you 
        passed in except it also contains a 'name' key containing the 
        human-readable name of the moved building.

        Attempting to make an illegal move (moving a building out of -5..5 
        bounds, moving it on top of another building, moving the PCC at all, 
        etc) results in a 1013 server error and no moves are made, even if 
        others in the list were legal.
        """
        pass

    @LacunaObject.set_empire_status
    @set_body_status
    @call_member_meth
    def get_buildable( self, x:int, y:int, tag:str = '', *args, **kwargs ):
        """Returns a list of buildings that can be built on the indicated 
        coords.

        X and Y coordinate ints are required.

        A single string representing the tag to filter on is optional.  Some 
        examples of tags are: Now, Later, Happiness, Ore, Resources
        Sending an invalid tag is not an error, it simply returns zero 
        results.
        A complete list of tags can be found at:
            https://us1.lacunaexpanse.com/api/Body.html#get_buildable_%28_session_id%2C_body_id%2C_x%2C_y%2C_tag_%29

        Retval contains the key 'buildable', which is a list of dicts keyed 
        off the human-readable building name:
            [
                'Water Purification Plant': {
                    'build': {
                        'can': 1,
                        'cost': {   'energy': '64',
                                    'food': '72',
                                    'ore': '88',
                                    'time': '15',
                                    'waste': '16',
                                    'water': '8'
                                },
                        'no_plot_use': '',
                        'reason': '',
                        'tags': ['Resources', 'Water', 'Now']
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
                { another building struct },
                ...
            ]

        Throws 1009 if the passed coords are illegal for any reason (already 
        occupied, out-of-bounds, etc)
        """
        pass

    @call_member_meth
    def rename( self, name:str = '', *args, **kwargs ):
        """ Renames the current planet.

        For whatever reason, this returns int 1 on success.  NOT a struct 
        (like every other method), just a bare int.
        """
        pass

    @LacunaObject.set_empire_status
    @call_member_meth
    def abandon( self, *args, **kwargs ):
        """ Abandons the current planet.
        Retval contains the standard server and empire keys.

        I tested this on three planets on PT.  All three were abandoned 
        successfully.  However, on the first two, the server returned 
        something other than JSON.  Unfortunately, my NotJsonError exception 
        wasn't being imported properly, so it didn't manage to dump out was 
        _was_ returned.

        On the third test, after fixing the exception import, the server did 
        return actual JSON.

        I assume that the server was just having issues the first two times, 
        this is not uncommon on PT.
        """
        pass

