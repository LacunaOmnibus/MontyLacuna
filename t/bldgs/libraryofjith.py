
import os, sys
bindir = os.path.abspath(os.path.dirname(__file__))
libdir = bindir + "/../../lib"
sys.path.append(libdir)

import lacuna as lac

glc = lac.clients.Member(
    config_file = bindir + "/../../etc/lacuna.cfg",
    config_section = 'my_sitter',
    #config_section = 'play_test',
)
my_planet   = glc.get_body_byname( 'bmots rof 2.6' )
lib         = my_planet.get_building_coords( -2, 1 )


### Get information on a specific empire's species
###
empire_to_research = 'tmtowtdi'

### First, find that empire's ID:
stats = glc.get_stats()
emps = stats.find_empire_rank( '', empire_to_research )
emp = ''
for i in emps:
    if i.empire_name == empire_to_research:
        emp = i
if not emp:
    raise AttributeError("Could not find the desired empire.")
print( "The ID of the empire you're looking for is:", emp.empire_id )
quit()

### Now that we have the desired empire ID, we can check its species.
species = lib.research_species( emp.empire_id )
print( "The species {} is described as '{}' and can inhabit orbits {} - {}."
    .format(species.name, species.description, species.min_orbit, species.max_orbit)
)


