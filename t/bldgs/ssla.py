
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
ssla        = my_planet.get_building_coords( 1, -4 )


### View buildable plans and their costs
###
#plans, costs, sub, making = ssla.view()
#print("I can make these:")
#for i in plans:
#    print( "\t{} ({})".format(i.name, i.type) )
#print("Time needed to build plans:")
#for i in costs:
#    print( "\tLevel", i.level, 'will take', i.time, "seconds." )
#print( "It'll cost", sub, "E to subsidize.")
#print( "Currently making", making)


### Make a plan
###
#plans, costs, sub, making = ssla.view()
#print( "Currently making", making)
#if making == 'None':
#    plans, costs, sub, making = ssla.make_plan('warehouse', 2)
#    print( "Now making", making)


### Subsidize a plan
###
#plans, costs, sub, making = ssla.view()
#print( "Currently making", making)
#if making != 'None':
#    plans, costs, sub, making = ssla.subsidize_plan()
#    print( "Now making", making)


