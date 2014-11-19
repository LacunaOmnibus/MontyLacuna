
"""

    Building is a base class representing generic buildings. A “generic 
    building” is usually one that’s handed back to you from the server as a 
    dict, often in a list of dicts, from such things as checking on the 
    Development Ministry’s build queue via its view() method.

    A Building object will probably, but not necessarily, have a building ID, 
    and may or may not belong to the current empire.

    MyBuilding represents a building owned by your empire, and most building 
    objects you encounter will inherit from MyBuilding.

    MontyLacuna attempts to provide method calls that mirror all of the method 
    calls documented by the TLE API.  However, MyBuilding had to violate that 
    for two methods:

        - ``do_upgrade()``
        - ``do_downgrade()``

        The published (server) method names for these are ``upgrade()`` and 
        ``downgrade()``.  However, we've got status attributes by those names, 
        and attributes overwrite methods of the same name.
        So these have been renamed, adding the ``do_`` prefix to avoid attribute 
        name collisions.


"""

import functools, re
from lacuna.bc import LacunaObject
from lacuna.exceptions import \
    CaptchaResponseError, \
    ServerError

class Building():
    def __init__( self, mydict:dict ):
        for k, v in mydict.items():
            setattr(self, k, v)

class InBuildQueue(Building):
    """
    Attributes::

        id                  "building-id-goes-here",
        name                "Planetary Commmand",
        to_level            8,
        seconds_remaining   537,
        x                   0,
        y                   0,
        subsidy_cost        3 # the essentia cost to subsidize just this building
    """

class MyBuilding(LacunaObject):
    """ 
    Attributes::

        id              Integer ID of the building itself
        body_id         Integer ID of the body this building is sitting on,
        name            "Apple Orchard",
        x               1,
        y               -1,
        url             "/apple",
        level           3,
        image           "apples3",
        efficiency      95,
        pending_build   {
                            # only included when building is building/upgrading
                            "seconds_remaining" : 430,
                            "start" : "01 31 2010 13:09:05 +0600",
                            "end" : "01 31 2010 18:09:05 +0600"
                        },
        work            {
                            # only included when building is working (Parks, Waste Recycling, etc)
                            "seconds_remaining" : 49,
                            "start" : "01 31 2010 13:09:05 +0600",
                            "end" : "01 31 2010 18:09:05 +0600"
                        }
    """

    def __init__( self, client, body_id:int, id:int = 0 ):
        ### Inheritance starts with LacunaObject, so super()__init__() calls 
        ### LacunaObject's __init__().
        super().__init__( client )
        self.body_id = body_id
        if id:
            self.id = id
            rv = self.client.send( self.path, 'view', (self.client.session_id, id) )
            self.write_building_status( rv )

    def call_building_meth(func):
        """ Decorator.
        Calls a server method that requires a id, but no body_id.
        This is the decorator that most MyBuilding methods will use.
        Methods using this decorator get the original server result handed 
        back to them in kwargs['rslt'].
        """
        @functools.wraps(func)
        def inner(self, *args, **kwargs):
            method_to_call = re.sub('^do_', '', func.__name__)
            myargs = (self.client.session_id, self.id) + args
            rslt = self.client.send( self.path, method_to_call, myargs )
            kwargs['rslt'] = rslt
            func( self, *args, **kwargs )
            return rslt
        return inner

    def call_returning_meth(func):
        """ Decorator.
        Calls a server method that requires a id, but no body_id.
        Rather than simply passing back the data returned from the TLE server, 
        returns the value from the originally-called method.

        Updates the empire status based on the TLE-returned data, as well as 
        the building status if it was included.
        """
        @functools.wraps(func)
        def inner(self, *args, **kwargs):
            method_to_call = re.sub('^do_', '', func.__name__)
            myargs = (self.client.session_id, self.id) + args
            rslt = self.client.send( self.path, method_to_call, myargs )
            status_dict = LacunaObject.get_status_dict(self, rslt)
            LacunaObject.write_empire_status(self, status_dict)
            self.write_building_status(rslt)
            kwargs['rslt'] = rslt
            myrslt = func( self, *args, **kwargs )
            return myrslt
        return inner

    def call_naked_returning_meth(func):
        """ Decorator.
        Calls a server method that does not require id or body_id.
        Rather than simply passing back the data returned from the TLE server, 
        returns the value from the originally-called method.

        Updates the empire status based on the TLE-returned data, so if you're 
        using this, there's no need to decorate with 
        @LacunaObject.set_empire_status (and doing so will fail).
        """
        @functools.wraps(func)
        def inner(self, *args, **kwargs):
            method_to_call = re.sub('^do_', '', func.__name__)
            myargs = (self.client.session_id,) + args
            rslt = self.client.send( self.path, method_to_call, myargs )
            status_dict = LacunaObject.get_status_dict(self, rslt)
            LacunaObject.write_empire_status(self, status_dict)
            kwargs['rslt'] = rslt
            myrslt = func( self, *args, **kwargs )
            return myrslt
        return inner

    def call_named_meth(func):
        """ Decorator.  
        Calls a server method that requires a id, but no body_id.
        Expects named arguments.  This is the 'new' way of doing it, but there are
        fairly few methods that work this way.  See generate_singularity()
        """
        @functools.wraps(func)
        def inner( self, mydict:dict ):
            mydict['session_id'] = self.client.session_id
            mydict['id'] = self.id
            rslt = self.client.send( self.path, func.__name__, (mydict,) )
            func( self, mydict )
            return rslt
        return inner

    def call_named_returning_meth(func, *args, **kwargs):
        """ Decorator.  
        Calls a server method that requires a session_id, but not a body_id.

        Expects named arguments, and returns the value from the locally-called 
        method rather than the dict returned from the TLE server.

        Updates the empire status based on the TLE-returned data, so if you're 
        using this, there's no need to decorate with 
        @LacunaObject.set_empire_status (and doing so will fail).
        """
        @functools.wraps(func)
        def inner( self, mydict:dict ):
            mydict['session_id'] = self.client.session_id
            mydict['building_id'] = self.id
            rslt = self.client.send( self.path, func.__name__, (mydict,) )
            LacunaObject.write_empire_status(self, rslt)
            kwargs['rslt'] = rslt
            myrslt = func( self, mydict, *args, **kwargs )
            return myrslt
        return inner

    def call_naked_meth(func):
        """ Decorator.
        Some building methods require neither a body_id nor a id (see 
        spaceport.py for examples).
        Methods using this decorator get the original server result handed 
        back to them in kwargs['rslt'].
        """
        @functools.wraps(func)
        def inner(self, *args):
            myargs = (self.client.session_id,) + args
            rslt = self.client.send( self.path, func.__name__, myargs )
            server_result = {'rslt': rslt}
            func( self, *args, **server_result )
            return rslt
        return inner

    def require_existing(func):
        """ Decorator.
        Many building methods only make sense to be called on a building that 
        actually already exists.  Add this decorator to those methods.
        """
        @functools.wraps(func)
        def inner(self, *args):
            if not self.id:
                raise AttributeError( "{} requires an already-existing building.".format(func.__name__) )
            func(self, args)
            return rslt
        return inner

    def set_building_status( func ):
        """ Decorator.
        Much like LacunaObject.set_empire_status.  A few of the Building server 
        methods return both empire status and building status.  So we'll still 
        decorate with LacunaObject.set_empire_status to get the empire status, 
        but we'll also decorate with this to set the body status.
        """
        @functools.wraps(func)
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
        ### build() is unique, as it requires a body_id but no id, since the 
        ### building doesn't exist yet.  No decorators here; the call to 
        ### view() after the building is placed will handle that.
        rv = self.client.send( self.path, 'build', (self.client.session_id, self.body_id, x, y) )
        rv['building']['id'] = rv['building']['id']
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
        ### incapable of calling any further MyBuilding methods.
        del( self.body_id )
        del( self.id )

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

class SingleStorage(MyBuilding):
    """ Base class for the storage buildings that store a singular resource 
    type, eg water or energy.
    """

    @LacunaObject.set_empire_status
    @MyBuilding.set_building_status
    @MyBuilding.call_building_meth
    def dump( self, amount:int = 0, **kwargs ):
        """ Converts the stored resource into waste """
        pass

class MultiStorage(MyBuilding):
    """ Base class for the storage buildings that store a variegated resource 
    type, eg food or ore.
    """

    @LacunaObject.set_empire_status
    @MyBuilding.set_building_status
    @MyBuilding.call_building_meth
    def dump( self, res_type:str = '', amount:int = 0, **kwargs ):
        """ Converts the stored resource into waste """
        pass
