
import os, sys
bindir = os.path.abspath(os.path.dirname(sys.argv[0]))
libdir = bindir + "/../../lib"
sys.path.append(libdir)

import lacuna as lac

glc = lac.clients.Member(
    config_file = bindir + "/../../etc/lacuna.cfg",
    config_section = 'sitter',
)

my_planet = glc.get_body_byname( 'bmots01' )
arch = my_planet.get_buildings_bytype( 'archaeology', 0, 1 )[0]



### Is the archmin performing a local search right now?
###
#rv = arch.view()
#if hasattr(arch, 'work'):
#    print( "Arch min is searching for {} now; that will complete at {}."
#        .format(arch.work['searching'], arch.work['end'])
#    )
#else:
#    print( "Arch min is not searching now." )


### Search through an ore type for a glyph.
### Requires that you have at least 10,000 of ore_type in stock.
###
#ore_type = 'rutile'
#arch.search_for_glyph( ore_type )
#print( "Arch min is now searching for a {} glyph.".format(ore_type) )


### Spend 2 E to subsidize the current search.  Raises a ServerError exception 
### if no search is happening right now.
###
### CAUTION - if you have a search going on, this will spend 2 E.
###
#arch.subsidize_search()
#print( "I just spent 2E to subsidize the current glyph search." )


### Get lists of available glyphs
### Deprecated call; don't use this.
###
#arch.get_glyphs()

### This is current; use this instead of get_glyphs().
###
#glyphs = arch.get_glyph_summary()
#for g in glyphs:
#    print( "Glyph {} has ID {}, and we have {} of them."
#        .format(g.name, g.id, g.quantity)
#    )


### Assemble glyph recipes
###
#halls_recipe_1 = ['goethite', 'halite', 'gypsum', 'trona']
#a = arch.assemble_glyphs( halls_recipe_1, 3 )
#print( "I just assembled {} of {}".format(a.quantity, a.item_name) )


### Get available ores
###
#ores = arch.get_ores_available_for_processing()
#for name, quantity in ores.my_ores():
#    print( "I have {:,} of {}".format(quantity, name) )


### Get info on working excavators
###
#excavs, max, trav = arch.view_excavators()
#print( "We have {} excavs working, and {} are in the air.  We max out at {:,}."
#    .format(len(excavs), trav, max)
#)
#e = excavs[0]
#print( "Our first listed excav got to {} on {}, and has a {}% chance of finding a glyph."
#    .format(e.body.name, e.date_landed, e.glyph)
#)


### Abandon existing excavator
### BE CAREFUL WITH THIS
#arch.abandon_excavator( integer excavator site ID from the view_excavators() call above )

