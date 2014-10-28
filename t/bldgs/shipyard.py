
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
sy          = my_planet.get_building_coords( 4, -4 )


### View build queue
###
#ships, number, cost = sy.view_build_queue()
#for i in ships:
#    print( i.type_human )
#print( number, "ships are building.")
#print( "It'll cost", cost, "E to subsidize them.")


### Subsidize whole build queue
###
#rv = sy.subsidize_build_queue()
#del rv['status']
#glc.pp.pprint( rv )


### Subsidize a single ship in the queue
### To test, add a few supply pods to the queue (they're slow to build), then 
### add an excavator after the pods.
###
#ships, number, cost = sy.view_build_queue()
#ship_id = 0
#for i in ships:
#    print( "Got", i.type_human )
#    if i.type_human == 'Excavator':
#        print("Subsidizing this one.")
#        ship_id = i.id
#        break
#sy.subsidize_ship( {'ship_id': ship_id} )


### Get buildable ships
###
#ships, docks, q_max, q_used = sy.get_buildable( 'Trade' )
#for i in ships:
#    print( i.type )
#print( docks, "docks are available for new ships.")
#print( "We have", q_used, "of a maximum", q_max, "ships queued.")


### Build some ships
###
#ships, number, cost = sy.build_ship('excavator', 2)
#print( number, "ships have been added to the queue.")
#print( "It'll cost", cost, "E to subsidize the entire queue.")


