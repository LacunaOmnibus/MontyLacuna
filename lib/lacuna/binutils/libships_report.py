
### HERE is where I left off

import lacuna, lacuna.binutils.libbin
import argparse, os, sys

class PlanetShipData():
    """ Contains the data gathered on ships living at a single planet
    """
    pass

class ShipsReport(lacuna.binutils.libbin.Script):

    def __init__(self):
        self.version = '0.1'
        parser = argparse.ArgumentParser(
            description = 'Displays a report on built ships and availability of space ports.',
            epilog      = "EXAMPLE: python bin/ships_report.py --tag War Earth",
        )
        parser.add_argument( 'name', 
            metavar     = '<planet>',
            action      = 'store',
            help        = "Produce report on ships at this planet.  'all' to report on all planets."
        )
        parser.add_argument( '--tag', 
            metavar     = '<tag>',
            action      = 'append',
            choices     = [ 'Colonization', 'Exploration', 'Intelligence', 'Mining', 'Trade', 'War' ],
            type        = str,
            default     = [],
            help        = "We'll only report on this type of ship.  Omit to report on all ship tags."
        )
        super().__init__(parser)

        self.planet     = ''
        self.planets    = []
        self.port       = ''
        self.ship_data  = {}    # planet_id => PlanetShipData object

        self.set_planets()
        self.set_spaceport()


    def set_planet( self, pname:str ):
        """ Meant to be called by the user to set which planet we're working on 
        right now.
        """
        self.planet = self.client.get_body_byname( pname )


    def set_planets( self ):
        self.client.cache_on( 'my_colonies', 3600 )
        self.planets = []
        if self.args.name == 'all':
            for colname in self.client.empire.colony_names.keys():
                self.planets.append(colname)
        else:
            self.planets = self.args.name
        self.client.cache_off()


    def set_spaceport( self ):
        self.port = self.planet.get_buildings_bytype( 'spaceport', 1, 1, 100 )
        if not self.port:
            raise RuntimeError("You don't have any working space ports!.")


    def gather_ship_data( self ):
        """ Get data on all of the ships at our spaceport that have the 
        requested tag.
        """
        pass








