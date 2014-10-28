
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
sec         = my_planet.get_building_coords( -3, -1 )


### View prisoners
###
pris = sec.view_prisoners()
for i in pris:
    print( "Prisoner named {} has an ID of {}.".format(pris.name, pris.id) )


### Release a prisoner
###
#prisoners = sec.view_prisoners()
#pris = prisoners[0]
#sec.release_prisoner( pris['id'] )


### View foreign spies
### Should show the guy you just released as a result.
###
#foreign = sec.view_foreign_spies()
#for i in foreign:
#    print( "Foreign agent named {} has an ID of {}.".format(i.name, i.id) )


###
### Now go run a security sweep to grab up that loose spy.
###


### Execute a prisoner
###
#prisoners = sec.view_prisoners()
#pris = prisoners[0]
#sec.execute_prisoner( pris['id'] )


