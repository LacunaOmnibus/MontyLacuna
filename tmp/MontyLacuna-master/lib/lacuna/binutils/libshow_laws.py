
import lacuna, lacuna.exceptions, lacuna.binutils.libbin
import lacuna.exceptions as err
import argparse, re

class ShowLaws(lacuna.binutils.libbin.Script):
    def __init__(self):
        self.version = '0.1'
        parser = argparse.ArgumentParser(
            description = "Displays the laws a star is subject to.",
            epilog = 'Full docs can be found at http://tmtowtdi.github.io/MontyLacuna/scripts/show_laws.html',
        )
        parser.add_argument( 'name', 
            metavar     = '<star>',
            action      = 'store',
            help        = 'The name of any star in the expanse.'
        )
        parser.add_argument( '--all',
            action      = 'store_true',
            help        = 'Star seizure laws are boring and are usually not displayed.  Pass this argument to see them as well.'
        )
        parser.add_argument( '--fresh',
            action      = 'store_true',
            help        = 'Clears any cached data.'
        )
        super().__init__(parser)

        ### ally_id and ally_name will not be set unless the station has 
        ### Members Only... laws set.  So check them before trying to use 
        ### them.
        self.ally_id            = None
        self.ally_name          = None

        self.map                = None
        self.star               = None
        self.seizure_laws       = []
        self.nonseizure_laws    = []

        if self.args.fresh:
            self.client.cache_clear( 'foreign_stations' )

        self._set_map()
        self._set_star()
        self._set_laws()


    def _set_map( self ):
        self.client.cache_on( 'foreign_stations', 3600 )
        self.map = self.client.get_map()
        self.client.cache_off()

    def _set_star( self ):
        """ Must be called after _set_map()
        """
        self.client.cache_on( 'foreign_stations', 3600 )
        try:
            self.star = self.map.get_star_by_name( self.args.name )
        except err.ServerError as e:
            print( "{} is not a valid star name.".format(self.args.name) )
            quit()
        if not hasattr(self.star, 'station'):
            print( "{} is either not seized by a station, or you don't have it probed.".format(self.args.name) )
            quit()
        self.client.cache_off()

    def _set_laws( self ):
        """ Must be called after _set_star()
        """
        self.client.cache_on( 'foreign_stations', 3600 )
        laws = self.star.view_laws()
        self.client.cache_off()

        seize_patt  = re.compile("^Seize control of \{Starmap [-\d]+")
        for l in laws:
            self._set_ally_if_possible( l.description )
            if seize_patt.match( l.description ):
                ### The descriptions of seizure laws contain a bunch of 
                ### in-game tag-type stuff that looks like crap on the 
                ### terminal.  Just repeat the name.
                l.description = l.name
                self.seizure_laws.append( l )
            else:
                self.nonseizure_laws.append( l )

    def _set_ally_if_possible( self, desc ):
        """ Some laws, namely the "Members Only ..." laws, include the name of 
        the alliance that passed the law in the description.
        """
        patt = re.compile("Only members of {Alliance (\d+) ([^}]+)}")
        rslt = patt.match( desc )
        if rslt:
            self.ally_id    = rslt.group(1)
            self.ally_name  = rslt.group(2)

    def show_laws_report( self ):
        reported_laws = []
        if self.args.all:
            reported_laws = self.seizure_laws
        reported_laws += self.nonseizure_laws
        for i in reported_laws:
            name = self.summarize( i.name, 30 )
            desc = self.summarize( i.description, 40 )
            print( "{:<30} {:<40}".format(name, desc) )

        print( "" )
        print( "The seizing station, {}, has seized {} stars."
            .format(self.star.station.name, len(self.seizure_laws)) 
        )
        if self.ally_name:
            print( "That station is owned by {}.".format(self.ally_name) )



