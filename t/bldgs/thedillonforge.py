
import os, re, sys
bindir = os.path.abspath(os.path.dirname(sys.argv[0]))
libdir = bindir + "/../../lib"
sys.path.append(libdir)

import lacuna as lac

glc = lac.clients.Member(
    config_file = bindir + "/../../etc/lacuna.cfg",
    #config_section = 'my_sitter',
    config_section = 'play_test',
)
my_planet   = glc.get_body_byname( 'bmots rof 2.1' )
forge       = my_planet.get_building_coords( 0, -1 )


### View list of plans
###
make, split, ct, sr, can, wrk, sub = forge.view()
#for i in make:
#    print( "{}, {}, {}, {}".format(i.name, i.max_level, i.perl_class, i.reset_sec_per_level) )
#print("--------")
#for i in split:
#    print( "{}, {}, {}, {}, {}, {}".format( i.name, i.perl_class, i.level, 
#                                            i.extra_build_level, i.fail_chance, 
#                                            i.reset_seconds  ))

### Make a plan
###
#make, split, ct, sr, can, wrk, sub = forge.make_plan( 'Module::PoliceStation', 1 )
#print( ct )
#print( sr )
#print( can )
#print( wrk )
#print( sub )


### Split a plan
###
#make, split, ct, sr, can, wrk, sub = forge.split_plan( 'Permanent::Beach3', 1, 7 )
#print( ct )
#print( sr )
#print( can )
#print( wrk )
#print( sub )


### Subsidize the current job
###
forge.subsidize()




### Subsidize the current job
###
#make, split, ct, sr, can, wrk, sub = forge.make_plan( 'Module::PoliceStation', 1 )


