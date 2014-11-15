
import datetime, os, sys

bindir = os.path.abspath(os.path.dirname(__file__))
libdir = bindir + "/../lib"
sys.path.append(libdir)

import lacuna as lac


glc = lac.clients.Member(
    config_file = bindir + "/../etc/lacuna.cfg",
    config_section = 'play_test',
)


### Get one of your planets
###

pname = 'bmots01'
#pname = 'bmots support 01'


### I'm starting to lean in this direction, but I'm not sure yet, and it's 
### getting late so my judgement might be off.  Think about this some more.
###
### But the idea is to force client.send() to cache its result while it's 
### still JSON.  We can't cache things like the result of get_body_byname(), 
### it's too object-y at that point, but we could cache the JSON string that 
### turns into the body object.
###
my_key_name = pname 
glc.cacheon( 'my_cache_name', my_key_name )     # doesn't exist
my_planet = glc.get_body_byname( pname )
glc.cacheoff(  )                                # doesn't exist

