
import os, sys
bindir = os.path.abspath(os.path.dirname(__file__))
libdir = bindir + "/../../lib"
sys.path.append(libdir)

import lacuna as lac

glc = lac.clients.Member(
    config_file = bindir + "/../../etc/lacuna.cfg",
    config_section = 'my_sitter',
)

my_planet = glc.get_body_byname( 'bmots rof 2.1' )
arch = my_planet.get_building_coords( -5, -5 )


### Get lists of available glyphs
###
### Deprecated call; don't use this.
#rva = arch.get_glyphs()
#glc.pp.pprint( rva['glyphs'] )
#print("------------")

### This is current; use this instead of get_glyphs().
#rvb = arch.get_glyph_summary()
#glc.pp.pprint( rvb['glyphs'] )
#print("------------")


### Assemble glyph recipes
###
#halls1 = ['goethite', 'halite', 'gypsum', 'trona']

#rvc = arch.assemble_glyphs( halls1 )
### Or, specify quantity:
#rvc = arch.assemble_glyphs( halls1, 3 )

#glc.pp.pprint( rvc )

#bad_recipe = ['goethite', 'halite', 'trona', 'gypsum']     # the order is invalid here
#rvd = arch.assemble_glyphs( bad_recipe )                   # So this raises 1002


### Get available ores
###
#rve = arch.get_ores_available_for_processing()
#glc.pp.pprint( rve )


### Get excavator list
###
#rvf = arch.view_excavators()
#glc.pp.pprint( rvf['excavators'] )
#glc.pp.pprint( rvf['excavators'][1] )


### Abandon existing excavator
### BE CAREFUL WITH THIS
#rvg = arch.abandon_excavator( integer excavator site ID from the view_excavators() call above )
#glc.pp.pprint( rvg )

