
import os, sys
bindir = os.path.abspath(os.path.dirname(__file__))
libdir = bindir + "/../../lib"
sys.path.append(libdir)

import lacuna as lac

glc = lac.clients.Member(
    config_file = bindir + "/../../etc/lacuna.cfg",
    #config_section = 'play_test',
    config_section = 'my_sitter',
)

my_planet = glc.get_body_byname( 'bmots rof 2.1' )
dev = my_planet.get_building_coords( -2, -4 )



### Subsidize entire build queue
###
#rva = dev.subsidize_build_queue()
#glc.pp.pprint( rva['essentia_spent'] )


### Subsidize a single build
###
#sp = my_planet.get_building_coords( -1, -2 )
#one_build = { 'scheduled_id': sp.id }
#rvb = dev.subsidize_one_build( one_build )
#glc.pp.pprint( rvb )


### Cancel a single build
###
sp = my_planet.get_building_coords( -1, 5 )
one_cancel = { 'scheduled_id': sp.id }
queue, cost = dev.cancel_build( one_cancel )
print( "Now that we've canceled a building, the remaining queue will cost", cost, "E to subsidize." )
print( "Remaining in the build queue are:" )
for i in queue:
    print( "\t", i.name )

