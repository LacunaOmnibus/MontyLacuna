
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
my_map      = glc.get_map();


### CHECK
### Everything in here worked in testing, but too many of the examples depend 
### on results from previous examples.
###
### Clean up.
###
###
### Also, there are a number of functions defined in here that need to become 
### methods of one of my classes.  Keep searching for CHECK.




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
#target_planet = my_map.get_orbiting_planet( 'Schu Ize', '--=Tatooine=--' )   # inhabited, hostile
#target = { 'body_name': target_planet.name }
#rvd = sp.get_my_fleet_for( target )
#glc.pp.pprint( rvd['ships'] )


### Get list of my ships available to send to a given target.
### This is using the target from the block above, so make sure it's not 
### commented out.
###
#rvd = sp.get_my_ships_for( target )
#glc.pp.pprint( rvd['incoming'] )

#glc.pp.pprint( rvd['available'] )
#print( len(rvd['available']) )

#glc.pp.pprint( rvd['unavailable'] )
#print( len(rvd['unavailable']) )

#glc.pp.pprint( rvd['orbiting'] )
#print( len(rvd['orbiting']) )

#glc.pp.pprint( rvd['mining_platforms'] )
#print( len(rvd['mining_platforms']) )

### Send a ship to the target
#target_planet = my_map.get_orbiting_planet( 'SMA bmots 018', 'Eagiflio 3' )   # roid
#target = { 'body_name': target_planet.name }
#rve = sp.get_my_ships_for( target )
#ship = get_available_ships_for( sp, target, 'mining_platform_ship', 1 )[0]
#rvf = sp.send_ship( ship['id'], target )
#glc.pp.pprint( rvf['ship'] )


### Send ships of a given type to a target.
###
#my_map = glc.get_map();
#target_star = my_map.get_star_by_name('SMA bmots 001') # this whole system is mine
#glc.pp.pprint( "Your target star's color is", target_star.color, "." )
#target = { 'star_name': target_star.name }
#types = [{
#        'type': 'scow',
#        'speed': 1800,
#        'hold_size': 1170000,
#    }]
#arrival = {
#    "day": 24,
#    "hour": 23,
#    "minute": 0,
#    "second": 0,
#}
#sp.send_my_ship_types( target, types, arrival )


### Send a fleet of ships at a target
###
#my_map = glc.get_map();
#target_star = my_map.get_star_by_name('SMA bmots 001')
#target = { 'star_name': target_star.name }
#ship_ids = []
#for i in get_available_ships_for( sp, target, 'scow_mega', 5 ):
#    ship_ids.append( i['id'] )
#sp.send_fleet( ship_ids, target, 200 )


### Recall a ship orbiting a planet
###
#target_planet = my_map.get_orbiting_planet( 'Schu Ize', '--=Tatooine=--' )
#target = { 'body_name': target_planet.name }
#ship = get_orbiting_ships_for( sp, target, 'fighter', 1 )[0]
#sp.recall_ship( ship['id'] )
#print( "I just recalled ship", ship['id'] )


### Recall all orbiting ships
###
#rvg = sp.recall_all()
#glc.pp.pprint( rvg['ships'] )


### Rename a ship
###
#paging      = {}
#myfilter    = { 'type': 'scow', }
#rvh = sp.view_all_ships( paging, myfilter )
#sp.name_ship( rvh['ships'][0]['id'], 'My New Ship Name' )
### These attempts will raise 1005:
#sp.name_ship( rvh['ships'][0]['id'], 'My New Way-Too-Long Ship Name That Will Simply Not Work' )
#sp.name_ship( rvh['ships'][0]['id'], 'Shit Fucker' )


### Scuttle a ship
###
#paging      = {}
#myfilter    = { 'type': 'scow', }
#rv = sp.view_all_ships( paging, myfilter )
#ship = {}
#for i in rv['ships']:
#    if i['name'] == 'scuttle_me':
#        ship = i
#if not 'id' in ship:
#    raise KeyError("Unable to find the requested ship.")
#print( "Scuttling ship", ship['name'] )
#sp.scuttle_ship( ship['id'] )


### Scuttle a bunch of ships
###
#paging      = {}
#myfilter    = { 'type': 'scow', }
#rv = sp.view_all_ships( paging, myfilter )
#ship_ids = []
#for i in rv['ships']:
#    ship_ids.append( i['id'] )
#print( "Scuttling {} scows".format(len(ship_ids)) )
#sp.mass_scuttle_ship( ship_ids )


### View ships currently in the air.
###
#rv = sp.view_ships_travelling()
#glc.pp.pprint( rv['ships_travelling'] )
#print( "There are {} ships in the air right now.".format(rv['number_of_ships_travelling']) )


### View ships currently orbiting other planets
###
#rv = sp.view_ships_orbiting()
#glc.pp.pprint( rv['ships'] )
#print( "There are {} ships orbiting {} right now.".format(rv['number_of_ships'], my_planet.name) )
#print('---------')


### Prepare to send spies to a target
###
#target_planet = my_map.get_orbiting_planet( 'SMA bmots 001', 'bmots rof 1.2' )
#rv = sp.prepare_send_spies( my_planet.id, target_planet.id )
#glc.pp.pprint( rv['ships'] )
#print("------------")
#glc.pp.pprint( rv['spies'] )


### Send spies to the target
###
#target_planet = my_map.get_orbiting_planet( 'SMA bmots 001', 'bmots rof 1.2' )
#rva = sp.prepare_send_spies( my_planet.id, target_planet.id )
#ship_id = rva['ships'][0]['id']
#spy_ids = [ x['id'] for x in rva['spies'][0:3] ]
#rvb = sp.send_spies( my_planet.id, target_planet.id, ship_id, spy_ids )
#glc.pp.pprint( rvb )


### Prepare to fetch spies home again
#target_planet = my_map.get_orbiting_planet( 'SMA bmots 001', 'bmots rof 1.2' )
#rv = sp.prepare_fetch_spies( my_planet.id, target_planet.id )
#glc.pp.pprint( rv['ships'][0] )
#print("------------")
#glc.pp.pprint( rv['spies'][0] )


### Fetch spies home again
### 
### This is the hard way.  See the next block below.
###
#target_planet = my_map.get_orbiting_planet( 'SMA bmots 001', 'bmots rof 1.2' )
#rva = sp.prepare_fetch_spies( target_planet.id, my_planet.id )
#ship_id = rva['ships'][0]['id']
#spy_ids = []
#for i in rva['spies']:
#    if i['based_from']['body_id'] == my_planet.id and i['assigned_to']['body_id'] == target_planet.id:
#        spy_ids.append( i['id'] )
#rvb = sp.fetch_spies( target_planet.id, my_planet.id, ship_id, spy_ids )
#glc.pp.pprint( rvb )


### Fetch spies home again
### 
### And there was much rejoicing.
### 
#target_planet = my_map.get_orbiting_planet( 'SMA bmots 001', 'bmots rof 1.2' )
#rv = sp.get_spies_back( target_planet.id )


### Check battle logs
###
#rv = sp.view_battle_logs()
#glc.pp.pprint( rv['battle_log'][0] )
#print( "--", rv['number_of_logs'], "--" )


