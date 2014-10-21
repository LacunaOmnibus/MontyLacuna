
import os, sys
bindir = os.path.abspath(os.path.dirname(__file__))
libdir = bindir + "/../../lib"
sys.path.append(libdir)

import lacuna as lac

glc = lac.clients.Member(
    config_file = bindir + "/../../etc/lacuna.cfg",
    config_section = 'my_sitter',
)

my_planet = glc.get_body_byname( 'bmots rof 2.6' )
bhg = my_planet.get_building_coords( 5, -3 )


### Get available actions
###
#target_zone = { 'zone':'1|-4' }
#rva = bhg.get_actions_for( target_zone )
#glc.pp.pprint( rva['tasks'] )


### Subsidize cooldown
### BE CAREFUL WITH THIS - it will spend 2E to remove the BHG's cooldown.
#rvb = bhg.subsidize_cooldown()
#glc.pp.pprint( rvb )


### Perform BHG action
### BE CAREFUL WITH THESE
###
### Method 1 - Generate.
### This is highly not recommended!
#t1 = {
#    "target"        : { "body_name" : "Some Planet Name" },
#    "task_name"     : "Change Type",
#    "params"        : { "newtype" : 35 },
#    "subsidize"     : 0                        # Danger Will Robinson!
#}
#rvc = bhg.generate_singularity(t1)
#glc.pp.pprint( rvc )

### Method 2 - Subsidize.
### This is what you should be doing.
#t2 = {
#    "target"        : { "body_name" : "Some Planet Name" },
#    "task_name"     : "Change Type",
#    "params"        : { "newtype" : 35 },
#    "subsidize"     : 1                         # And there was much rejoicing
#}
#rvc = bhg.generate_singularity(t2)
#glc.pp.pprint( rvc )

