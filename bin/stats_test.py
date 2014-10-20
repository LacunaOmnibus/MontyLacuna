
import os, sys
import pprint, re

bindir = os.path.abspath(os.path.dirname(__file__))
libdir = bindir + "/../lib"
sys.path.append(libdir)

import lacuna as lac
pp = pprint.PrettyPrinter( indent = 4 )



guest = lac.clients.Guest(
    config_file = bindir + "/../etc/lacuna.cfg",
    config_section = 'my_guest',
)
glc = lac.clients.Member(
    config_file = bindir + "/../etc/lacuna.cfg",
    config_section = 'my_sitter',
)

### credits() works fine from a guest account.
#guest_stats = guest.get_stats()
#guest_cred = guest_stats.credits()
#pp.pprint( guest_cred )
#quit()


stats = glc.get_stats()


ranks = stats.alliance_rank()
pp.pprint( ranks )

#ranks = stats.find_alliance_rank('influence', 'S.M.A')
#pp.pprint( ranks )


### CHECK this is where I got tired of doing the same thing over and over and 
### stopped testing.  I'm a bad person.

