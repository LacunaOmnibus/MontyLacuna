
### This needs to ultimately go away, but I want it in github so it's handy 
### while I'm being attacked this weekend.

import lacuna as lac

glc = lac.clients.Member(
    config_file = bindir + "/etc/lacuna.cfg",
    config_section = 'my_sitter',
    #config_section = 'play_test',
)
my_planet   = glc.get_body_byname( 'bmots rof 2.7' )
sp          = my_planet.get_building_coords( 5, 5 )
my_map      = glc.get_map();


### View my ships
###
#myfilter    = { 'type': 'barge', }
#paging      = { 'page_number': 1, "items_per_page": 3 }
#sort        = 'speed'
#rva = sp.view_all_ships( paging, myfilter, sort )
#glc.pp.pprint( rva['ships'] )
#print( "There are {} of my ships in my filter.".format(rva['number_of_ships']) )


### Send spies to the target
###
target_planet = map.get_orbiting_planet( 'Oot Yaeplie Oad', 'SASS bmots 02' )
rva = sp.prepare_send_spies( my_planet.id, target_planet['id'] )
ship_id = rva['ships'][0]['id']
spy_ids = [ x['id'] for x in rva['spies'] ]
rvb = sp.send_spies( my_planet.id, target_planet['id'], ship_id, spy_ids )
print( "Sent", len(rvb['spies_sent']), "spies from", my_planet.name, ".")


