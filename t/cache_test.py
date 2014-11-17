
import datetime, os, sys

bindir = os.path.abspath(os.path.dirname(__file__))
libdir = bindir + "/../lib"
sys.path.append(libdir)

import lacuna as lac


glc = lac.clients.Member(
    config_file = bindir + "/../etc/lacuna.cfg",
    config_section = 'play_test',
)


### 
### How about leaving out the my_key_name?
###
### The key then gets created by client.send() as a join of send()'s args -- 
### every send() call gets cached as long as cacheon is turned on.  The user 
### just specifies the cache name.  He can later clear the entire cache by 
### name.
###
### I think that's the way to go.
###
### Forcing the user to cacheon and then immediately cacheoff for every call 
### is going to get tedious quick.
###
glc.cacheon( 'my_cache_name', 'my_key_name', 3600 )     # doesn't exist

my_planet = glc.get_body_byname( pname )
glc.cacheoff(  )                                # doesn't exist

    ...later, optionally...
glc.clear_cache( 'my_cache_name', my_key_name )

