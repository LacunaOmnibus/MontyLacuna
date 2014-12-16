
import functools, re
import lacuna.bc
from lacuna.exceptions import \
    CaptchaResponseError, \
    ServerError

class Building(lacuna.bc.SubClass):
    """ Base class representing generic buildings. A “generic building” is 
    usually one that’s handed back to you from the server as a dict, often in 
    a list of dicts, from such things as checking on the Development 
    Ministry’s build queue via its view() method.

    A :class:`lacuna.building.Building` object will probably, but not 
    necessarily, have a building ID, and may or may not belong to the current 
    empire.

    Most buildings you deal with will be :class:`lacuna.building.MyBuilding` 
    objects, not :class:`lacuna.building.Building` objects.
    """

class InBuildQueue(Building):
    """ A building in the Development Ministry's build queue.

    Attributes::

        id                  "building-id-goes-here",
        name                "Planetary Commmand",
        to_level            8,
        seconds_remaining   537,
        x                   0,
        y                   0,
        subsidy_cost        3 # the essentia cost to subsidize just this building
    """

class MyBuilding(lacuna.bc.LacunaObject):
    """ Represents a building owned by your empire.  Most building objects 
    you encounter will inherit from MyBuilding.

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
        pending_build   lacuna.building.Working object
        work            lacuna.building.Working object

    - :class:`lacuna.building.Working`

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

    def __init__( self, client, body_id:int, id:int = 0 ):
        super().__init__( client )
        self.body_id = body_id
        if id:
            self.id = id
            rv = self.client.send( self.path, 'view', (self.client.session_id, id) )
            self._write_building_status( rv )


    def call_building_meth(func):
        """ Decorator.
        Calls a server method that requires a building id, but no body_id.
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
        Calls a server method that requires a building id, but no body_id.
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
            status_dict = lacuna.bc.LacunaObject.get_status_dict(self, rslt)
            lacuna.bc.LacunaObject.write_empire_status(self, status_dict)
            self._write_building_status(rslt)
            kwargs['rslt'] = rslt
            myrslt = func( self, *args, **kwargs )
            return myrslt
        return inner


    def call_naked_returning_meth(func):
        """ Decorator.
        Calls a server method that does not require building id or body_id.
        Rather than simply passing back the data returned from the TLE server, 
        returns the value from the originally-called method.

        Updates the empire status based on the TLE-returned data, so if you're 
        using this, there's no need to decorate with 
        @lacuna.bc.LacunaObject.set_empire_status (and doing so will fail).
        """
        @functools.wraps(func)
        def inner(self, *args, **kwargs):
            method_to_call = re.sub('^do_', '', func.__name__)
            myargs = (self.client.session_id,) + args
            rslt = self.client.send( self.path, method_to_call, myargs )
            status_dict = lacuna.bc.LacunaObject.get_status_dict(self, rslt)
            lacuna.bc.LacunaObject.write_empire_status(self, status_dict)
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
        @lacuna.bc.LacunaObject.set_empire_status (and doing so will fail).
        """
        @functools.wraps(func)
        def inner( self, mydict:dict ):
            mydict['session_id'] = self.client.session_id
            mydict['building_id'] = self.id
            rslt = self.client.send( self.path, func.__name__, (mydict,) )
            lacuna.bc.LacunaObject.write_empire_status(self, rslt)
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
        Much like lacuna.bc.LacunaObject.set_empire_status.  A few of the Building server 
        methods return both empire status and building status.  So we'll still 
        decorate with lacuna.bc.LacunaObject.set_empire_status to get the empire status, 
        but we'll also decorate with this to set the body status.
        """
        @functools.wraps(func)
        def inner(*args, **kwargs):
            rv = func( *args, **kwargs )
            self = args[0]
            self._write_building_status( rv )
            return rv
        return inner


    def _write_building_status( self, rv:dict ):
        mydict = {}
        if 'building' in rv:
            mydict = rv['building']
            del( rv['building'] )

        if 'pending_build' in mydict and type(mydict['pending_build']) is dict:
            self.pending_build = Working(self.client, mydict['pending_build'])
            del mydict['pending_build']

        if 'work' in mydict and type(mydict['work']) is dict:
            self.work = Working(self.client, mydict['work'])
            del mydict['work']

        for n, v in mydict.items():
            setattr( self, n, self.get_type(v) )


    def build( self, x:int, y:int, **kwargs ):
        """ Actually places a building on the requested coords, assuming the 
        building is buildable, the coords are empty, and a plot is available.

        After calling ``build()``, your "new building" object will be be an 
        "existing building" object, capable of calling the rest of the building 
        methods.
        """
        ### build() is unique, as it requires a body_id but no building_id, 
        ### since the building doesn't exist yet.  No decorators here; the 
        ### call to view() after the building is placed will handle that.
        rv = self.client.send( self.path, 'build', (self.client.session_id, self.body_id, x, y) )
        self._write_building_status( rv )
        self.view()


    @lacuna.bc.LacunaObject.set_empire_status
    @set_building_status
    @call_building_meth
    def view( self, **kwargs ):
        pass


    @lacuna.bc.LacunaObject.set_empire_status
    @call_building_meth
    def demolish( self, **kwargs ):
        ### Since the building no longer exists, make sure that the object is 
        ### incapable of calling any further MyBuilding methods.
        del( self.body_id )
        del( self.id )


    @lacuna.bc.LacunaObject.set_empire_status
    @set_building_status
    @call_building_meth
    def do_upgrade( self, **kwargs ):
        """ Adds the current building to the build queue. """
        pass


    @lacuna.bc.LacunaObject.set_empire_status
    @set_building_status
    @call_building_meth
    def do_downgrade( self, **kwargs ):
        pass


    @lacuna.bc.LacunaObject.set_empire_status
    @call_building_meth
    def get_stats_for_level( self, level:int, **kwargs ):
        """ Get what the stats for this building would be at the requested 
        level.
        
        Returns a dict including the key ``building``, which contains the
        hypothetical stats.
        """
        ### Purposely not decorating with set_building_status, since it's 
        ### reading out of rv['building'], and in this case, the information 
        ### in there pertains to the hypothetical requested level, not the 
        ### building's actual stats.
        pass


    @lacuna.bc.LacunaObject.set_empire_status
    @set_building_status
    @call_building_meth
    def repair( self, **kwargs ):
        """ Repairs a building, provided you have enough resources onsite.
        See the repair_costs building attribute before calling
        ``repair()`` to determine how much res the repair will take.
        """
        pass


class SingleStorage(MyBuilding):
    """ Base class for the storage buildings that store a singular resource 
    type, ie water and energy.
    """

    @lacuna.bc.LacunaObject.set_empire_status
    @MyBuilding.set_building_status
    @MyBuilding.call_building_meth
    def dump( self, amount:int = 0, **kwargs ):
        """ Converts the stored resource into waste 

        Arguments:
            - amount -- Required integer.  The amount of res to dump.
        """
        pass


class MultiStorage(MyBuilding):
    """ Base class for the storage buildings that store a variegated resource 
    type, ie food and ore.
    """

    @lacuna.bc.LacunaObject.set_empire_status
    @MyBuilding.set_building_status
    @MyBuilding.call_building_meth
    def dump( self, res_type:str, amount:int = 0, **kwargs ):
        """ Converts the stored resource into waste.

        Arguments:
            - res_type -- Required string.  The name of the specific type of res
              to dump ('anthracite', 'bauxite', 'algae', 'apple', etc )
            - amount -- Required integer.  The amount of res to dump.
        """
        pass


class Working(lacuna.bc.SubClass):
    """ The work being done, actually or potentially, by a building.

    Attributes::

        seconds     430,
        seconds_el  lacuna.bc.ElaspsedTime object representing the value in 
                    seconds.
        start       "01 31 2010 13:09:05 +0600"
        start_dt    datetime.datetime object representing the value in start.
        end         "01 31 2010 18:09:05 +0600"
        end_dt      datetime.datetime object representing the value in end.

    - :class:`lacuna.bc.ElapsedTime`
    - `datetime.datetime <https://docs.python.org/3.4/library/datetime.html>`_

    """
    def __init__(self, client, mydict:dict):
        if type(mydict['seconds_remaining']) is not int or mydict['seconds_remaining'] <= 0:
            ### This sometimes comes back as a negative, which we can't send 
            ### to sec2time.  If it's anything other than an int >= 0, change 
            ### it to a 0.
            mydict['seconds_remaining'] = 0

        self.seconds_el = self.sec2time( mydict['seconds_remaining'] )
        self.start_dt   = self.tle2time( mydict['start'] )
        self.end_dt     = self.tle2time( mydict['end'] )

        ### 'seconds_remaining' is too damn wordy, just change it to 
        ### 'seconds'.  But don't delete 'seconds_remaining' -- leave that in 
        ### case our user is following the TLE docu instead of the MontyLacuna 
        ### docu.
        mydict['seconds'] = mydict['seconds_remaining']

        super().__init__(client, mydict)

