
import os, sys
bindir = os.path.abspath(os.path.dirname(__file__))
libdir = bindir + "/../../lib"
sys.path.append(libdir)

import lacuna as lac

glc = lac.clients.Member(
    config_file = bindir + "/../../etc/lacuna.cfg",
    config_section = 'my_real',
)

my_planet = glc.get_body_byname( 'ZASS Zorro' )
cops = my_planet.get_building_coords( 5, 5 )


### See incoming ships
###
ships = cops.view_foriegn_ships()
for i in ships:
    print( "{} is coming from {}'s planet {}.'"
        .format(i.type_human, i.origin['empire']['name'], i.origin['name'])
    )

