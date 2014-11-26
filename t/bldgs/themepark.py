
import os, re, sys
bindir = os.path.abspath(os.path.dirname(sys.argv[0]))
libdir = bindir + "/../../lib"
sys.path.append(libdir)

import lacuna as lac

glc = lac.clients.Member(
    config_file = bindir + "/../../etc/lacuna.cfg",
    #config_section = 'my_sitter',
    config_section = 'play_test',
)
my_planet   = glc.get_body_byname( 'bmots rof 2.1' )
tpark       = my_planet.get_building_coords( 3, -3 )


### View themepark
###
view = tpark.view()
print( view.can_operate )
print( view.reason )
print( view.food_type_count )

### Start the tpark for an hour.
###
#view = tpark.operate()
#print( view.can_operate )
#print( view.reason )
#print( view.food_type_count )

