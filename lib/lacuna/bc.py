
"""Module for lacuna base classes."""

import datetime, functools, math, pprint, re

class SubClass():
    """ A generic base class for turning returned dicts into objects, and 
    for providing utility methods.

    Almost all MontyLacuna objects inherit from this class, so any methods of 
    this class can be called from (almost) any MontyLacuna object::

        >>> my_planet = glc.get_body_byname( 'Earth' )
        >>> print( my_planet.client)
        <lacuna.clients.Member object at 0x7fb19ed863c8>

        >>> arch = my_planet.get_buildings_bytype( 'archaeology', 0, 1 )[0]
        >>> el = arch.sec2time( 123456 )
        >>> print( el.days, el.hours, el.minutes, el.seconds )
        1 10 17 36

    ...etc.
    """

    def __init__(self, client, mydict:dict):
        """ Create a lacuna.bc.SubClass object.

        Args:
            client (lacuna.clients.Member): The client used for any connections
            mydict (dict): The keys will become attributes of the 
                SubClass object, and the values will become the values of those
                attributes.
        """
        self.client = client
        for k, v in mydict.items():
            setattr( self, k, self.get_type(v) )

    def get_type( self, cand ):
        """ Changes strings that look like numbers into numbers.

        Since all communications with the server is via JSON, which is a text 
        transport, all values that look like numbers are actually strings. 
        
        eg the '5' in 'ship_count = 5' is a string, not an int, so doing math on 
        it, or trying to format it as a number, is going to cause problems.

        This attempts to turn strings that should be either ints or floats into 
        ints or floats.  Any type other than an int or float gets returned 
        unmolested::

            cand = 1
            new = client.get_type( cand )
            print( type(new) )              # int

            cand = 1.7
            new = client.get_type( cand )
            print( type(new) )              # float

            cand = "one point seven"
            new = client.get_type( cand )
            print( type(new) )              # str

            cand = { 'number': 1.7 }
            new = client.get_type( cand )
            print( type(new) )              # dict

        """
        try:
            ### int() here just tells us if it's a number; it operates without 
            ### exception on both ints and floats (int(1.7) == 1).  The point 
            ### of this is to throw an exception if we've got a string or a 
            ### dict or whatever, but to pass through on any number.
            new = int(cand)
            if '.' in cand:
                new = float(cand)
        except:
            ### Not a number; leave it alone.
            new = cand
        return new


    def tle2time(self, tle_time:str):
        """ Converts a TLE datetime string into a datetime object.

        Args:
            tle_datetime (str): eg ``30 11 2014 21:40:31 +0000``.
                The "+0000" is meant to be the timezone, but in TLE 
                datetime strings this is always "+0000" (UTC), so 
                this method is ignoring it, and it could actually 
                be omitted from the passed-in string.

        Returns:
            datetime.datetime: A `datetime.datetime <https://docs.python.org/3.4/library/datetime.html>`_ object
        """
        ### No, I don't know why this is here rather than in utils.py.  This 
        ### is where I originally put it and it's being called from here.  
        ### When you get motivated, find the calls and fix them to use utils 
        ### and then remove this from here.
        m = re.match("^(\d\d) (\d\d) (\d{4}) (\d\d):(\d\d):(\d\d)", tle_time)
        if m:
            return datetime.datetime(
                int(m.group(3)),    # year
                int(m.group(2)),    # month
                int(m.group(1)),    # day
                int(m.group(4)),    # hour
                int(m.group(5)),    # minute
                int(m.group(6)),    # second
            )
        else:
            raise AttributeError( "{} isn't a TLE datetime string.".format(tle_time) )

    def sec2time(self, secs:int):
        """ Converts seconds into days, hours, minutes, and seconds.

        Args:
            seconds (int): seconds to convert
        Returns:
            lacuna.bc.ElapsedTime: Your passed-in seconds converted.
        """
        ### http://stackoverflow.com/questions/4048651/python-function-to-convert-seconds-into-minutes-hours-and-days
        ###
        secs = int(secs)        # Give the user a break if they sent a string.
        s = datetime.timedelta( seconds = secs )
        d = datetime.datetime(1, 1, 1) + s
        return ElapsedTime(d)


class LacunaObject(SubClass):
    """ Superclass from which almost all MontyLacuna objects inherit.
    """
    pp = pprint.PrettyPrinter( indent = 4 )

    def __init__(self, client:object, *args, **kwargs):
        if not hasattr(self, 'path'):
            raise AttributeError("LacunaObject subclass "+ str(type(self)) +" did not define a 'path' class attribute.")
        self.client = client

    def set_empire_status( func ):
        """Decorator.
        
        Update the Empire object's attributes with fresh status data with 
        each decorated method call.

        Object Attributes::

            essentia                8462.5,
            has_new_messages        '1769',
            home_planet_id          '108756',
            id                      '23598',
            is_isolationist         '0',
            latest_message_id       '67512585',
            name                    'tmtowtdi',
            rpc_count               485,
            self_destruct_active    '0',
            self_destruct_date      '14 07 2011 21:38:22 +0000',
            status_message          'Making Lacuna a better Expanse.',
            tech_level              '30'
            planets                 {   12345: "Mercury",
                                        12346: "Venus",
                                        etc     },
            planet_names            {   "Mercury": 12345,
                                        "Venus": 12346,
                                        etc     },

        The status block can show up in various places for different methods;
        it's just not consistent.  Some candidates::

            rv = {
                status: { here }
                status: {
                    empire: { or here }
                }
                empire: { or even here }
            }


        """
        @functools.wraps(func)
        def inner(*args, **kwargs):
            rv = func( *args, **kwargs )
            self = args[0]
            mydict = self.get_status_dict(rv)
            self.write_empire_status(mydict)
            return rv
        return inner

    def get_status_dict(self, server_response:dict):
        mydict = {}
        if 'empire' in server_response:
            mydict = server_response['empire']
        elif 'status' in server_response:
            if 'empire' in server_response['status']:
                mydict = server_response['status']['empire']
            else:
                mydict = server_response['status']
        return mydict

    def write_empire_status(self, mydict:dict):
        if 'rpc_count' in mydict and hasattr(self.client.empire, 'rpc_count'):
            if int(mydict['rpc_count']) <= int(self.client.empire.rpc_count):
                ### Our result came from the cache rather than a fresh request 
                ### to the server, so don't update anything.
                return
        for i in mydict:
            setattr( self.client.empire, i, self.get_type(mydict[i]) )
        self.client.empire.planet_names = {name: id for id, name in self.client.empire.planets.items()}
        self.client.empire.colony_names = {name: id for id, name in self.client.empire.colonies.items()}
        if hasattr(self.client.empire, 'stations'):
            self.client.empire.station_names = {name: id for id, name in self.client.empire.stations.items()}

    def call_guest_meth(func):
        """Decorator.  
        Makes an RPC not requiring that the client is logged in.
        The decorated method must be named identically to an existing TLE method.
        """
        @functools.wraps(func)
        def inner(self, *args, **kwargs):
            kwargs['rslt'] = self.client.send( self.path, func.__name__, args )
            myrslt = func( self, *args, **kwargs )
            return myrslt
        return inner

    def call_member_meth(func):
        """ Decorator.  
        Makes an RPC that _does_ require that the client is logged in.
        The decorated method must be named identically to an existing TLE method.
        Expects positional arguments.  This is the 'old' way of doing things, but
        almost all of the TLE methods work this way.
        """
        @functools.wraps(func)
        def inner(self, *args, **kwargs):
            ### Most of our callers will have self.client, except when self 
            ### is, itself, a client.
            session_id = ''
            if hasattr( self.client, 'session_id' ):
                session_id = self.client.session_id
            elif hasattr( self, 'session_id' ):
                session_id = self.session_id
            myargs = (session_id,) + args
            rslt = self.client.send( self.path, func.__name__, myargs )
            kwargs['rslt'] = rslt
            func( self, *args, **kwargs )
            return rslt
        return inner


    def call_returning_meth(func):
        """ Decorator.  
        Makes an RPC that _does_ require that the client is logged in.
        Most RPC calls simply return to the user the data returned from the TLE 
        servers (after a slight massage).  But some methods need to modify that 
        data themselves.

        Updates the empire status based on the TLE-returned data, so if you're 
        using this, there's no need to decorate with 
        @LacunaObject.set_empire_status (and doing so will fail).
        """
        @functools.wraps(func)
        def inner(self, *args, **kwargs):
            myargs = (self.client.session_id,) + args
            rslt = self.client.send( self.path, func.__name__, myargs )
            status_dict = self.get_status_dict(rslt)
            self.write_empire_status(status_dict)
            kwargs['rslt'] = rslt
            myrslt = func( self, *args, **kwargs )
            return myrslt
        return inner

    def call_named_returning_meth(func):
        """ Decorator.  
        Makes an RPC that _does_ require that the client is logged in.
        Most RPC calls simply return to the user the data returned from the TLE 
        servers (after a slight massage).  But some methods need to modify that 
        data themselves.

        Updates the empire status based on the TLE-returned data, so if you're 
        using this, there's no need to decorate with 
        @LacunaObject.set_empire_status (and doing so will fail).
        """
        @functools.wraps(func)
        def inner(self, mydict:dict, *args, **kwargs):
            mydict['session_id'] = self.client.session_id
            rslt = self.client.send( self.path, func.__name__, (mydict,) )
            status_dict = self.get_status_dict(rslt)
            self.write_empire_status(status_dict)
            kwargs['rslt'] = rslt
            myrslt = func( self, mydict, *args, **kwargs )
            return myrslt
        return inner

    def call_member_named_meth(func):
        """ Decorator.  
        Makes an RPC that _does_ require that the client is logged in.
        The decorated method must be named identically to an existing TLE method.
        Expects named arguments.  This is the 'new' way of doing it, but there are
        fairly few methods that work this way.  See map.get_star_map()
        """
        @functools.wraps(func)
        def inner( self, mydict:dict ):
            mydict['session_id'] = self.client.session_id
            rslt = self.client.send( self.path, func.__name__, (mydict,) )
            func( self, mydict )
            return rslt
        return inner

    def call_body_meth(func):
        """ Decorator.  
        Just like call_member_meth(), except that this version includes the 
        body_id in the args passed to the server.
        """
        @functools.wraps(func)
        def inner(self, *args, **kwargs):
            myargs = (self.client.session_id, self.body_id) + args
            rslt = self.client.send( self.path, func.__name__, myargs )
            status_dict = self.get_status_dict(rslt)
            self.write_empire_status(status_dict)
            kwargs['rslt'] = rslt
            func( self, *args, **kwargs )
            return rslt
        return inner

    def call_returning_body_meth(func):
        """ Decorator.  
        Just like call_returning_meth(), except that this version includes the 
        body_id in the args passed to the server.
        """
        @functools.wraps(func)
        def inner(self, *args, **kwargs):
            myargs = (self.client.session_id, self.body_id) + args
            rslt = self.client.send( self.path, func.__name__, myargs )
            status_dict = self.get_status_dict(rslt)
            self.write_empire_status(status_dict)
            kwargs['rslt'] = rslt
            myrslt = func( self, *args, **kwargs )
            return myrslt
        return inner

class ElapsedTime():
    """ Turns seconds into days, hours, minutes, and seconds.

    Some methods return how long something is going to take in terms of seconds 
    only.  Since it can be a little difficult to look at 190353 seconds and 
    know off the top of your head how long that really is, you can pass those 
    seconds to ElapsedTime.

    Object Attributes (all are integers)::

        days
        hours
        minutes
        seconds

    This is awfully close to a `datetime.datetime <https://docs.python.org/3.4/library/datetime.html>`_ object, except:
        - The attributes are plural: "days" instead of "day"
        - The number of days elapsed is correct as-is.  datetime.day would 
          actually be one too high, and the user would need to subtract 
          one, and he's going to forget to do that 90% of the time.

    *CAUTION* - :meth:`lacuna.bc.SubClass.sec2time` is slightly hokey - if the 
    number of seconds passed in is greater than the number of seconds in the 
    current month (2678400 for a 31-day month), then all returns will be reset::

        time = i.sec2time( 2678400 )
        print( "That's {} days, {} hours, {} minutes, and {} seconds."
            .format(time.days, time.hours, time.minutes, time.seconds)
        )
            "That's 0 days, 0 hours, 0 minutes, and 0 seconds."

    Since very few TLE-related activities will take more than a month, this 
    is usually not a problem.  But a ship sent at speed 1 from one corner of 
    the expanse to the other won't be able to make reasonable use of this 
    converter.
    """
    def __init__(self, d:datetime):
        self.days = d.day - 1
        self.hours = d.hour
        self.minutes = d.minute
        self.seconds = d.second

