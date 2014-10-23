
import os, sys
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
sp          = my_planet.get_building_coords( 5, 5 )


### View my ships
###
#myfilter    = { 'type': 'barge', }
#paging      = { 'page_number': 1, "items_per_page": 3 }
#sort        = 'speed'
#rva = sp.view_all_ships( paging, myfilter, sort )
#glc.pp.pprint( rva['ships'] )
#print( "There are {} of my ships in my filter.".format(rva['number_of_ships']) )


### View incoming foreign ships
###
#rvb = sp.view_foreign_ships( 1 )
#glc.pp.pprint( rvb['ships'] )
#print( "There are {} incoming foreign ships.".format(rvb['number_of_ships']) )


### Get list of my ships available to send as a fleet to a given target.
###
target_star_name   = 'Schu Ize'
target_planet_name = '--=Tatooine=--'  # must orbit target_star_name
my_map = glc.get_map();
rvc = my_map.get_star_by_name(target_star_name)
target_planet = ''
for i in rvc['star']['bodies']:
    if i['name'] == target_planet_name:
        target_planet = i
#target = { 'body_name': target_planet['name'] }
#rvd = sp.get_my_fleet_for( target )
#glc.pp.pprint( rvd['ships'] )


### Get list of my ships available to send to a given target.
### This is using the target_star and target_planet stuff from the block 
### above, so make sure it's not commented out.
###
#target = { 'star_name': rvc['star']['name'] }
target = { 'body_name': target_planet['name'] }
rvd = sp.get_my_ships_for( target )
#glc.pp.pprint( rvd['incoming'] )

#glc.pp.pprint( rvd['available'] )
#print( len(rvd['available']) )

#glc.pp.pprint( rvd['unavailable'] )
#print( len(rvd['unavailable']) )

#glc.pp.pprint( rvd['orbiting'] )
#print( len(rvd['orbiting']) )

glc.pp.pprint( rvd['mining_platforms'] )
print( len(rvd['mining_platforms']) )

