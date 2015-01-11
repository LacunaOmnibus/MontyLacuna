
import os, sys
bindir = os.path.abspath(os.path.dirname(sys.argv[0]))
libdir = bindir + "/../../lib"
sys.path.append(libdir)

import lacuna as lac

glc = lac.clients.Member(
    config_file = bindir + "/../../etc/lacuna.cfg",
    config_section = 'play_test',
    #config_section = 'my_sitter',
)

my_planet = glc.get_body_byname( 'bmots rof 2.1' )
dev = my_planet.get_buildings_bytype( 'development', 0, 1 )[0]


### Subsidize entire build queue
###
#cost = dev.subsidize_build_queue()
#print( "I spent {} E to subsidize my whole build queue.".format(cost) )


### Subsidize a single build
###
#bldg = my_planet.get_building_coords( 5, 4 )   # coords of a building that's upgrading now.
#one_build = { 'scheduled_id': bldg.id }
#cost = dev.subsidize_one_build( one_build )
#print( "I spent {} E to subsidize a single building.".format(cost) )


### Cancel a single build
###
#bldg = my_planet.get_building_coords( -1, 5 )    # some currently upgrading building
#one_cancel = { 'scheduled_id': bldg.id }
#queue, cost = dev.cancel_build( one_cancel )
#print( "Now that we've canceled a building, the remaining queue will cost", cost, "E to subsidize." )
#print( "Remaining in the build queue are:" )
#for i in queue:
#    print( "\t", i.name )

