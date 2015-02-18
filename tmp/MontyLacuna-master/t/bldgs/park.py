
import os, re, sys
bindir = os.path.abspath(os.path.dirname(sys.argv[0]))
libdir = bindir + "/../../lib"
sys.path.append(libdir)

import lacuna as lac

glc = lac.clients.Member(
    config_file = bindir + "/../../etc/lacuna.cfg",
    config_section = 'play_test',
)
my_planet   = glc.get_body_byname( 'bmots support 01' )
park        = my_planet.get_buildings_bytype( 'park', 0, 1 )[0]


### See if there's a party going on right now.  If so, show how much longer 
### it'll continue.
###
#party = park.view( )
#if party.can_throw:
#    print( "I can throw a party." )
#else:
#    t = park.sec2time( party.seconds_remaining )
#    print( "A party is currently running for the next {}d, {}h, {}m, {}s.  It'll produce {:,} happy."
#        .format(t.days, t.hours, t.minutes, t.seconds, party.happiness)
#    )


### Throw a party
###
#party = park.throw_a_party();
#t = park.sec2time( party.seconds_remaining )
#print( "I just threw a party that will last {}d, {}h, {}m, {}s.  It'll produce {:,} happy."
#        #.format(party.seconds_remaining, party.happiness)
#        .format(t.days, t.hours, t.minutes, t.seconds, party.happiness)
#    )


### Subsidize the party for 2E (gotta pay to clear out all those fratboys!)
### 
#park.subsidize_party()
#print( "I just subsidized the ongoing party." )

