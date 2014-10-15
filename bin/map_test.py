
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


mymap = glc.get_map();
#pp.pprint( mymap.get_stars(285, -1115, 290, -1120) )


star_dict = {
    'left': 285,
    'right': 290,
    'top': -1115,
    'bottom': -1120
}
#pp.pprint( mymap.get_star_map(star_dict) )


### 
### Everything below works, just one at a time (since I intelligently used 
### 'rv' as the variable name in each one).
###
### 15320, used in several places below, is the ID of Oot Yaeplie Oad (star 
### for rof 2).
###

#rv = mymap.check_star_for_incoming_probe( 15320 )
#pp.pprint( rv )

#rv = mymap.get_star( 15320 )
#pp.pprint( rv )

#rv = mymap.get_star_by_name( 'Oot Yaeplie Oad' )
#pp.pprint( rv )

#rv = mymap.get_star_by_xy( 288, -1118 )
#pp.pprint( rv )

#rv = mymap.search_stars( "Oot Yaeplie" )
#pp.pprint( rv )

#zone_dict = { 'zone': '-1|0', }
#rv = mymap.probe_summary_fissures( zone_dict )
#pp.pprint( rv )












