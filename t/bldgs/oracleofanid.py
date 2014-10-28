
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
my_planet   = glc.get_body_byname( 'bmots rof 1.1' )
ora         = my_planet.get_building_coords( -3, -2 )


### See what stars we have probed
###
#star_list = ora.get_probed_stars( {'page_number': 1} )
#print("Stars probed by this oracle:")
#for s in star_list:
#    print( s.name )


### Get info on a single probed star
### 
### This example is a little ridiculous.  Normally you won't call 
### get_probed_stars() immediately followed by get_probed_star().  We're doing 
### it this way here just so we can get the star ID to pass off to get_star().
#star_list = ora.get_probed_stars( {'page_number': 1} )
#id = star_list[0].id
#star = ora.get_star( id )
#print( "Bodies orbiting", star.name, ":" )
#for b in star.bodies:
#    print( "\t", b.name );


