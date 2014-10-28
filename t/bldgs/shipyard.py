
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
sy          = my_planet.get_building_coords( 3, -4 )


### View prisoners
###
pris = sy.view_prisoners()
for i in pris:
    print( "Prisoner named {} has an ID of {}.".format(pris.name, pris.id) )




