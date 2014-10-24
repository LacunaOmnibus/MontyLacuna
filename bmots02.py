


### This needs to ultimately go away, but I want it in github so it's handy 
### while I'm being attacked this weekend.

#2.1
#    sent 90
#   all on counter
#2.2
#    sent 64 (that's what the script said, but it looks like 90 to me)
#   all on counter
#2.4
#    sent 90
#   These guys are low level, so not on counter.  Saving for defense.
#2.6
#    sent 92
#   all on counter
#2.7
#    sent 81
#   unassigned - saved as defenders.

02 needs PS 25-30 inclusive (SCC is OK)
    make 26-30
    26
    27
    28
    29
    30

import os, sys
bindir = os.path.abspath(os.path.dirname(__file__))
libdir = bindir + "/lib"
sys.path.append(libdir)

import lacuna as lac

glc = lac.clients.Member(
    config_file = bindir + "/etc/lacuna.cfg",
    config_section = 'my_sitter',
    #config_section = 'play_test',
)
my_planet   = glc.get_body_byname( 'bmots rof 2.7' )
sp          = my_planet.get_building_coords( 5, 5 )


### View my ships
###
#myfilter    = { 'type': 'barge', }
#paging      = { 'page_number': 1, "items_per_page": 3 }
#sort        = 'speed'
#rva = sp.view_all_ships( paging, myfilter, sort )
#glc.pp.pprint( rva['ships'] )
#print( "There are {} of my ships in my filter.".format(rva['number_of_ships']) )


def get_orbiting_planet( glc, star_name:str, planet_name:str ):
    my_map = glc.get_map();
    rvc = my_map.get_star_by_name(star_name)
    target_planet = ''
    for i in rvc['star']['bodies']:
        if i['name'] == planet_name:
            target_planet = i
    if not target_planet:
        raise KeyError("Unable to find target planet", planet_name, ".")
    return target_planet

def get_task_ships_for( sp, target:dict, type:str, task:str = 'available', quantity:int = 1 ):
    rv = sp.get_my_ships_for( target )
    ships = [] 
    cnt = 0
    for i in rv[task]:
        if i['type'] == type:
            ships.append( i )
            cnt += 1
            if cnt >= quantity:
                break
    if not 'id' in ships[0]:
        raise KeyError("Unable to find any available", type, "ship.")
    return ships

def get_available_ships_for( sp, target:dict, type:str, quantity:int = 1 ):
    return get_task_ships_for( sp, target, type, 'available', quantity )

def get_incoming_ships_for( sp, target:dict, type:str, quantity:int = 1 ):
    return get_task_ships_for( sp, target, type, 'incoming', quantity )

def get_mining_ships_for( sp, target:dict, type:str, quantity:int = 1 ):
    return get_task_ships_for( sp, target, type, 'mining_plantforms', quantity )

def get_orbiting_ships_for( sp, target:dict, type:str, quantity:int = 1 ):
    return get_task_ships_for( sp, target, type, 'orbiting', quantity )

def get_unavailable_ships_for( sp, target:dict, type:str, quantity:int = 1 ):
    return get_task_ships_for( sp, target, type, 'unavailable', quantity )


### Send spies to the target
###
target_planet = get_orbiting_planet( glc, 'Oot Yaeplie Oad', 'SASS bmots 02' )
rva = sp.prepare_send_spies( my_planet.id, target_planet['id'] )
ship_id = rva['ships'][0]['id']
spy_ids = [ x['id'] for x in rva['spies'] ]
rvb = sp.send_spies( my_planet.id, target_planet['id'], ship_id, spy_ids )
print( "Sent", len(rvb['spies_sent']), "spies from", my_planet.name, ".")



### Fetch spies home again
### 
### And there was much rejoicing.
### 
### CHECK get_spies_back() needs to go into spaceport.py.
def get_spies_back( sp, from_id, ship_name = '' ):
    prep_rv = sp.prepare_fetch_spies( from_id, sp.body_id )

    ship_id = 0
    if ship_name:
        for ship in prep_prep_rv['ships']:
            if ship['name'] == ship_name:
                ship_id = ship['id']
                break
    else:
        ship_id = prep_rv['ships'][0]['id']     # No ship name specified.  Use the first one available.

    if int(ship_id) <= 0:
        raise KeyError("No ships matching your criteria are available to fetch spies.")

    spy_ids = []
    for i in prep_rv['spies']:
        if i['based_from']['body_id'] == sp.body_id and i['assigned_to']['body_id'] == from_id:
            spy_ids.append( i['id'] )
    fetch_rv = sp.fetch_spies( target_planet['id'], my_planet.id, ship_id, spy_ids )
    return fetch_rv
    
#target_planet = get_orbiting_planet( glc, 'SMA bmots 001', 'bmots rof 1.2' )
#rv = get_spies_back( sp, target_planet['id'] )

