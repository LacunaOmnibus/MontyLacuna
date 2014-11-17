
import datetime, os, sys

bindir = os.path.abspath(os.path.dirname(__file__))
libdir = bindir + "/../lib"
sys.path.append(libdir)

import lacuna as lac

glc = lac.clients.Member(
    config_file = bindir + "/../etc/lacuna.cfg",
    config_section = 'play_test',
)


print( "START TIME", datetime.datetime.now() )
print( "----------------------" )

glc.cache_on( 'my_cache_name', 3600 )
my_planet_one = glc.get_body_byname("bmots01")
print( datetime.datetime.now() )
my_planet_one = glc.get_body_byname("bmots01")
print( datetime.datetime.now() )

glc.cache_clear()
print( "----------------------" )

my_planet_one = glc.get_body_byname("bmots01")
print( datetime.datetime.now() )
my_planet_one = glc.get_body_byname("bmots01")
print( datetime.datetime.now() )

