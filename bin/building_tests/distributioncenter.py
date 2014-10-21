
import os, sys
bindir = os.path.abspath(os.path.dirname(__file__))
libdir = bindir + "/../../lib"
sys.path.append(libdir)

import lacuna as lac

glc = lac.clients.Member(
    config_file = bindir + "/../../etc/lacuna.cfg",
    config_section = 'play_test',
)
my_planet = glc.get_body_byname( 'bmots rof 2.1' )
dist = my_planet.get_building_coords( -1, -3 )


### List resources onsite to see what can be reserved
###
#rva = dist.get_stored_resources( )
#glc.pp.pprint( rva['resources'] )


### Reserve specific resources
###
res = [
    { 
        'type': 'apple',
        'quantity': 10
    },
    { 
        'type': 'energy',
        'quantity': 11
    },
    { 
        'type': 'cheese',
        'quantity': 12
    },
]
#rvb = dist.reserve( res )
#glc.pp.pprint( rvb['reserve'] )


### Check to see what's currently in the reserve
###
#glc.pp.pprint( dist.view()['reserve'] )


### Release all reserved resources
###
#rvc = dist.release_reserve( )
#glc.pp.pprint( rvc )


