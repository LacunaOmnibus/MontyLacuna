
import os, sys
bindir = os.path.abspath(os.path.dirname(__file__))
libdir = bindir + "/../../lib"
sys.path.append(libdir)

import lacuna as lac

glc = lac.clients.Member(
    config_file = bindir + "/../../etc/lacuna.cfg",
    #config_section = 'my_sitter',
    config_section = 'play_test',
)
my_planet   = glc.get_body_byname( 'bmots rof 1.1' )
minmin      = my_planet.get_building_coords( -3, 3 )


### See what platforms you have out
###
#rva = minmin.view_platforms()
#glc.pp.pprint( rva['platforms'] )
#print( "I have {} of a maximum {} platforms out.".format(len(rva['platforms']), rva['max_platforms']) )


### See what ships are mining
###
rvb = minmin.view_ships()
glc.pp.pprint( rvb['ships'] )
