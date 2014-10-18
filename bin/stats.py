
import os, sys
import pprint, re

bindir = os.path.abspath(os.path.dirname(__file__))
libdir = bindir + "/../lib"
sys.path.append(libdir)

import lacuna as lac
pp = pprint.PrettyPrinter( indent = 4 )

guest = lac.users.Client(
    host = 'us1.lacunaexpanse.com',
)
glc = lac.users.Member(
    host = 'us1.lacunaexpanse.com',
    username='',
    password='',
)

stats = glc.get_stats()

### credits() works fine from a guest account.
#guest_stats = guest.get_stats()
#guest_cred = guest_stats.credits()
#pp.pprint( guest_cred )


#ranks = stats.alliance_rank()
#pp.pprint( ranks )

#ranks = stats.find_alliance_rank('influence', 'S.M.A')
#del( ranks['status'] )
#pp.pprint( ranks )


### CHECK this is where I got tired of doing the same thing over and over and 
### stopped testing.  I'm a bad person.

