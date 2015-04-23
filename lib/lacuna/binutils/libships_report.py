
import lacuna, lacuna.binutils.libbin
import argparse, csv, os, sys

class PlanetShipData():
    """ Contains the data gathered on ships living at a single planet.
    """
    def __init__(self, pname, docked_ships, ships_detail, docks_avail, docks_ttl):
        self.pname          = pname
        self.docked_ships   = docked_ships     # Dict -- type: number
        self.ships_detail   = ships_detail      # list of ExistingShip objects
        self.docks_avail    = docks_avail
        self.docks_ttl      = docks_ttl

    def display_report( self, sr ):
        if sr.args.format == 'csv':
            self.display_csv_report( sr )
        else:
            self.display_cli_report()

    def display_cli_report( self ):
        """ Displays a human-readable report on the ships on a single planet on 
        the terminal.
        """
        print( "{} has {:,} of {:,} docks available.".format(self.pname, self.docks_avail, self.docks_ttl) )
        print( "Displaying currently-docked ships.  (Try CSV format for a complete report.)" )
        for type in sorted( self.docked_ships ):
            print( "\t{:<30} {: >6,}".format(type, self.docked_ships[type]) )
        print( '' )

    def display_csv_report( self, sr ):
        """ Displays a CSV report on the ships on a single planet on the terminal.
        """
        writer = csv.writer( sys.stdout ) 

        if not sr.header_written:
            row = [ "Planet Name", "ID", "Name", "Type", "Task", "Speed", "Hold Size", 
                "Berth Level", "Date Available", "Max Occupants", "Destination" ]
            writer.writerow( row )
            sr.header_written = True

        for s in self.ships_detail:
            row = [ self.pname, s.id, s.name, s.type, s.task, s. speed, s.hold_size, 
                s.berth_level, s.date_available, s.max_occupants, ]
            if hasattr(s, "to"):
                row.append( s.to.name )
            else:
                row.append( '' )
            writer.writerow( row )
        

class ShipsReport(lacuna.binutils.libbin.Script):
    """ Gather and report on ship data by planet.
    """

    def __init__(self):
        self.version = '0.1'
        parser = argparse.ArgumentParser(
            description = 'Displays a report on built ships.',
            epilog      = "Full docs can be found at http://tmtowtdi.github.io/MontyLacuna/scripts/ships_report.html",
        )
        parser.add_argument( 'name', 
            metavar     = '<planet>',
            action      = 'store',
            help        = "Produce report on ships at this planet.  'all' to report on all planets."
        )
        parser.add_argument( '--fresh', 
            action      = 'store_true',
            help        = "Ship data is cached so you can run the report multiple times, quickly.  But if you run it once, then go build ships and want a new report that includes those ships, you'll want fresh, not cached data.  In that case, pass this option on the second run."
        )
        parser.add_argument( '--format', 
            metavar     = '<format>',
            action      = 'store',
            choices     = [ 'cli', 'csv' ],
            default     = 'cli',
            help        = "What format do you want your output?  Choices include 'cli' and 'csv'.  Defaults to 'cli'."
        )
        parser.add_argument( '--tag', 
            metavar     = '<tag>',
            dest        = 'tags',
            action      = 'append',
            choices     = [ 'Colonization', 'Exploration', 'Intelligence', 'Mining', 'Trade', 'War' ],
            type        = str,
            default     = [],
            help        = "Report on ships with this tag.  Omit to report on all tags.  Valid tags are: 'Colonization', 'Exploration', 'Intelligence', 'Mining', 'Trade', 'War'."
        )
        super().__init__(parser)

        self.header_written = False
        self.planet         = ''
        self.planets        = []
        self.port           = ''
        self.ship_data      = {}    # planet_id => PlanetShipData object
        if self.args.fresh:
            self.client.cache_clear( 'ships_report' )
        self.set_planets()


    def _set_spaceport( self ):
        """ Finds a spaceport on the current planet.  Must be called after set_planet()
        """
        self.port = self.planet.get_buildings_bytype( 'spaceport', 1, 1, 100 )[0]
        if not self.port:
            raise RuntimeError("You don't have any working space ports!.")

    def set_planet( self, pname:str ):
        """ Meant to be called by the user to set which planet we're working on 
        right now.

        Arguments:
            - pname -- String name of the planet
        """
        self.client.cache_on( 'my_colonies', 3600 )
        self.planet = self.client.get_body_byname( pname )
        self._set_spaceport()
        self.client.cache_off()

    def gather_ship_data( self ):
        """ Get data on all of the ships at our planet that have the 
        requested tag, or all ships if no tag was passed.
        """
        self.client.cache_on( 'ships_report', 3600 )

        ### We need both of these calls.  view_all_ships() gives (oddly 
        ### enough) all ships.  view() just gives numbers on docked ships, 
        ### which is close enough for the summary view.
        paging = { 'no_paging': 1 }
        ships_detail, num = self.port.view_all_ships(paging)    
        docked_ships, docks_avail, docks_ttl = self.port.view()

        self.ship_data[ self.planet.name ] = PlanetShipData( self.planet.name, docked_ships, ships_detail, docks_avail, docks_ttl )
        self.client.cache_off()

    def display_full_report( self ):
        """ Displays the report on whatever planet or planets was specified by 
        the user.
        """
        for pname in sorted( self.ship_data.keys() ):
            self.ship_data[pname].display_report( self )

