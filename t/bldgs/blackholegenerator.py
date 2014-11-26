
import os, sys
bindir = os.path.abspath(os.path.dirname(sys.argv[0]))
libdir = bindir + "/../../lib"
sys.path.append(libdir)

import lacuna as lac

glc = lac.clients.Member(
    config_file = bindir + "/../../etc/lacuna.cfg",
    config_section = 'play_test',
)

my_planet = glc.get_body_byname( 'bmots rof 1.3' )
bhg = my_planet.get_building_coords( 5, -3 )


### Get available actions
###
#target = { 'zone':'1|-4' }
#target = { 'body_name':'Schu Ize 2' }
#actions = bhg.get_actions_for( target )
#for a in actions:
#    print( "We have a {}% chance of failing the task of {} at a distance of {}."
#        .format(a.base_fail, a.name, a.dist)
#    )


### Subsidize cooldown
### BE CAREFUL WITH THIS - it will spend 2E to remove the BHG's cooldown.
#bhg.subsidize_cooldown()


### Perform BHG action
###

### Method 1 - Generate.    DON'T DO THIS!
###
#args = {
#    "target"        : { "body_name" : "Some Planet Name" },
#    "task_name"     : "Change Type",
#    "params"        : { "newtype" : 35 },
#    "subsidize"     : 0                                    # Danger Will Robinson!
#}
#target, side, fail = bhg.generate_singularity( args )


### Method 2 - Subsidize.   This is what you should be doing.
###
args = {
    "target"        : { "body_name" : "Schu Ize 2" },
    "task_name"     : "Change Type",
    "params"        : { "newtype" : 31 },
    "subsidize"     : 1                                     # And there was much rejoicing
}
target, side, fail = bhg.generate_singularity( args )
if hasattr(target, 'message'):
    print( "Our attempt generated the message", target.message )
if hasattr(side, 'message'):
    print( "Our side effect generated the message", side.message )
if hasattr(fail, 'message'):
    print( "Our attempt failed with the message", fail.message )

