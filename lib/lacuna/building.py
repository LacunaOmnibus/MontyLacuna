
"""
    Building is a base class, extending LacunaObject.

    LacunaObject requires a path 'class' variable, but Building does not 
    provide it; any module extending Building must provide that path variable.

    building dict example: {#{{{
        This is what comes back from a server call to view().  These keys become
        attributes of the building object.

        {
            "name" : "Apple Orchard",
            "x" : 1,
            "y" : -1,
            "url" : "/apple",
            "level" : 3,
            "image" : "apples3",
            "efficiency" : 95,
            "pending_build" : {            # only included when building is building/upgrading
                "seconds_remaining" : 430,
                "start" : "01 31 2010 13:09:05 +0600",
                "end" : "01 31 2010 18:09:05 +0600"
            },
            "work" : {                     # only included when building is working (Parks, Waste Recycling, etc)
                "seconds_remaining" : 49,
                "start" : "01 31 2010 13:09:05 +0600",
                "end" : "01 31 2010 18:09:05 +0600"
            }
        },
    }#}}}

    There are two types of Building objects:
            - Potential buildings
            - Existing buildings
    A Potential building doesn't exist yet.  Its constuctor requires a body_id 
    but no building_id.  A Potential building can't do anything but call 
    build().  After calling build(), the Potential building becomes an 
    Existing building.

    do_upgrade(), do_downgrade()
    The published (server) method names for these are "upgrade()" and 
    "downgrade()".  However, we've got status attributes by those names, and 
    attributes overwrite methods of the same name.
    So these have been renamed, adding the "do_" prefix" to avoid attribute 
    name collisions.

"""

import re
from lacuna.bc import LacunaObject
from lacuna.exceptions import \
    CaptchaResponseError, \
    ServerError

class Building(LacunaObject):

    def __init__( self, client, body_id:int, building_id:int = 0 ):
        super().__init__( client )
        self.body_id = body_id
        if building_id:
            self.building_id = building_id
            rv = self.client.send( self.path, 'view', (self.client.session_id, building_id) )
            self.write_building_status( rv )

    def call_building_meth(func):
        """Decorator.
        Calls a server method that requires a building_id, but no body_id.
        This is the decorator that most Building methods will use.
        Methods using this decorator get the original server result handed 
        back to them in **kwargs['rslt'].
        """
        def inner(self, *args, **kwargs):
            method_to_call = re.sub('^do_', '', func.__name__)
            myargs = (self.client.session_id, self.building_id) + args
            rslt = self.client.send( self.path, method_to_call, myargs )
            kwargs['rslt'] = rslt
            #server_result = {'rslt': rslt}
            #func( self, *args, **server_result )
            func( self, *args, **kwargs )
            return rslt
        return inner

    def call_building_named_meth(func):
        """Decorator.  
        Calls a server method that requires a building_id, but no body_id.
        Expects named arguments.  This is the 'new' way of doing it, but there are
        fairly few methods that work this way.  See generate_singularity()
        """
        def inner( self, mydict:dict ):
            mydict['session_id'] = self.client.session_id
            mydict['building_id'] = self.building_id
            rslt = self.client.send( self.path, func.__name__, (mydict,) )
            func( self, mydict )
            return rslt
        return inner

    def call_naked_meth(func):
        """Decorator.
        Some building methods require neither a body_id nor a building_id (see 
        spaceport.py for examples).
        Methods using this decorator get the original server result handed 
        back to them in **kwargs['rslt'].
        """
        def inner(self, *args):
            myargs = (self.client.session_id,) + args
            rslt = self.client.send( self.path, func.__name__, myargs )
            server_result = {'rslt': rslt}
            func( self, *args, **server_result )
            return rslt
        return inner

    def require_existing(func):
        """Decorator.
        Many building methods only make sense to be called on a building that 
        actually already exists.  Add this decorator to those methods.
        """
        def inner(self, *args):
            if not self.building_id:
                raise AttributeError( "{} requires an already-existing building.".format(func.__name__) )
            func(self, args)
            return rslt
        return inner

    def set_building_status( func ):
        """Decorator.
        Much like LacunaObject.set_empire_status.  A few of the Building server 
        methods return both empire status and building status.  So we'll still 
        decorate with LacunaObject.set_empire_status to get the empire status, 
        but we'll also decorate with this to set the body status.
        """
        def inner(*args, **kwargs):
            rv = func( *args, **kwargs )
            self = args[0]
            self.write_building_status( rv )
            return rv
        return inner

    def write_building_status( self, rv:dict ):
        mydict = {}
        if 'building' in rv:
            mydict = rv['building']
            del( rv['building'] )
        for n, v in mydict.items():
            setattr( self, n, v )

    def build( self, x:int, y:int, **kwargs ):
        """ Actually places a building on the requested coords, assuming the building is
        buildable, the coords are empty, and a plot is available.
        After calling build(), your "new building" object will be be an "existing building"
        object, capable of calling the rest of the building methods.
        """
        ### build() is unique, as it requires a body_id but no building_id, 
        ### since the building doesn't exist yet.  No decorators here; the 
        ### call to view() after the building is placed will handle that.
        rv = self.client.send( self.path, 'build', (self.client.session_id, self.body_id, x, y) )
        rv['building']['building_id'] = rv['building']['id']
        self.write_building_status( rv )
        self.view();

    @LacunaObject.set_empire_status
    @set_building_status
    @call_building_meth
    def view( self, **kwargs ):
        pass

    @LacunaObject.set_empire_status
    @call_building_meth
    def demolish( self, **kwargs ):
        ### Since the building no longer exists, make sure that the object is 
        ### incapable of calling any further Building methods.
        del( self.body_id )
        del( self.building_id )

    @LacunaObject.set_empire_status
    @set_building_status
    @call_building_meth
    def do_upgrade( self, **kwargs ):
        """ Adds the current building to the build queue. """
        pass

    @LacunaObject.set_empire_status
    @set_building_status
    @call_building_meth
    def do_downgrade( self, **kwargs ):
        pass

    @LacunaObject.set_empire_status
    @call_building_meth
    def get_stats_for_level( self, level:int, **kwargs ):
        """ Returns what the stats for this building would be at the requested level.  The
        hypothetical stats are returned in rv['building'].
        """
        ### Purposely not decorating with set_building_status, since it's 
        ### reading out of rv['building'], and in this case, the information 
        ### in there pertains to the hypothetical requested level, not the 
        ### building's actual stats.
        pass

    @LacunaObject.set_empire_status
    @set_building_status
    @call_building_meth
    def repair( self, **kwargs ):
        """ Repairs a building, provided you have enough resources onsite.
        See the repair_costs building attribute (it's a dict) before calling
        repair to determine how much res the repair will take.
        """
        pass

class SingleStorage(Building):
    """ Base class for the storage buildings that store a singular resource 
    type, eg water or energy.
    """

    @LacunaObject.set_empire_status
    @Building.set_building_status
    @Building.call_building_meth
    def dump( self, amount:int = 0, **kwargs ):
        """ Converts the stored resource into waste """
        pass

class MultiStorage(Building):
    """ Base class for the storage buildings that store a variegated resource 
    type, eg food or ore.
    """

    @LacunaObject.set_empire_status
    @Building.set_building_status
    @Building.call_building_meth
    def dump( self, res_type:str = '', amount:int = 0, **kwargs ):
        """ Converts the stored resource into waste """
        pass
