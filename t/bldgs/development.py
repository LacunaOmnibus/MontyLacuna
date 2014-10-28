
import os, sys
bindir = os.path.abspath(os.path.dirname(__file__))
libdir = bindir + "/../../lib"
sys.path.append(libdir)

import lacuna as lac

glc = lac.clients.Member(
    config_file = bindir + "/../../etc/lacuna.cfg",
    config_section = 'play_test',
)

my_planet = glc.get_body_byname( 'bmots rof 2.1' )
dev = my_planet.get_building_coords( -2, -4 )


### BE CAREFUL IN HERE.
### The subsidize_*() methods will spend your E


### Subsidize entire build queue
###
#rva = dev.subsidize_build_queue()
#glc.pp.pprint( rva['essentia_spent'] )


### Subsidize a single build
#sp = my_planet.get_building_coords( -1, -2 )
#one_build = { 'scheduled_id': sp.id }
#rvb = dev.subsidize_one_build( one_build )
#glc.pp.pprint( rvb )


### Cancel a single build
#sp = my_planet.get_building_coords( -1, -2 )
#one_cancel = { 'scheduled_id': sp.id }
#rvc = dev.cancel_build( one_cancel )
#glc.pp.pprint( rvc )

