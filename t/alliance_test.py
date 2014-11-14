
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

ally = glc.get_alliance()

### Find an alliance by name
###
#allies = ally.find( 'S.M.A' )
#for i in allies:
#    print( "The alliance named {} has an ID of {}."
#        .format(i.name, i.id)
#    )


### Get info on the alliance your logged-in client is a member of.  If that 
### client is not in an alliance, this will raise a GDIError.
###
#my_all = glc.get_my_alliance();
#print( "My alliance is named '{}'; here are some of the members:".format(my_all.name) )
#for i in my_all.members[0:10]:
#    print( "\t", i.name )

