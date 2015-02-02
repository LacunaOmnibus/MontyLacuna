
import os, re, sys
bindir = os.path.abspath(os.path.dirname(sys.argv[0]))
libdir = bindir + "/../../lib"
sys.path.append(libdir)

import lacuna as lac

glc = lac.clients.Member(
    config_file = bindir + "/../../etc/lacuna.cfg",
    config_section = 'sitter',
)

my_station = glc.get_body_byname( 'Some Station' )
art = my_station.get_buildings_bytype( 'artmuseum' )[0]

###
### The artmuseum is an example of a boring building even though it doesn't 
### live in the boring/ directory - it's an SS module, but still doesn't have 
### any methods other that what are provided by its parents.
###

print( art.name )
print( art.id )
print( art.image )

