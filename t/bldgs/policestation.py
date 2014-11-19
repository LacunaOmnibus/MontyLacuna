
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
ships, count = cops.view_foreign_ships()
print( "There are", count, "ships incoming." )
for i in ships:
    print( "{} is coming from {}'s planet {}."
        .format(i.type_human, i.origin['empire']['name'], i.origin['name'])
    )
print( "-------------------------------" )

### See orbiting ships
### 
ships, count = cops.view_ships_orbiting()
print( "There are", count, "ships orbiting." )
for i in ships:
    print( "{} from {} got here on {}."
        .format(i.type_human, i.origin['empire']['name'], i.date_arrived)
    )
print( "-------------------------------" )
