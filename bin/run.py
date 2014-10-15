
import os, pprint, sys

bindir = os.path.abspath(os.path.dirname(__file__))
libdir = bindir + "/../lib"
sys.path.append(libdir)
import lacuna as lac

pp = pprint.PrettyPrinter( indent = 4 )

guest = lac.users.Client()

glc = lac.users.Member(
    username='',
    password='',
)

### some methods can be called directly from the client
print( glc.is_name_available('tmtowtdi') )

### a Member object automatically has an empire object attached to it.
print( glc.empire.rpc_count )

### Other objects can be created from the Member object via the appropriate 
### get_*() method.
mymap = glc.get_map();
pp.pprint( mymap.get_stars(285, -1115, 290, -1120) )    # rof 2.1


