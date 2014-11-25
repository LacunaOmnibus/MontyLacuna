
import os, re, sys
bindir = os.path.abspath(os.path.dirname(__file__))
libdir = bindir + "/../../lib"
sys.path.append(libdir)

import lacuna as lac

glc = lac.clients.Member(
    config_file = bindir + "/../../etc/lacuna.cfg",
    config_section = 'my_real',
)

my_station = glc.get_body_byname( 'SASS bmots 02' )
scc = my_station.get_buildings_bytype( 'stationcommand', 0, 1 )[0]



### View station details
### 
#view = scc.view()
#print( "My station {} has {:,} energy stored and is making {:,} water per hour."
#    .format(view.name, view.energy_stored, view.water_hour)
#)


### View plans onsite
### 
#plans = scc.view_plans()
#for i in plans:
#    print( "I have {} {} plans at level {}+{}."
#        .format(i.quantity, i.name, i.level, i.extra_build_level )
#    )


### View incoming supply chains
### 
#chains = scc.view_incoming_supply_chains()
#for i in chains:
#    print( "{:,}/hr of {} is coming from {} at {}% efficiency."
#        .format(int(i.resource_hour), i.resource_type, i.from_body.name, i.percent_transferred)
#    )

