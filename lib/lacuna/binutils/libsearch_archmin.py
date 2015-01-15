
import lacuna, lacuna.binutils.libbin, lacuna.types
import lacuna.exceptions as err
import argparse, os, sys

class SearchArchmin(lacuna.binutils.libbin.Script):

    MIN_ORE_FOR_SEARCH = 10000

    def __init__(self):
        self.version = '0.1'
        parser = argparse.ArgumentParser(
            description = 'Begins an Archaeology Ministry search for a glyph.',
            epilog      = "EXAMPLE python bin/search_archmin.py Earth bauxite",
        )
        parser.add_argument( 'name', 
            metavar     = '<planet>',
            action      = 'store',
            help        = "Name of planet on which to search.  Use 'all' to begin archmin searches on all of your planets."
        )
        parser.add_argument( 'glyph', 
            metavar     = '<glyphtype>',
            action      = 'store',
            help        = "Type of ore to search through for glyphs.  You must have at least 10,000 of this ore in storage.  If you use 'needed' as the ore type, a search will be performed for whatever glyph type you have least of."
        )
        parser.add_argument( '-l', '--list', 
            action      = 'store_true',
            help        = "Displays a list of all ores and then quits.  This overrides all other options and can be used on its own."
        )

        self.skip_argparse = {
            '-l':       self.list_ores,
            '--list':   self.list_ores,
        }

        super().__init__(parser)

        self.trans = lacuna.types.Translator()
        if self.args.glyph.lower() != 'needed':
            self.requested_glyph = self.trans.translate_oretype( self.args.glyph )

        self.planets        = []    # list (strings) of planet names
        self.glyphs         = {}    # name: quantity_on_site
        self.needed_glyph   = ''    # name of glyph we have least of
        self.ore_to_search  = ''    # name of ore to search through for glyphs
        self.ores           = {}    # name: quantity_on_site

        self.client.cache_on( 'my_colonies', 3600 )
        if self.args.name == 'all':
            for colname in sorted( self.client.empire.colony_names.keys() ):
                self.planets.append(colname)
        else:
            self.planets = [ self.args.name ]
        self.client.cache_off()

    def list_ores(self):
        ores = [
            "anthracite", "bauxite", "beryl", "chromite", "chalcopyrite",
            "fluorite", "galena", "goethite", "gold", "gypsum", "halite",
            "kerogen", "magnetite", "methane", "monazite", "rutile", "sulfur",
            "trona", "uraninite", "zircon",
        ]
        print( 'You can search for any of these ores:' )
        for i in ores:
            print( "\t", i.title() )
        quit()

    def set_planet( self, pname:str ):
        """ Sets the current working planet by name.
        
        Gets the archmin and PCC on this planet, and counts how much of each 
        ore and how many glyphs we have in storage.

        Raises :class:`lacuna.exceptions.NoSuchBuildingError` if you don't have 
        an Archaeology Ministry or PCC on the planet (although, if you don't 
        have a PCC, you probably have bigger problems than not being able to 
        perform an archmin search.)

        Raises :class:`lacuna.exceptions.WorkingError` if the planet's archmin 
        is already performing a search.

        Arguments:
            - pname -- String name of the planet.
        """
        self.planet = self.client.get_body_byname( pname )
        self.client.user_logger.debug( "Getting the archmin on {}.".format(self.planet.name) )
        self._set_archmin()
        self.client.user_logger.debug( "Getting the PCC on {}.".format(self.planet.name) )
        self._set_pcc()
        self.client.user_logger.debug( "Counting ores on {}.".format(self.planet.name) )
        self._count_ores()
        self.client.user_logger.debug( "Counting glyphs on {}.".format(self.planet.name) )
        self._count_glyphs()

    def _set_archmin( self ):
        self.archmin = self.planet.get_buildings_bytype( 'archaeology', 0, 100 )[0]
        if not self.archmin:
            raise err.NoSuchBuildingError("You don't have an Archaeology Ministry on {}.".format(self.planet.name))
        if hasattr(self.archmin, 'work'):
            raise err.WorkingError("The archmin on {} is already performing a search.".format(self.planet.name))

    def _set_pcc( self ):
        self.pcc = self.planet.get_buildings_bytype( 'planetarycommand', 0, 100 )[0]
        if not self.pcc:
            raise err.NoSuchBuildingError("You don't have a PCC on {}.".format(self.planet.name)) # Huzzuh?

    def _count_ores( self ):
        """ Count how many of each ore is available onsite.
        
        Assigns all ores in the game (not just ores we actually have > 0 of) 
        to the self.ores dict.
        """
        food, ore, planet, colony_cost = self.pcc.view()
        for o in ore.all_ores:
            if( hasattr(ore, o) ):
                self.ores[o.lower()] = getattr(ore, o)
            else:
                self.ores[o.lower()] = 0

    def _count_glyphs( self ):
        """ Count how many of each glyph is available onsite.
        
        Must be called after _count_ores().

        Assigns all glyphs in the game (not just glyphs we actually have > 0 of) 
        to the self.glyphs dict.  Also populates the 'needed_glyph' attribute 
        with the name of whatever glyph we have least of.
        """
        glyphs = self.archmin.get_glyph_summary()
        for g in glyphs:
            self.glyphs[ g.name.lower() ] = g.quantity
            if not self.needed_glyph or g.quantity < self.glyphs[ self.needed_glyph ]:
                if self.ores[g.name.lower()] >= self.MIN_ORE_FOR_SEARCH:
                    self.needed_glyph = g.name

        ### Backfill any glyphs we haven't got onsite
        for o in self.ores:
            if o not in self.glyphs:
                self.glyphs[o] = 0
                if self.ores[o] >= self.MIN_ORE_FOR_SEARCH:
                    self.needed_glyph = o

    def validate_ore( self ):
        """ Figures out which ore we should be searching through, and ensures 
        that we have enough of that ore to perform a search.

        Sets self.ore_to_search if successful.  Raises 
        :class:`lacuna.exceptions.InsufficientResourceError` if there's not 
        enough ore onsite to perform a search.
        """
        if self.args.glyph == 'needed':
            if not self.needed_glyph:
                raise err.InsufficientResourceError("You don't have enough of any ore to perform an archmin search.")
            else:
                self.ore_to_search = self.needed_glyph
        else:
            if self.ores[ self.requested_glyph ] < self.MIN_ORE_FOR_SEARCH:
                raise err.InsufficientResourceError("You don't have enough {} ore to perform an archmin search."
                    .format(self.requested_glyph)
                )
            else:
                self.ore_to_search = self.requested_glyph

    def search_for_glyph( self ):
        """ Begins a search in the archmin for whatever glyph type was 
        determined by validate_ore() to be the one to search.
        """
        self.archmin.search_for_glyph( self.ore_to_search )


