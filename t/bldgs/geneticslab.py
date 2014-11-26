
import os, sys
bindir = os.path.abspath(os.path.dirname(sys.argv[0]))
libdir = bindir + "/../../lib"
sys.path.append(libdir)

import lacuna as lac
from lacuna.exceptions import CaptchaResponseError

glc = lac.clients.Member(
    config_file = bindir + "/../../etc/lacuna.cfg",
    config_section = 'play_test',
    #config_section = 'sitter',
)
my_planet   = glc.get_body_byname( 'bmots rof 1.4' )
gen         = my_planet.get_buildings_bytype( 'geneticslab', 0, 1 )[0]


### Prepare for experimentation
### 
grafts, s_odds, g_odds, cost, can = gen.prepare_experiment()
if can:
    print( "I have {:,}% chance of grafting, and prisoners have {:,}% chance of surviving.  {:,} E per attempt."
        .format(g_odds, s_odds, cost))
else:
    print( "I'm currently unable to run any experiments." )
###
### Requires you have 2 prisoners with at least 2 graftable affinities on the 
### second one. 
###
### This test is a bit contrived; IRL you shouldn't need to be messing with 
### the eval() - you'll know what affinity you're attempting to graft.
###
for g in grafts:
    random_affin = g.graftable_affinities[0]
    print( "I can graft {} from spy {}.  His score is {}."
        .format( random_affin, g.spy.name, eval("g.species."+random_affin) )
    )


### Perform an experiment
### If you test this here, then look back at your browser, the profile screen 
### will probably not update even if the experiment here succeeded.  Refresh 
### your browser; the change took, it's just not being displayed.
###
#grafts, s_odds, g_odds, cost, can = gen.prepare_experiment()
#exp = gen.run_experiment( grafts[0]['spy'].id, 'research_affinity' )
#survive_text = "did" if exp.survive else "did not"
#graft_text = "did" if exp.graft else "did not"
#print( "The graft {} succeed, and the prisoner {} survive.  The reason listed is:"
#    .format(graft_text, survive_text)
#)
#print( "\t", exp.message )


### Rename your species
### Like with performing an experiment, the browser won't update after this 
### test.  Log out, reload your browser, then log back in.
###
#new_legal_species = {
#    "name": "Grundle foobar",
#    "description": "This is my shiny new and totally valid and legal description."
#}
#new_illegal_species = {
#    "name": "This string is way too long to be a valid species name",
#    "description": "This description contains < and >, which are both illegal."
#}
### 
### Pick one.  The 'new_illegal_species' one will raise an exception.
###
#rv = gen.rename_species( new_legal_species )
#rv = gen.rename_species( new_illegal_species )
#if rv:
#    print( "Your species has been renamed." )
#else:
#    print( "The attempt to rename your species failed.  No explanation given." )

