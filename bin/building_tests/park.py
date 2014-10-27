
import os, re, sys
bindir = os.path.abspath(os.path.dirname(__file__))
libdir = bindir + "/../../lib"
sys.path.append(libdir)

import lacuna as lac

glc = lac.clients.Member(
    config_file = bindir + "/../../etc/lacuna.cfg",
    #config_section = 'my_sitter',
    config_section = 'play_test',
)
my_planet   = glc.get_body_byname( 'bmots rof 2.1' )
park        = my_planet.get_building_coords( 2, -3 )


### See if there's a party going on right now.  If so, show how much longer 
### it'll continue.
###
#view = park.view( )
#glc.pp.pprint( view['party'] )


### Throw a party
###
#park.throw_a_party();
#view = park.view( )
#glc.pp.pprint( view['party'] )


### Subsidize the party for 2E (gotta pay to clear out all those fratboys!)
### 
#park.subsidize_party()

