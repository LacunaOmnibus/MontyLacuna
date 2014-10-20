
"""
    Building is a base class, extending LacunaObject.

    LacunaObject requires a path 'class' variable, but Building does not 
    provide it; any module extending Building must provide that path variable.

    Specific building class names must match the URL needed to access them (eg 
    the Space Port class must be named 'spaceport').  Having class names that 
    differ from the published URLs just creates one more thing to have to look 
    up somewhere.
    The names of the modules containing those building classes are hardcoded 
    in buildings/__init__.py, so those module names can be more flexible.  
    However, I see no need to complicate things by using different names for 
    the modules, either, so name them "<classname>.py" (eg "spaceport.py").

    There are two types of Building objects:
            - Potential buildings
            - Existing buildings
    A Potential building doesn't exist yet.  Its constuctor requires a body_id 
    but no building_id.  A Potential building can't do anything but call 
    build().  After calling build(), the Potential building becomes an 
    Existing building.
"""

import re
from lacuna.bc import LacunaObject

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
        """
        def inner(self, *args):
            method_to_call = re.sub('^do_', '', func.__name__)
            myargs = (self.client.session_id, self.building_id) + args
            rslt = self.client.send( self.path, method_to_call, myargs )
            func( self, *args )
            return rslt
        return inner

    def call_naked_meth(func):
        """Decorator.
        Some building methods require neither a body_id nor a building_id (see 
        spaceport.py for examples).
        """
        def inner(self, *args):
            myargs = (self.client.session_id,) + args
            rslt = self.client.send( self.path, func.__name__, myargs )
            func( self, *args )
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
        if 'building' in rv:
            mydict = rv['building']
            del( rv['building'] )
        for n, v in mydict.items():
            setattr( self, n, v )

    def build( self, x:int, y:int ):
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
    def view( self ):
        pass

    @LacunaObject.set_empire_status
    @call_building_meth
    def demolish( self ):
        ### Since the building no longer exists, make sure that the object is 
        ### incapable of calling any further Building methods.
        del( self.body_id )
        del( self.building_id )

    @LacunaObject.set_empire_status
    @set_building_status
    @call_building_meth
    def do_upgrade( self ):
        """ Adds the current building to the build queue.
        The published method name is "upgrade", not "do_upgrade".  But we've got an attribute
        (set from a status return) named "upgrade", and attributes overwrite methods of the
        same name.  So this has been renamed "do_upgrade".  The call_building_meth() decorator
        knows how to deal with methods that =~ /^do_/.
        """
        pass

    @LacunaObject.set_empire_status
    @set_building_status
    @call_building_meth
    def do_downgrade( self ):
        pass

    @LacunaObject.set_empire_status
    @call_building_meth
    def get_stats_for_level( self, level:int ):
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
    def repair( self ):
        """ Repairs a building, provided you have enough resources onsite.
        See the repair_costs building attribute (it's a dict) before calling
        repair to determine how much res the repair will take.
        """
        pass
