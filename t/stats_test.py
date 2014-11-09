
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
###
guest_stats = guest.get_stats()
guest_cred = guest_stats.credits()
print( "TLE Play Testers:" )
for i in guest_cred['Play Testers']:
    print( "\t", i )




### Look at alliance stats by page
###
#stats = glc.get_stats()
#ranks, num, page = stats.alliance_rank()
#print( "There are", num, "total alliances." )
#print( "Names of alliances on page number", page, ":" )
#for i in ranks:
#    print( "\t", i.alliance_name )


### Look at alliance stats for a specific alliance
###
#stats = glc.get_stats()
#ranks = stats.find_alliance_rank('influence', 'S.M.A')
#for i in ranks:
#    print( "{} appears on page {}.".format(i.alliance_name, i.page_number) )


### CHECK this is where I got tired of doing the same thing over and over and 
### stopped testing.  I'm a bad person.

