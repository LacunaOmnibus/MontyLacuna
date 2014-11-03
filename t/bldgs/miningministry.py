
import os, re, sys
bindir = os.path.abspath(os.path.dirname(__file__))
libdir = bindir + "/../../lib"
sys.path.append(libdir)

import lacuna as lac

glc = lac.clients.Member(
    config_file = bindir + "/../../etc/lacuna.cfg",
    config_section = 'my_sitter',
    #config_section = 'play_test',
)
my_planet   = glc.get_body_byname( 'bmots rof 1.1' )
minmin      = my_planet.get_building_coords( -3, 3 )


### See what platforms you have out
###
#plats, max = minmin.view_platforms()
#print( "I have {} of a maximum {} platforms out.".format(len(plats), max) )
#for i in plats[0:3]:
#    print( "The plat on {} is producing {} chromite per hour and its shipping capacity is {}."
#        .format(i.asteroid['name'], i.chromite_hour, i.shipping_capacity)
#    )


### See what ships are mining
###
#ships = minmin.view_ships()
#for i in ships:
#    if i.task == 'Mining':
#        print( "Ship {} is currently on mining duty.".format(i.name) )


### Add a cargo ship to the current mining fleet
###
#ships = minmin.view_ships()
#for s in ships:
#    if s.task == 'Docked':
#        minmin.add_cargo_ship_to_fleet( s.id )
#        print( "I just added ship {} (id {}) to your mining fleet.".format(s['name'], s['id']) )
#        break



### Remove a cargo ship to the current mining fleet
###
#ships = minmin.view_ships()
#for s in ships:
#    if s.task == 'Mining' and re.match("Hulk Fast", s.name):
#        minmin.remove_cargo_ship_from_fleet( s.id )
#        print( "I just removed ship {} (id {}) from your mining fleet.".format(s['name'], s['id']) )
#        break


### Abandon a mining platform
###
#plats = minmin.view_platforms()
#for i in plats:
#    if i.asteroid['name'] == 'Su Bootto Zoa 5':
#        j = i['asteroid']
#        minmin.abandon_platform( i.id )
#        print( "I just abandoned the platform at {} (ID {}).".format(j.name, j.id) )
#        break

