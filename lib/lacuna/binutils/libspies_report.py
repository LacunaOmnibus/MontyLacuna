
import lacuna, lacuna.binutils.libbin
import lacuna.exceptions as err
import argparse, csv, os, sys

class PlanetSpyData():
    """ Contains the data gathered on spies homed from a single planet.
    """
    def __init__(self, pname, spies):
        self.pname  = pname
        self.spies  = spies

    def _organize_counts( self ):
        self.a_counts = {}  # assignments
        self.l_counts = {}  # locations
        for s in self.spies:
            if s.assignment in self.a_counts:
                self.a_counts[ s.assignment ] += 1
            else:
                self.a_counts[ s.assignment ] = 1

            lkey = self._loc_key( s )
            if lkey in self.l_counts:
                self.l_counts[ lkey ] += 1
            else:
                self.l_counts[ lkey ] = 1

    def _loc_key(self, spy):
        ### Be sure name is at the end so that's the bit that gets summarized 
        ### if necessary.
        return "{: <7} ({: >5},{: >5}) - {}".format(    spy.assigned_to.id, 
                                                        spy.assigned_to.x, spy.assigned_to.y,
                                                        spy.assigned_to.name                    )

    def display_report( self, sr ):
        """ Displays the report requested by the user, either cli or csv 
        format, depending upon the command-line option.
        """
        if sr.args.format == 'csv':
            self.display_csv_report( sr )
        else:
            self.display_cli_report()

    def display_cli_report( self ):
        """ Displays a human-readable report on the spies homed from a single 
        planet on the terminal.
        """
        self._organize_counts()
        r_width = 70
        leader  = " "*2
        w       = str( r_width - len(leader) - len(leader) - 3)
        print( self.pname )
        print( "-"*len(self.pname) )
        print( "{}Assignments:".format(leader) )
        for assignment in sorted( self.a_counts.keys() ):
            tmpl = "{0}{0}{1:<" + w + "} {2: >3}"
            print(  tmpl.format(leader, assignment, self.a_counts[assignment]) )
        print( "{}Locations:".format(leader) )
        for location in sorted( self.l_counts.keys() ):
            tmpl = "{0}{0}{1:<" + w + "} {2: >3}"
            print( tmpl.format(leader, self.summarize(location, int(w)), self.l_counts[location]) )
        print( '' )

    def summarize( self, string:str, mymax:int ):
        """ If a string is too long, shortens it and adds ellipsis.

        Arguments:
            - string -- Some string to summarize
            - max -- Integer max length of the string.  Must be greater than 3.

        If the string is "abcdefghijk" and the max is 6, this will return 
        "abc..."

        Returns the summarized string, or the original string if it was shorter 
        than max.
        """
        mymax = 4 if mymax < 4 else mymax
        if len(string) > mymax:
            submax = mymax - 3
            string = string[0:submax] + "..."
        return string
        
    def display_csv_report( self, sr ):
        """ Displays a CSV report on the ships on a single planet on the terminal.
        """
        writer = csv.writer( sys.stdout ) 

        if not sr.header_written:
            row = [ "ID", "Name", "Home Planet Name", "Assignment", "Level", "Politics", "Mayhem",
                "Theft", "Intel", "Offense", "Defense", "Available On", "Seconds Remaining",
                "Location Planet ID", "Location Planet Name", "Location Planet X", "Location Planet Y",     ]
            writer.writerow( row )
            sr.header_written = True

        for s in self.spies:
            row = [ s.id, s.name, s.based_from.name, s.assignment, s.level, s.politics, s.mayhem,
                s.theft, s.intel, s.offense_rating, s.defense_rating, s.available_on, s.seconds_remaining,
                s.assigned_to.id, s.assigned_to.name, s.assigned_to.x, s.assigned_to.y,     ]
            if hasattr(s, "to"):
                row.append( s.to.name )
            else:
                row.append( '' )
            writer.writerow( row )
        

class SpiesReport(lacuna.binutils.libbin.Script):
    """ Gather and report on spy data by planet.
    """

    def __init__(self):
        self.version = '0.1'
        parser = argparse.ArgumentParser(
            description = 'Displays a report on spies.',
            epilog      = "EXAMPLE: python bin/spies_report.py Earth",
        )
        parser.add_argument( 'name', 
            metavar     = '<planet>',
            action      = 'store',
            help        = "Produce report on spies at this planet.  'all' to report on all planets."
        )
        parser.add_argument( '--fresh', 
            action      = 'store_true',
            help        = "Spy data is cached so you can run the report multiple times, quickly.  But if you run it once, then go assign or train spies and want a new report that includes those spies, you'll want fresh, not cached data.  In that case, pass this option on the second run."
        )
        parser.add_argument( '--format', 
            metavar     = '<format>',
            action      = 'store',
            choices     = [ 'cli', 'csv' ],
            default     = 'cli',
            help        = "What format do you want your output?  Choices include 'cli' and 'csv'.  Defaults to 'cli'."
        )
        super().__init__(parser)

        self.header_written = False
        self.planet         = ''
        self.intmin         = ''
        self.planets        = []
        self.spy_data       = {}    # planet_id => PlanetSpyData object

        if self.args.fresh:
            self.client.cache_clear( 'spies' )

        self._set_planets()

    def _set_planets( self ):
        self.client.cache_on( 'my_colonies', 3600 )
        self.planets = []
        if self.args.name == 'all':
            for colname in sorted( self.client.empire.colony_names.keys() ):
                self.planets.append(colname)
        else:
            self.planets = [self.args.name]
        self.client.cache_off()

    def set_planet( self, pname:str ):
        """ Meant to be called by the user to set which planet we're working on 
        right now.

        Arguments:
            - pname -- String name of the planet

        Raises :class:`lacuna.exceptions.NoSuchBuildingError` if the planet 
        being set does not have a working Intelligence Ministry.
        """
        self.client.cache_on( 'my_colonies', 3600 )
        self.planet = self.client.get_body_byname( pname )
        self._set_intmin()
        self.client.cache_off()

    def _set_intmin( self ):
        """ Finds the Intelligence Ministry on the current planet.  Must be 
        called after set_planet()

        Raises :class:`lacuna.exceptions.NoSuchBuildingError` if the planet 
        being set does not have a working Intelligence Ministry.
        """
        self.intmin = self.planet.get_buildings_bytype( 'intelligence', 1, 1, 100 )[0]

    def gather_spy_data( self ):
        """ Get data on all of the spies at our planet.  Must be called after 
        :meth:`lacuna.binutils.libspies_report.SpiesReport.set_planet`.
        """
        self.client.cache_on( 'spies', 3600 )
        spies = self.intmin.view_all_spies()
        self.spy_data[ self.planet.name ] = PlanetSpyData( self.planet.name, spies )
        self.client.cache_off()

    def display_full_report( self ):
        """ Displays the report on whatever planet or planets was specified by 
        the user.  Must be called after
        :meth:`lacuna.binutils.libspies_report.SpiesReport.gather_spy_data`.
        """
        for pname in sorted( self.spy_data.keys() ):
            self.spy_data[pname].display_report( self )


