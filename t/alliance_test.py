
import os
import sys
import pprint, re

bindir = os.path.abspath(os.path.dirname(__file__))
libdir = bindir + "/../lib"
sys.path.append(libdir)

import lacuna as lac
pp = pprint.PrettyPrinter( indent = 4 )

glc = lac.clients.Member(
    config_file = bindir + "/../etc/lacuna.cfg",
    config_section = 'my_sitter',
)

### Get info on the alliance of the client's empire.  If the client's empire 
### is not in an alliance, this will raise a GDIError.
###
my_all = glc.get_my_alliance();
print( "My alliance is named '{}'; here are some of the members:".format(my_all.name) )
for i in my_all.members[0:10]:
    print( "\t", i.name )


### get_alliance() returns a vanilla Alliance object.  This gives you access 
### to the documented Alliance methods, but the Alliance object itself DOES 
### NOT ACTUALLY REPRESENT AN ALLIANCE.
###
all = glc.get_alliance();

#pp.pprint( all.view_profile(26)['profile'] )    # Culture 
#pp.pprint( all.find("S.M.A.") )

