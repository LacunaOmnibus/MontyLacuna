
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

my_planet = glc.get_body_byname( 'bmots rof 2.1' )
arch = my_planet.get_building_coords( -5, -5 )


### Is the archmin performing a local search right now?
###
#rv = arch.view()
#if hasattr(arch, 'work'):
#    print( "Arch min is searching for {} now; that will complete at {}."
#        .format(arch.work['searching'], arch.work['end'])
#    )
#else:
#    print( "Arch min is not searching now." )



### Get lists of available glyphs
###
### Deprecated call; don't use this.
#arch.get_glyphs()

### This is current; use this instead of get_glyphs().
glyphs = arch.get_glyph_summary()
for g in glyphs:
    print( "Glyph {} has ID {}, and we have {} of them."
        .format(g.name, g.id, g.quantity)
    )


### Assemble glyph recipes
###
#halls_recipe_1 = ['goethite', 'halite', 'gypsum', 'trona']
#arch.assemble_glyphs( halls_recipe_1, 3 )
### 
#bad_recipe = ['goethite', 'halite', 'trona', 'gypsum']     # the order is invalid here
#rvd = arch.assemble_glyphs( bad_recipe )                   # So this raises 1002


### Get available ores
###
#rv = arch.get_ores_available_for_processing()
#for ore, quantity in rv['ore'].items():
#    print( "We have {} of {}." .format(quantity, ore) )


### Get info on working excavators
###
#excavs, max, trav = arch.view_excavators()
#print( "We have {} excavs working, and {} are in the air.  We max out at {}."
#    .format(len(excavs), trav, max)
#)
#e = excavs[0]
#print( "Our first listed excav got to {} on {}, and has a {}% chance of finding a glyph."
#    .format(e.body.name, e.date_landed, e.glyph)
#)


### Abandon existing excavator
### BE CAREFUL WITH THIS
#arch.abandon_excavator( integer excavator site ID from the view_excavators() call above )

