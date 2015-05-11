
import lacuna, lacuna.binutils.libbin, lacuna.types
import lacuna.exceptions as err
import argparse, os, sys
import lacuna.exceptions as err

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
            help        = "If --topoff is sent, instead of building --num new ships, we'll make sure that we have at least --num ships already built."
        )
        super().__init__(parser)

        self.client.cache_on( 'my_colonies', 3600 )
        self.planets = []
        if self.args.name == 'all':
            for colname in self.client.empire.colony_names.keys():
                self.planets.append(colname)
        else:
            self.planets = [ self.abbrv.get_name(self.args.name) ]
        self.client.cache_off()

        self.trans = lacuna.types.Translator()
        self.shiptype = self.trans.translate_shiptype( self.args.type )

    def set_planet( self, pname:str ):
        self.planet = self.client.get_body_byname( pname )

    def get_shipyards( self ):
        """
        Raises err.NoSuchBuildingError if this planet doesn't have any 
        shipyards of the requested level.
        """
        yards = self.planet.get_buildings_bytype( 'shipyard', self.args.min_lvl )
        return( yards )

    def build_at_yard( self, yard, build_cnt ):
        """ Build ships at the given shipyard.

        Args:
            yard (lacuna.buildings.callable.shipyard): The shipyard to build at
            build_cnt (int): The total number of ships left to build
        Returns:
            tuple:

                - num_built (int): Number of ships being built at this SY
                - num_left (int): Number of ships that still need to be built
        """
        ships, building_now, cost   = yard.view_build_queue()
        num_to_build_here           = yard.level - building_now
        num_to_build_here           = build_cnt if build_cnt < num_to_build_here else num_to_build_here
        self.client.user_logger.debug( "About to try building {} ships." .format(num_to_build_here))
        if num_to_build_here > 0:
            try:
                yard.build_ship( self.shiptype, num_to_build_here )
            except err.ServerError as e:
                self.client.user_logger.warning( "Failed to build at this shipyard because: {}".format(e) )
                return( 0, build_cnt )
        else:
            self.client.user_logger.info( "Looks like we've added all to the queue that we can." )
        build_cnt -= num_to_build_here
        return( num_to_build_here, build_cnt )

    def determine_buildable( self, yards ):
        """ Ensures we can actually build the requested ship type, and figures 
        out how many of them we should build.

        Args:
            yards (lacuna.buildings.callable.shipyard): list of objects.
        Returns:
            numships (int): number of ships we should queue across all shipyards.
        Raises:
            KeyError: if the ship can't be built for any reason.

        This number to be built does not take current build queues into 
        account.  Four level 30 SYs are going to return 120, no matter what 
        those SYs are currently doing.
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
            num_to_build = self.get_topoff_num( requested_num, num_to_build );

        return num_to_build

    def get_topoff_num( self, req_cnt, available_slots ):
        old_cache = self.client.cache_off() # be sure this is off.
        sp = self.planet.get_buildings_bytype( 'spaceport', 1, 1, 100 )[0]

        num_to_build = 0
        paging = { 'no_paging': 1 }
        filter = { 'type': self.shiptype }
        ships, existing_ships_cnt = sp.view_all_ships( paging, filter )

        if existing_ships_cnt >= req_cnt:
            self.client.user_logger.info( "You already have {} {}s built, no need to top off."
                .format(existing_ships_cnt, self.args.type)
            )
        else:
            topoff_num = (req_cnt - existing_ships_cnt)
            if topoff_num > available_slots:
                self.client.user_logger.info( "We should build {} more ships to top off, but only have slots for {} more."
                    .format(topoff_num, available_slots)
                )
                num_to_build = available_slots
            else:
                num_to_build = topoff_num
        return num_to_build

