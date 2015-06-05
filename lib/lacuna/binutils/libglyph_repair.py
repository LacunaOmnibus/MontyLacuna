
import lacuna, lacuna.binutils.libbin
import argparse, os, sys

class GlyphRepair(lacuna.binutils.libbin.Script):

    def __init__(self):
        self.version = '0.1'
        self.glyphs = [
            "algaepond", "amalgusmeadow", "beeldebannest", "blackholegenerator", "citadelofknope",
            "crashedshipsite", "dentonbrambles", "geothermalvent", "gratchsgauntlet",
            "interdimensionalrift", "kalavianruins", "lapisforest", "libraryofjith", "malcudfield",
            "naturalspring", "oracleofanid", "pantheonofhagness", "templeofthedrajilites",
            "thedillonforge", "volcano"
        ]
        parser = argparse.ArgumentParser(
            description = 'Repair all damaged glyph buildings.',
            epilog      = 'Full docs can be found at http://tmtowtdi.github.io/MontyLacuna/scripts/glyph_repair.html',
        )
        parser.add_argument( 'name', 
            metavar     = '<planet>',
            action      = 'store',
            help        = 'All glyph (permanent) buildings on this planet will be repaired if damaged.'
        )
        parser.add_argument( 'fresh', 
            action      = 'store',
            help        = 'Clears the cache to ensure fresh data.'
        )
        self.damaged    = {}    # squishname => id
        self.ute        = lacuna.utils.Utils()

        if self.args.fresh:
            self.client.cache_clear("my_planets")
        self.client.cache_on("my_planets", 3600)
        super().__init__(parser)
        self.set_planets()

    def find_damage( self ):
        """ Checks if the current planet has damaged glyph buildings.

        You **MUST** call ``set_current_planet`` before calling this.

        Returns:
            num (int): The number of damaged glyph buildings.
        """
        for bldg_name in self.planet.buildings_name.keys():
            squishname = self.ute.squish(bldg_name, True)
            if squishname in self.glyphs:
                bldgs = self.planet.buildings_name[ bldg_name ]
                for b in bldgs:
                    if b['efficiency'] != '100':
                        self.damaged[squishname] = b['id']
        return len(self.damaged)

    def do_repairs( self ):
        """ Repairs all glyph buildings found to be damaged on the current planet.

        You **MUST** call ``set_current_planet`` before calling this.
        """
        ### Since we're changed state, clear the cache.
        self.client.cache_clear("my_planets")

        for classname in self.damaged.keys():
            self.client.user_logger.debug("Getting {}...".format(classname))
            bldg = self.planet.get_building_id( classname, self.damaged[classname] )
            if int(bldg.efficiency) < 100:
                bldg.repair()
                self.client.user_logger.info("{} has been repaired.".format(classname))
            else:
                self.client.user_logger.debug("{} was listed as damaged, but isn't.".format(classname))

    def set_current_planet( self, pname ):
        self.planet     = self.client.get_body_byname( pname )
        self.damaged    = {}

