
### 
### Search LEFT OFF HERE
###

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
### The map on PT is smaller than that on US1, but the US1 data was copied to 
### PT.  So be sure you're getting one of your bodies that's actually within 
### the bounds of the PT map or Weird Things can happen.
my_planet   = glc.get_body_byname( 'bmots01' )
sp          = my_planet.get_building_coords( 5, 5 )
my_map      = glc.get_map();



### View my ships
###
#myfilter    = { 'type': 'excavator', }
#paging      = { 'page_number': 1, "items_per_page": 3 }
#sort        = 'speed'
#ships, number = sp.view_all_ships( paging, myfilter, sort )
#for i in ships:
#    print( i.type_human )
#print( "There are {} of my ships matching my filter.".format(number) )


### View incoming foreign ships
###
#ships, number = sp.view_foreign_ships( 1 )
#for i in ships:
#    print( i.type_human )
#print( "There are {} incoming foreign ships.".format(number) )


### Get list of my ships available to send as a fleet to a given target.
### 
#target_planet = my_map.get_orbiting_planet( 'Schu Ize', '--=Tatooine=--' )   # inhabited, hostile
#target = { 'body_id': target_planet.id }
#ships = sp.get_my_fleet_for( target )
#for i in ships:
#    print( i.type_human )


### Get list of my ships available to send to a given target.
### The Hard Way
###
#target_planet = my_map.get_orbiting_planet( 'Schu Ize', '--=Tatooine=--' )   # inhabited, hostile
#target = { 'body_id': target_planet.id }
#inc, avail, unavail, orbit, mining, fleet_limit = sp.get_my_ships_for( target )
#for i in avail[0:2]:
#    print(i.name, "is available")
#print("--------------")
#for i in unavail[0:2]:
#    print(i.name, "is not available because", i.reason)
#print("--------------")
#for i in orbit[0:2]:
#    print(i.name, "is orbiting ", i.orbiting['name'])
#print("--------------")
#for i in mining[0:2]:
#    print(i.empire_name, "owns this mining platform.")
#print("--------------")


### Get list of my ships available to send to a given target.
### The Easy Way
###
#target_planet = my_map.get_orbiting_planet( 'Schu Ize', '--=Tatooine=--' )   # inhabited, hostile
#target = { 'body_id': target_planet.id }
#ships = sp.get_available_ships_for( target )
#for i in ships[0:3]:
#    print( i.name )


### Send a ship to the target
###
#target_planet = my_map.get_orbiting_planet( 'Cronos', 'Lo Soafrui Slee 8' )   # roid
#target = { 'body_name': target_planet.name }
#ships = sp.get_available_ships_for( target )
#ship = ''
#for i in ships:
#    if i.type == 'mining_platform_ship':
#        ship = i
#rv = sp.send_ship( ship.id, target )
#glc.pp.pprint( rv.name )


### Send ships of a given type to a target.
###
#my_map = glc.get_map();
#target_star = my_map.get_star_by_name('Schu Ize')
#print( "Your target star's color is", target_star.color, "." )
#target = { 'star_name': target_star.name }
#types = [{
#        'type': 'scow',
#        'speed': 1800,
#        'hold_size': 1170000,
#    }]
#arrival = {
#    "day": 28,          # date of arrival
#    "hour": 23,         # 24-hour server clock hour of arrival
#    "minute": 59,       # etc
#    "second": 0,
#}
#sp.send_my_ship_types( target, types, arrival )


### Send a fleet of ships at a target
###
#my_map = glc.get_map();
#target_star = my_map.get_star_by_name('Schu Ize')
#target_planet = my_map.get_orbiting_planet( 'Schu Ize', '--=Tatooine=--' )
#target = { 'body_name': target_planet.name }
#ship_ids = []
#for i in sp.get_available_ships_for( target ):
#    if i.type == 'fighter':
#        ship_ids.append( i.id )
#        if len(ship_ids) >= 5:
#            break
#sp.send_fleet( ship_ids, target )


### Recall a ship orbiting a planet
###
#target_planet = my_map.get_orbiting_planet( 'Schu Ize', '--=Tatooine=--' )
#target = { 'body_name': target_planet.name }
#ships = sp.get_orbiting_ships_for( target )
#ship = ships[0]
#sp.recall_ship( ship.id )
#print( "I just recalled ship", ship.id )


### Recall all orbiting ships
###
#sp.client.debugging_method = 'recall_all'
#recalled = sp.recall_all()
#for i in recalled:
#    print("Returning from", i.returning_from['name'], "to", i.to['name'])


### Rename a ship
###
#paging      = {}
#myfilter    = { 'type': 'scow', }
#ships, number = sp.view_all_ships( paging, myfilter )
#for i in ships:
#    print("Renaming", i.name, "to 'My New Ship Name'.")
#    sp.name_ship( i.id, 'My New Ship Name' )
    ### These attempts will raise 1005:
    #sp.name_ship( i.id, 'My New Way-Too-Long Ship Name That Will Simply Not Work' )
    #sp.name_ship( i.id, 'Shit Fucker' )


### Scuttle a ship
###
#paging      = {}
#myfilter    = { 'type': 'scow', }
#ships, number = sp.view_all_ships( paging, myfilter )
#ship = {}
#for i in ships:
#    if i.name == 'My New Ship Name':
#        ship = i
#        break
#if not hasattr(ship, 'id'):
#    raise KeyError("Unable to find the requested ship.")
#print( "Scuttling ship", ship.name )
#sp.scuttle_ship( ship.id )


### Scuttle a bunch of ships
###
#paging      = {}
#myfilter    = { 'type': 'scow', }
#ships, number = sp.view_all_ships( paging, myfilter )
#ship_ids = []
#for i in ships:
#    ship_ids.append( i.id )
#print( "Scuttling {} scows".format(len(ship_ids)) )
#sp.mass_scuttle_ship( ship_ids )


### View ships currently in the air.
###
#slist, number = sp.view_ships_travelling()
#for i in slist:
#    print( i.name )
#print( "There are {} ships in the air right now.".format(number) )


### View foreign ships currently orbiting this planet
###
#ships, number = sp.view_ships_orbiting()
#for i in ships:
#    print( i.name )
#print( "There are {} foreign ships orbiting {} right now.".format(number, my_planet.name) )
#print('---------')


### Prepare to send spies to a target
###
#target_planet = my_map.get_orbiting_planet( 'SMA bmots 001', 'bmots rof 1.2' )
#ships, spies = sp.prepare_send_spies( my_planet.id, target_planet.id )
#print("Available Ships")
#for i in ships:
#    print( i.name )
#print("------------")
#print("Available Spies")
#for i in spies:
#    print( "{} is based on {} and has performed {} off and {} def missions.".format(
#        i.name, i.based_from.name, i.mission_count.offensive, i.mission_count.defensive
#    ))


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


### Look at battle logs
###
#rv = sp.view_battle_logs()
#glc.pp.pprint( rv['battle_log'][0] )
#print( "--", rv['number_of_logs'], "--" )


