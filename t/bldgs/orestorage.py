
import os, sys
bindir = os.path.abspath(os.path.dirname(sys.argv[0]))
libdir = bindir + "/../../lib"
sys.path.append(libdir)

import lacuna as lac

glc = lac.clients.Member(
    config_file = bindir + "/../../etc/lacuna.cfg",
    #config_section = 'my_sitter',
    config_section = 'play_test',
)
my_planet = glc.get_body_byname( 'bmots rof 2.1' )
ore = my_planet.get_building_coords( -4, 4 )

### Dump food to waste
### CAREFUL WITH THIS - it's actually dumping some of your energy.
### Depending on your storage building's level, you may want to dump less of 
### the resource.
res_type = 'rutile'
amount = 1000 * 1000 * 1000
rva = ore.dump( res_type, amount )
print( "Done;", amount, "of", res_type, "has been dumped.")

