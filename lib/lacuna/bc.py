
"""Module for lacuna base classes."""

import pprint

class LacunaObject:

    pp = pprint.PrettyPrinter( indent = 4 )

    def __init__(self, client:object, *args, **kwargs):
        if not hasattr(self, 'path'):
            raise AttributeError("LacunaObject subclass "+ str(type(self)) +" did not define a 'path' class attribute.")
        self.client = client

    def set_empire_status( func ):
        """Decorator.
        
        Update the Empire object's attributes with fresh status data with 
        each decorated method call.

        The status block can show up in various places for different methods;
        it's just not consistent.  Some candidates:
            rv = {
                status: { here }

                status: {
                    empire: { or here }
                }

                empire: { or even here }
            }

        'essentia': 8462.5,
        'has_new_messages': '1769',
        'home_planet_id': '108756',
        'id': '23598',
        'is_isolationist': '0',
        'latest_message_id': '67512585',
        'name': 'tmtowtdi',
        'rpc_count': 485,
        'self_destruct_active': '0',
        'self_destruct_date': '14 07 2011 21:38:22 +0000',
        'status_message': 'Making Lacuna a better Expanse.',
        'tech_level': '30'
        'planets': { id: name },

        ### This does not get returned from the server this way, but it's 
        ### needed often enough that we'll set it here.
        'planet_names': { name: id },
        """
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
        for i in mydict:
            setattr( self.client.empire, i, mydict[i] )
        self.client.empire.planet_names = {name: id for id, name in self.client.empire.planets.items()}

    def call_guest_meth(func):
        """Decorator.  
        Makes an RPC not requiring that the client is logged in.
        The decorated method must be named identically to an existing TLE method.
        """
        def inner(self, *args):
            rslt = self.client.send( self.path, func.__name__, args )
            func( self, *args )
            return rslt
        return inner

    def call_member_meth(func):
        """ Decorator.  
        Makes an RPC that _does_ require that the client is logged in.
        The decorated method must be named identically to an existing TLE method.
        Expects positional arguments.  This is the 'old' way of doing things, but
        almost all of the TLE methods work this way.
        """
        def inner(self, *args, **kwargs):
            myargs = (self.client.session_id,) + args
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
        def inner(self, *args, **kwargs):
            myargs = (self.client.session_id,) + args
            rslt = self.client.send( self.path, func.__name__, myargs )
            status_dict = self.get_status_dict(rslt)
            self.write_empire_status(status_dict)
            kwargs['rslt'] = rslt
            myrslt = func( self, *args, **kwargs )
            return myrslt
        return inner

    def call_member_named_meth(func):
        """ Decorator.  
        Makes an RPC that _does_ require that the client is logged in.
        The decorated method must be named identically to an existing TLE method.
        Expects named arguments.  This is the 'new' way of doing it, but there are
        fairly few methods that work this way.  See map.get_star_map()
        """
        def inner( self, mydict:dict ):
            mydict['session_id'] = self.client.session_id
            rslt = self.client.send( self.path, func.__name__, (mydict,) )
            func( self, mydict )
            return rslt
        return inner

class SubClass():
    def __init__(self, client, mydict:dict):
        self.client = client
        for k, v in mydict.items():
            setattr(self, k, v)

