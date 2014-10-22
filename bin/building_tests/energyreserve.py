
import os, sys
bindir = os.path.abspath(os.path.dirname(__file__))
libdir = bindir + "/../../lib"
sys.path.append(libdir)

import lacuna as lac

glc = lac.clients.Member(
    config_file = bindir + "/../../etc/lacuna.cfg",
    config_section = 'my_sitter',
)
my_planet = glc.get_body_byname( 'bmots rof 2.1' )
nrg = my_planet.get_building_coords( -2, 4 )

### Dump energy to waste
###
one_bill = 1000 * 1000 * 1000
rva = nrg.dump( one_bill )
glc.pp.pprint( rva )

