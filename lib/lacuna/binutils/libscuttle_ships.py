
import lacuna, lacuna.binutils.libbin, lacuna.types
import lacuna.exceptions as err
import argparse, operator, os, sys

class ScuttleShips(lacuna.binutils.libbin.Script):
    def __init__(self):
        self.version = '0.1'
        parser = argparse.ArgumentParser(
            description = 'Scuttles ships at a specific planet.',
            epilog      = "Full docs can be found at http://tmtowtdi.github.io/MontyLacuna/scripts/scuttle_ships.html",
        )
        parser.add_argument( 'name', 
            metavar     = '<planet>',
            action      = 'store',
            help        = 'Name of the planet on which to scuttle ships.'
        )
        parser.add_argument( 'type', 
            metavar     = '<shiptype>',
            action      = 'store',
            help        = "Type of ship to scuttle.  Must translate to a TLE 'system' ship name, but most commonly-use names will be correctly translated (eg 'srcs' works for 'short_range_colony_ship').  See the online docs for a complete list."
        )
        parser.add_argument( '--low', 
            metavar     = '<attribute>',
            action      = 'store',
            choices     = [ 'combat', 'hold_size', 'max_occupants', 'speed', 'stealth',  ],
            default     = 'speed',
            help        = "Ships with the lowest score in this attribute will be scuttled first.  Defaults to 'speed'."
        )
        parser.add_argument( '--num', 
            metavar     = '<count>',
            action      = 'store',
            type        = int,
            default     = 1,
            help        = "Number of ships to scuttle.  Defaults to 1."
        )
        super().__init__(parser)

        self.client.user_logger.debug( "Setting {} as the working planet.".format(self.args.name) )
        self._set_planet( self.args.name )
        self.client.user_logger.debug( "Finding a spaceport on {}.".format(self.planet.name) )
        self._set_spaceport()

        self.trans = lacuna.types.Translator()
        self.shiptype = self.trans.translate_shiptype( self.args.type )


    def _set_planet( self, pname:str ):
        self.planet = self.client.get_body_byname( pname )


    def _set_spaceport( self ):
        self.client.cache_on( 'my_colonies', 3600 )
        self.port = self.planet.get_buildings_bytype( 'spaceport', 1, 1, 100 )[0]
        self.client.cache_off()
        if not self.port:
            raise RuntimeError("You don't have any shipyards of the required level.")


    def scuttle( self ):
        """ Scuttles the specified number of the requested ship type.  If we 
        don't have as many as were specified, scuttles them all.

        Returns the integer number of ships scuttled.
        """
        self.client.cache_on( 'ships_report', 3600 )
        paging = { "no_paging": 1 }
        filter = { "type": self.shiptype }
        ships, num = self.port.view_all_ships( paging, filter )
        self.client.cache_off()

        ids_to_scuttle = [ p.id for p in sorted(ships, key=operator.attrgetter(self.args.low)) if p.task == 'Docked' ][0:self.args.num]
        if ids_to_scuttle:
            self.port.mass_scuttle_ship( ids_to_scuttle ) 
            self.client.cache_clear( 'ships_report' )
        return len(ids_to_scuttle)

