
import os
import sys
import pprint, re

bindir = os.path.abspath(os.path.dirname(__file__))
libdir = bindir + "/../lib"
sys.path.append(libdir)

import lacuna as lac
pp = pprint.PrettyPrinter( indent = 4 )

glc = lac.users.Member(
    host = 'us1.lacunaexpanse.com',
    username='',
    password='',
)

### Get info on the alliance of the client's empire.  If the client's empire 
### is not in an alliance (tmt_testing is not), this will raise a GDIError.
my_all = glc.get_my_alliance();
print( my_all.name )
pp.pprint( my_all.members )


### get_alliance() returns a vanilla Alliance object.  This gives you access 
### to the documented Alliance methods, but the Alliance object itself DOES 
### NOT ACTUALLY REPRESENT AN ALLIANCE.
all = glc.get_alliance();

#pp.pprint( all.view_profile(26)['profile'] )    # Culture 
#pp.pprint( all.find("S.M.A.") )

