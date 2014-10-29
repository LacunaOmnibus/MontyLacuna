
import os, re, sys
bindir = os.path.abspath(os.path.dirname(__file__))
libdir = bindir + "/../../lib"
sys.path.append(libdir)

import lacuna as lac

glc = lac.clients.Member(
    config_file = bindir + "/../../etc/lacuna.cfg",
    #config_section = 'my_sitter',
    config_section = 'play_test',
)
my_planet   = glc.get_body_byname( 'bmots rof 2.1' )
temp        = my_planet.get_building_coords( -1, -4 )


### View list of planets
###
#rv = temp.list_planets()
#glc.pp.pprint( rv['planets'] )


### View map of a specific planet
### 
#rv = temp.list_planets()
#pid = rv['planets'][0]['id']
#rv = temp.view_planet(pid)
#glc.pp.pprint( rv['map'] )

