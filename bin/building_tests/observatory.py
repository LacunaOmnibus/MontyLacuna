
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
my_planet   = glc.get_body_byname( 'bmots rof 1.1' )
obs         = my_planet.get_building_coords( 5, -3 )


### See what stars we have probed
###
#rva = obs.get_probed_stars()
#glc.pp.pprint( rva['stars'][0].color )
#print( "We have {} of a maximum {} stars probed, and {} probes currently on the way"
#    .format(rva['star_count'], rva['max_probes'], rva['travelling'] )
#)


### Abandon a single probe
###
#rvb = obs.get_probed_stars()
#for s in rvb['stars']:
#    if s.name == 'SMA1I 91 New Eagle':
#        print("abandoning")
#        obs.abandon_probe( s.id )
#        break


### Abandon all probes
###
#obs.abandon_all_probes()


