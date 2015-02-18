
### Search on CHECK
###
### This works, but is very much a quick-and-dirty because I needed it now now 
### now and didn't have time to make it pretty.
###
### Fixify it.

import lacuna, lacuna.binutils.libbin
import argparse, csv, operator, os, sys

class StationsReport(lacuna.binutils.libbin.Script):
    """ Gather and report on stations.
    """

    def __init__(self):
        self.version = '0.1'
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
        ### I'm purposely not documenting some of the args, like "building" or 
        ### "influence", just because it's easier to type the abbreviated 
        ### versions.  But somebody's going to type it all the way out.
        parser.add_argument( '--report', 
            metavar     = '<report type>',
            action      = 'store',
            choices     = [ 'allres', 'bldg', 'building', 'buildings', 'chain', 'inf', 'influence', 'lowres' ],
            default     = 'allres',
            help        = "Determines which report to display.  One of 'allres', 'bldg', 'chain', 'inf', 'lowres'.  Defaults to 'allres'."
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
        self.client.user_logger.debug( "Checking station {}.".format(sname) )
        self.client.cache_on( 'my_stations', 3600 )
        self.station = self.client.get_body_byname( sname )
        self.client.cache_off()

    def run_report( self ):
        """ Displays the report specified by the user at the command line.
        """
        if self.args.report == 'allres':
            return self.show_allres()
        elif self.args.report == 'bldg' or self.args.report == 'building' or self.args.report == 'buildings':
            return self.show_buildings()
        elif self.args.report == 'chain':
            return self.show_sc()
        elif self.args.report == 'inf' or self.args.report == 'influence':
            return self.show_influence()
        elif self.args.report == 'lowres':
            return self.show_lowres()

    def _report_header( self ):
        return( "{} ({}, {}) - Zone {}"
            .format(self.station.name, self.station.x, self.station.y, self.station.zone)
        )

    def _res_report( self ):
        tmpl = "\t{:<20} {: >12,}\n"
        mystr =   tmpl.format(  "Food / hour:",     self.station.food_hour      )
        mystr +=  tmpl.format(  "Ore / hour:",      self.station.ore_hour       )
        mystr +=  tmpl.format(  "Water / hour:",    self.station.water_hour     )
        mystr +=  tmpl.format(  "Energy / hour:",   self.station.energy_hour    )
        return mystr

    def _show_res_report( self ):
        print( self._report_header() )
        print( self._res_report(), end="" )
        print( "---------------" )

    def show_allres( self ):
        """ Show the allres report.  """
        cnt = 1
        self._show_res_report()
        return cnt

    def show_buildings( self ):
        """ Show the buildings report.  """
        cnt = 1
        tmpl = "    {:<30} {: >13} {: >8} {: >12}" 
        print( self._report_header() )
        print( tmpl.format("NAME", "COORDS", "LEVEL", "EFFICIENCY") )
        for name, dict_list in sorted( self.station.buildings_name.items() ):
            for bd in dict_list:
                coords = "({},{})".format(bd['x'], bd['y'])
                print( tmpl.format(bd['name'], coords, bd['level'], bd['efficiency']) )
        print( "---------------" )
        return cnt

    def show_influence( self ):
        """ Show the influence report.  """
        cnt = 1
        print( self._report_header() )
        print( "\tSpent/Available -- {}/{}".format(self.station.influence.spent, self.station.influence.total) )
        return cnt

    def show_lowres( self ):
        """ Show the lowres report.  """
        cnt = 0
        print( self._report_header() )
        if self.station.food_hour < 0 or self.station.ore_hour < 0 or self.station.water_hour < 0 or self.station.energy_hour < 0:
            cnt += 1
            self._show_res_report()
        else:
            l.debug( "All resource incomes for {} are positive; no report created.".format(self.station.name) )
        return cnt

    def show_sc( self ):
        """ Show the supply chain report.  """
        cnt = 1
        self.client.cache_on( 'my_stations', 3600 )
        pcc = self.station.get_buildings_bytype( 'stationcommand', 1, 1 )[0]
        self.client.cache_off()
        chains      = pcc.view_incoming_supply_chains()
        hdr_tmpl    = "    {:<26} {:<10} {: >15} {: >13}"   # can't comma-ify header string
        tmpl        = "    {:<26} {:<10} {: >15,} {: >13}"
        print( self._report_header() )
        print( hdr_tmpl.format("SOURCE", "RES TYPE", "RES/HOUR", "EFFICIENCY") )
        for sc in sorted( list(chains), key=operator.attrgetter('from_body.name', 'resource_type') ):
            body    = self.summarize( sc.from_body.name, 26 )
            rtype   = self.summarize( sc.resource_type, 10 )
            print( tmpl.format(body, rtype, sc.resource_hour, sc.percent_transferred) )
        print( "---------------" )
        ### We're returning the number of stations we've reported on, not the 
        ### number of supply chains.  So don't inc this in the for loop.
        return cnt

