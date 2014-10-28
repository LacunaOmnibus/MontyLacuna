
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
minmin      = my_planet.get_building_coords( -3, 3 )


### See what platforms you have out
###
#rva = minmin.view_platforms()
#glc.pp.pprint( rva['platforms'] )
#print( "I have {} of a maximum {} platforms out.".format(len(rva['platforms']), rva['max_platforms']) )


### See what ships are mining
###
#rvb = minmin.view_ships()
#glc.pp.pprint( rvb['ships'] )
#quit()


### Add a cargo ship to the current mining fleet
###
#rvc = minmin.view_ships()
#for s in rvc['ships']:
#    if s['task'] == 'Docked':
#        minmin.add_cargo_ship_to_fleet( s['id'] )
#        print( "I just added ship {} (id {}) to your mining fleet.".format(s['name'], s['id']) )
#        break



### Remove a cargo ship to the current mining fleet
###
#rvd = minmin.view_ships()
#for s in rvd['ships']:
#    if s['task'] == 'Mining' and re.match("Hulk Fast", s['name']):
#        minmin.remove_cargo_ship_from_fleet( s['id'] )
#        print( "I just removed ship {} (id {}) from your mining fleet.".format(s['name'], s['id']) )
#        break


### Abandon a mining platform
###
#rve = minmin.view_platforms()
#for i in rve['platforms']:
#    if 'asteroid' in i and i['asteroid']['name'] == 'Su Bootto Zoa 5':
#        j = i['asteroid']
#        minmin.abandon_platform( i['id'] )
#        print( "I just abandoned the platform at {} (ID {}).".format(j['name'], j['id']) )
#        break

