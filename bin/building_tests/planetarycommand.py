
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
pcc         = my_planet.get_building_coords( 0, 0 )


### View basic info
###
#view = pcc.view()
#print( "I'm producing", view['ore']['anthracite_hour'], "anthracite per hour." )
#print( "It'll cost me", view['next_colony_cost'], "happy for my next colony." )
#print( "etc..." )


### Check plans
###
#plans = pcc.view_plans()
#glc.pp.pprint( plans['plans'] )


### Check incoming supply chains
###
#sc = pcc.view_incoming_supply_chains()
#glc.pp.pprint( sc['supply_chains'] )

