
import lacuna, lacuna.binutils.libbin, lacuna.types
import argparse, os, sys

class BuildShips(lacuna.binutils.libbin.Script):

    def __init__(self):
        self.version = '0.1'
        parser = argparse.ArgumentParser(
            description = 'This will build as many of a single type of ship as you want, up to the maximum that can be built across all shipyards on your planet.  If there are already ships in your build queue, this will figure that out and only build what it can.',
            epilog      = "Full docs can be found at http://tmtowtdi.github.io/MontyLacuna/scripts/build_ships.html",
        )
        parser.add_argument( 'name', 
            metavar     = '<planet>',
            action      = 'store',
            help        = 'Name of planet on which to build ships.'
        )
        parser.add_argument( 'type', 
            metavar     = '<shiptype>',
            action      = 'store',
            help        = "Type of ship to build.  Most commonly-used names will work.  See the online docs for types.Translator for specifics."
        )
        parser.add_argument( '--num', 
            metavar     = '<count>',
            action      = 'store',
            type        = int,
            default     = 0,
            help        = "Number of ships to build.  Defaults to 'fill up all available build queue slots'.  If you request more ships than your shipyards can queue, as many as possible will be built."
        )
        parser.add_argument( '--level', 
            metavar     = '<lvl>',
            dest        = 'min_lvl',
            action      = 'store',
            type        = int,
            default     = 1,
            help        = 'Minimum shipyard level to use for building.  Defaults to 1.'
        )
        parser.add_argument( '--topoff', 
            dest        = 'topoff',
            action      = 'store_true',
            help        = "If --topoff is sent, instead of building --num new ships, we'll make sure that we have at least --num ships in stock."
        )
        super().__init__(parser)

        self.client.cache_on( 'my_colonies', 3600 )
        self.planets = []
        if self.args.name == 'all':
            for colname in self.client.empire.colony_names.keys():
                self.planets.append(colname)
        else:
            self.planets = [ self.args.name ]
        self.client.cache_off()

        self.trans = lacuna.types.Translator()
        self.shiptype = self.trans.translate_shiptype( self.args.type )

    def set_planet( self, pname:str ):
        self.planet = self.client.get_body_byname( pname )

    def get_shipyards( self ):
        yards = self.planet.get_buildings_bytype( 'shipyard', self.args.min_lvl )
        if not yards:
            raise RuntimeError("You don't have any shipyards of the required level.")
        return( yards )


    def determine_buildable(self, yards):
        """ Ensures we can actually build the requested ship type, and figures 
        out how many of them we should build.

        Arguments:
            - yards -- list of lacuna.building.shipyard.shipyard objects

        Returns the number of ships we should queue across all shipyards.

        This number to be built does not take current build queues into 
        account.  Four level 30 SYs are going to return 120, no matter what 
        those SYs are currently doing.

        Raises KeyError if the shiptype isn't buildable for whatever reason.
        """
        ships, docks_avail, build_queue_max, build_queue_used = yards[0].get_buildable()
        if not docks_avail:
            raise KeyError("You don't have any docks available to hold more ships.")
        if not build_queue_max:
            raise KeyError("All of your build queue slots are occupied.")
        if not len([ i for i in ships if i.type == self.shiptype ]):
            raise KeyError( "The type of ship requested, {}, cannot be built.".format(self.args.type) )

        ### If the 'num to build' arg is 0, that means "build max"
        requested_num = self.args.num if self.args.num > 0 else build_queue_max
        ### If we were asked to build more than we can, back off to just 
        ### building what we can.
        num_to_build = requested_num    if requested_num < build_queue_max      else build_queue_max

        if docks_avail < requested_num:
            if docks_avail < build_queue_max:
                num_to_build = docks_avail
            else:
                num_to_build = build_queue_max
        elif build_queue_max < requested_num:
            if docks_avail < build_queue_max:
                num_to_build = docks_avail
            else:
                num_to_build = build_queue_max
        else:
            num_to_build = requested_num

        if self.args.topoff:
            old_cache = self.client.cache_off() # be sure this is off.
            sp = self.planet.get_buildings_bytype( 'spaceport', self.args.min_lvl, 1, 100 )[0]

            currently_in_stock = 0
            docked_ships, docks_avail, docks_max = sp.view()
            if self.shiptype in docked_ships:
                currently_in_stock = docked_ships[self.shiptype]

            if currently_in_stock >= requested_num:
                self.client.user_logger.info( "You already have {} {}s built, no need to top off."
                    .format(currently_in_stock, self.args.type)
                )
                num_to_build = 0
            topoff_num = (requested_num - currently_in_stock)
            if topoff_num > num_to_build:
                self.client.user_logger.info( "We should build {} more ships to top off, but only have slots for {} more."
                    .format(topoff_num, num_to_build)
                )
            else:
                num_to_build = topoff_num
        return num_to_build

