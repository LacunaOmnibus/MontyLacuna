
import os, re, sys
bindir = os.path.abspath(os.path.dirname(sys.argv[0]))
libdir = bindir + "/../../lib"
sys.path.append(libdir)

import lacuna as lac

glc = lac.clients.Member(
    config_file = bindir + "/../../etc/lacuna.cfg",
    config_section = 'my_sitter',
    #config_section = 'play_test',
)
my_planet   = glc.get_body_byname( 'bmots rof 2.7' )
park        = my_planet.get_building_coords( -1, -5 )


### See if there's a party going on right now.  If so, show how much longer 
### it'll continue.
###
party = park.view( )
if party.can_throw:
    print( "I can throw a party." )
else:
    print( "A party is currently running for the next {} seconds.  It'll produce {} happy."
        .format(party.seconds_remaining, party.happiness)
    )


### Throw a party
###
#party = park.throw_a_party();
#print( "I just threw a party for the next {} seconds.  It'll produce {} happy."
#        .format(party.seconds_remaining, party.happiness)
#    )


### Subsidize the party for 2E (gotta pay to clear out all those fratboys!)
### 
#park.subsidize_party()
#print( "I just subsidized the ongoing party." )

