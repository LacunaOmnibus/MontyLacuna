
import os, re, sys
bindir = os.path.abspath(os.path.dirname(sys.argv[0]))
libdir = bindir + "/../../lib"
sys.path.append(libdir)

import lacuna as lac

glc = lac.clients.Member(
    config_file = bindir + "/../../etc/lacuna.cfg",
    config_section = 'play_test_one',
)
my_planet   = glc.get_body_byname( 'Earph' )
obs         = my_planet.get_building_coords( 5, -3 )


### See what stars we have probed
###
#stars, out, max, travelling = obs.get_probed_stars()
#print( "We have {} of a maximum {} stars probed, and {} probes currently on the way"
#    .format(out, max, travelling )
#)
#print( "We have probes at these stars:" )
#for s in stars[0:3]:
#    print( "\t{} ({}, {}) is {} and has {} bodies orbiting it."
#        .format(s.name, s.x, s.y, s.color, len(s.bodies))
#    )


### Abandon a single probe
###
#stars, out, max, travelling = obs.get_probed_stars()
#s = stars[-1]
#print( "Before abandoning one, we have {} of a maximum {} stars probed." .format(out, max) )
#obs.abandon_probe( s.id )
#stars, out, max, travelling = obs.get_probed_stars()
#print( "After abandoning one, we have {} of a maximum {} stars probed." .format(out, max) )


### Abandon all probes
###
#obs.abandon_all_probes()


