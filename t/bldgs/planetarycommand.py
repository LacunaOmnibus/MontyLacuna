
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
my_planet   = glc.get_body_byname( 'bmots rof 2.1' )
pcc         = my_planet.get_building_coords( 0, 0 )




### View basic info
###
#food, ore, planet, cost = pcc.view()
#print( "I have {1:,} {0} stored and am producing {2:,} {0} per hour."
#    .format('algae', int(food.algae_stored), int(food.algae_hour))
#)
#print( "I have {1:,} {0} stored and am producing {2:,} {0} per hour."
#    .format('bauxite', int(ore.bauxite_stored), int(ore.bauxite_hour))
#)
#print( "This planet has {:,}/{:,} waste and {:,}/{:,} energy and is in orbit {}."
#    .format(int(planet.waste_stored), int(planet.waste_capacity), 
#            int(planet.energy_stored), int(planet.energy_capacity), planet.orbit)
#)
#print( "It'll cost me {:,} happy for my next colony or station.".format(int(cost)) )


### Check plans
###
#plans = pcc.view_plans()
#for i in plans[0:5]:
#    print( "I have {} of {} at level {}+{}"
#        .format(i.quantity, i.name, i.level, i.extra_build_level)
#    )


### Check incoming supply chains
###
#sc = pcc.view_incoming_supply_chains()
#for i in sc[0:5]:
#    print( "I have {:,}/hour of {} incoming from {}."
#        .format(int(i.resource_hour), i.resource_type, i.from_body['name'])
#    )

