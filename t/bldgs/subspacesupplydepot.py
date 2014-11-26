
import os, re, sys
bindir = os.path.abspath(os.path.dirname(sys.argv[0]))
libdir = bindir + "/../../lib"
sys.path.append(libdir)

import lacuna as lac

glc = lac.clients.Member(
    config_file = bindir + "/../../etc/lacuna.cfg",
    #config_section = 'my_sitter',
    config_section = 'play_test_two',
)

my_planet   = glc.get_body_byname( 'Evolme' )
ssd         = my_planet.get_building_coords( 3, -2 )

### This is completely untested.  I haven't got an SSD lying around to play 
### with.
###
#ssd.transmit_water()



rv = ssd.complete_build_queue()
glc.pp.pprint( rv )

