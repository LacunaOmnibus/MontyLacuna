
import os, sys

libdir = os.path.abspath(os.path.dirname(__file__)) + "/../lib"
sys.path.append(libdir)

import lacuna

glc = lacuna.clients.Member(
    config_file = os.path.abspath(os.path.dirname(__file__)) + "/../etc/lacuna.cfg",
    config_section = 'play_test',
)


### Get some basic info about your planet
###
#p = glc.get_body_byname( 'bmots support 02' )
#print( "My planet is of type {}.  It orbits the star {} in orbit {}, and is owned by {}."
#    .format(p.surface_type, p.star_name, p.orbit, p.empire.name)
#)
#print( "There's {} bauxite and {} anthracite available.  But no unobtainium."
#    .format(p.ore.bauxite, p.ore.anthracite)    # etc
#)
#if hasattr(p, 'station'):
#    print( "This planet is under the control of", p.station.name )


### Get the building at a specific coordinate on your planet's surface
###
#my_planet = glc.get_body_byname( 'bmots support 02' )
#my_pcc = my_planet.get_building_coords(0, 0)
#print( "The building's full name is {}.  Mine is operating at {}% efficiency."
#    .format(my_pcc.name, my_pcc.efficiency)
#)
#quit()


### Get all of the buildings of a certain type above a specific level
### 
### Since getting building lists like this requires looking at each individual 
### building, it can be slow.  So let's turn caching on in case we want to run 
### this more than once.
#glc.cache_on( 'my_buildings_test', 3600 )
#my_planet = glc.get_body_byname( 'bmots support 01' )
#ports = my_planet.get_buildings_bytype('spaceport', 25)
#for i in ports:
#    print( "The spaceport at ({},{}) is level {}."
#        .format(i.x, i.y, i.level)
#    )


### Repair broken buildings
###
#building_ids = []
#for id, bldg_dict in my_planet.buildings_id.items():
#    if int(bldg_dict['efficiency']) < 100:
#        print( "{} is damaged.".format(bldg_dict['name']) )
#        building_ids.append( id )
#repaired = my_planet.repair_list( building_ids )
#for i in repaired:
#    print( "{} is now at {}% efficiency."
#        .format(i.name, i.efficiency )
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
#my_planet = glc.get_body_byname( 'bmots support 02' )
#bldabl = my_planet.get_buildable( 1, 0, 'Water' )
#for i in bldabl:
#    print( "I can build a {} on this plot in {} seconds.".format(i.name, i.cost.time) )


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

