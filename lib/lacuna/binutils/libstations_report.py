
### Search on CHECK
###
### This works, but is very much a quick-and-dirty because I needed it now now 
### now and didn't have time to make it pretty.
###
### Fixify it.

import lacuna, lacuna.binutils.libbin
import argparse, csv, os, sys

class StationsReport(lacuna.binutils.libbin.Script):
    """ Gather and report on stations.
    """

    def __init__(self):
        self.version = '0.1'
        ### CHECK I updated no help docu below.
        parser = argparse.ArgumentParser(
            description = 'Displays a report on one or more space stations.',
            epilog      = "Full docs, including explanations of the different report types, can be found at http://tmtowtdi.github.io/MontyLacuna/scripts/stations_report.html",
        )
        parser.add_argument( 'name', 
            metavar     = '<station>',
            action      = 'store',
            help        = "Produce report on this station.  'all' to report on all stations."
        )
        parser.add_argument( '--fresh', 
            action      = 'store_true',
            help        = "Ship data is cached so you can run the report multiple times, quickly.  But if you run it once, then go build ships and want a new report that includes those ships, you'll want fresh, not cached data.  In that case, pass this option on the second run."
        )
        parser.add_argument( '--report', 
            metavar     = '<report type>',
            action      = 'store',
            choices     = [ 'allres', 'inf', 'lowres' ],
            default     = 'allres',
            help        = "Determines which report to display.  One of 'allres', 'inf', 'lowres'.  Defaults to 'allres'."
        )
        super().__init__(parser)
        self.station        = ''
        self.stations       = []
        if self.args.fresh:
            self.client.cache_clear( 'stations_report' )
            self.client.cache_clear( 'my_stations' )
        self._set_stations()


    def _set_stations( self ):
        self.client.cache_on( 'my_stations', 3600 )
        self.planets = []
        if self.args.name == 'all':
            for station_name in sorted( self.client.empire.station_names.keys() ):
                self.stations.append(station_name)
        else:
            self.stations = [self.args.name]
        self.client.cache_off()


    def set_station( self, sname:str ):
        """ Meant to be called by the user to set which planet we're working on 
        right now.

        Arguments:
            - sname -- String name of the planet
        """
        self.client.cache_on( 'my_stations', 3600 )
        self.station = self.client.get_body_byname( sname )
        self.client.cache_off()


    def run_report( self ):
        if self.args.report == 'lowres':
            return self.show_lowres()
        elif self.args.report == 'allres':
            return self.show_allres()
        elif self.args.report == 'inf':
            return self.show_influence()

    def _show_report_header( self ):
        print( "{} ({}, {}) - Zone {}"
            .format(self.station.name, self.station.x, self.station.y, self.station.zone)
        )

    def show_lowres( self ):
        cnt = 0
        if self.station.food_hour < 0 or self.station.ore_hour < 0 or self.station.water_hour < 0 or self.station.energy_hour < 0:
            cnt += 1
            self._show_report_header()
            print( "\tFood / hour:", self.station.food_hour )
            print( "\tOre / hour:", self.station.ore_hour )
            print( "\tWater / hour:", self.station.water_hour )
            print( "\tEnergy / hour:", self.station.energy_hour )
            print( "---------------" )
        return cnt

    def show_allres( self ):
        cnt = 1
        self._show_report_header()
        print( "\tFood / hour:", self.station.food_hour )
        print( "\tOre / hour:", self.station.ore_hour )
        print( "\tWater / hour:", self.station.water_hour )
        print( "\tEnergy / hour:", self.station.energy_hour )
        print( "---------------" )
        return cnt

    def show_influence( self ):
        cnt = 1
        self._show_report_header()
        print( "\tSpent/Available -- {}/{}".format(self.station.influence.spent, self.station.influence.total) )
        return cnt

