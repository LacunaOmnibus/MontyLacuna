
import os, re, sys
bindir = os.path.abspath(os.path.dirname(sys.argv[0]))
libdir = bindir + "/../../lib"
sys.path.append(libdir)

import lacuna as lac

glc = lac.clients.Member(
    config_file = bindir + "/../../etc/lacuna.cfg",
    config_section = 'sitter',
)

my_planet = glc.get_body_byname( 'Earth' )
saw = my_planet.get_buildings_bytype( 'saw', 1, 1, 100 )[0]

###
### The saw is an example of a boring building - it doesn't have any methods 
### other that what are provided by its parents.
###

print( saw.name )
print( saw.id )
print( saw.image )

