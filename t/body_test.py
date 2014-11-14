
import os
import sys
import pprint
pp = pprint.PrettyPrinter( indent = 4 )
import re

bindir = os.path.abspath(os.path.dirname(__file__))
libdir = bindir + "/../lib"
sys.path.append(libdir)

import lacuna as lac


glc = lac.clients.Member(
    config_file = bindir + "/../etc/lacuna.cfg",
    config_section = 'play_test',
)

my_map = glc.get_map()


### Find some information about the body in orbit 3 around a specific star.
### Use the name of any star whose bodies you can see on the starmap.
###
#starname = 'Sol'
#star = my_map.get_star_by_name(starname)
#for i in star.bodies:
#    if i.orbit == '3':
#        print( "The planet in orbit 3 around {} is named {}."
#            .format(starname, i.name) 
#        )


### Get one of your planets
###
#my_planet = glc.get_body_byname( 'bmots01' )
#print( "Planet {} has ID {}.".format(my_planet.name, my_planet.id) )


### Repair broken buildings
###
#my_planet = glc.get_body_byname( 'bmots support 02' )
#building_ids = []
#for id, bldg_dict in my_planet.buildings_id.items():
#    if int(bldg_dict['efficiency']) < 100:
#        print( "{} is damaged.".format(bldg_dict['name']) )
#        building_ids.append( id )
#rv = my_planet.repair_list( building_ids )
#for id, bldg_dict in rv['buildings'].items():
#    print( "{} is now at {}% efficiency."
#        .format(bldg_dict['name'], bldg_dict['efficiency'] )
#    )


### Rearrange
### 
### First, find out the ID of the building at coords (5, 5):
#my_planet = glc.get_body_byname( 'bmots01' )
#bldg_to_move = ''
#for bid, mydict in my_planet.buildings_id.items():
#    if mydict['x'] == '5' and mydict['y'] == '5':
#        bldg_to_move = mydict
#if not bldg_to_move:
#    raise KeyError("You don't have any buildings at 5, 5 on this planet.")
### 
### Now, set up  the move_to list, specifying where the building should end 
### up, then move it.
#move_to = [{
#    'id': bldg_to_move['id'],
#    'x': 0,                 # enter the coords to move it to
#    'y': 1                  # enter the coords to move it to
#}]   
#rv = my_planet.rearrange_buildings( move_to )
#print( "I just moved the building {} to ({}, {})."
#    .format(rv['moved']['name'],rv['moved']['x'],rv['moved']['y'])
#)


### Get list of buildings that can be built on a given plot
###
#my_planet = glc.get_body_byname( 'bmots support 01' )
#rv = my_planet.get_buildable( 0, 1, 'Water' )
#for name, bldg_dict in rv['buildable'].items():
#    print( "I can build a {} on this plot.".format(name) )


### Rename your planet
###
#my_planet = glc.get_body_byname( 'bmots support 01' )
#if my_planet.rename( 'MY NEW PLANET NAME' ):
#    print( "The rename test worked!  Don't forget to go rename your planet back now." )


### Abandon your planet
### DO NOT TEST THIS UNLESS YOU'RE 100% SURE YOU'RE LOGGED IN WITH A TEST 
### ACCOUNT.
###
#my_planet = glc.get_body_byname( 'bmots support 01' )
#raise KeyError( "really be very very careful with this - you're about to abandon a planet." )
#my_planet.abandon()

