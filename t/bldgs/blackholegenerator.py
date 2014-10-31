
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

my_planet = glc.get_body_byname( 'bmots rof 1.3' )
bhg = my_planet.get_building_coords( 5, -3 )


### Get available actions
###
#target_zone = { 'zone':'1|-4' }
#t = bhg.get_actions_for( target_zone )[0]
#print( "We have a {}% chance of failing the task of {} at a distance of {}."
#    .format(t.base_fail, t.name, t.dist)
#)


### Subsidize cooldown
### BE CAREFUL WITH THIS - it will spend 2E to remove the BHG's cooldown.
#bhg.subsidize_cooldown()


### Perform BHG action
###

### Method 1 - Generate.    DON'T DO THIS!
###
#t1 = {
#    "target"        : { "body_name" : "Some Planet Name" },
#    "task_name"     : "Change Type",
#    "params"        : { "newtype" : 35 },
#    "subsidize"     : 0                                    # Danger Will Robinson!
#}
#rvc = bhg.generate_singularity(t1)
#glc.pp.pprint( rvc )


### Method 2 - Subsidize.   This is what you should be doing.
###
t2 = {
    "target"        : { "body_name" : "Opriogee 2" },
    "task_name"     : "Change Type",
    "params"        : { "newtype" : 31 },
    "subsidize"     : 1                                     # And there was much rejoicing
}
rv = bhg.generate_singularity(t2)

#print( "Our attempt to use the BHG on {} resulted in the message '{}'." 
#    .format(rv.target['name'], rv.target['message'])
#)
#
#if hasattr(rv, 'side'):
#    print( "Our BHG usage had the side affect of {} on {}." 
#        .format(rv.side['message'], rv.side['name'])
#    )

