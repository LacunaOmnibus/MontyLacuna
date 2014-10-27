
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
my_planet   = glc.get_body_byname( 'bmots rof 1.4' )
mcomm       = my_planet.get_building_coords( 4, -2 )


### See what missions are available
###
#mission_list = mcomm.get_missions()
#for m in mission_list:
#    print( m.rewards )


### Complete a mission.
###
#mission_list = mcomm.get_missions()
#m = mission_list[0]
#rva = mcomm.complete_mission( m.id )
#print( m.name )
#glc.pp.pprint( rva )


### Skip a mission.
###
mission_list = mcomm.get_missions()
for m in mission_list:
    if m.name == 'Orange Crush':
        rv = mcomm.skip_mission( m.id )
        glc.pp.pprint( rv )
        break

