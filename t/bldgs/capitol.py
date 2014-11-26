
import os, sys
bindir = os.path.abspath(os.path.dirname(sys.argv[0]))
libdir = bindir + "/../../lib"
sys.path.append(libdir)

import lacuna as lac

glc = lac.clients.Member(
    config_file = bindir + "/../../etc/lacuna.cfg",
    config_section = 'my_sitter',
)

my_planet = glc.get_body_byname( 'bmots rof 2.1' )
cap = my_planet.get_building_coords( 0, -3 )


### Get available actions
###
rva = cap.rename_empire( "tmtowtdi" )
glc.pp.pprint( rva )


