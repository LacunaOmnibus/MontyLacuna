
import lacuna, lacuna.binutils.libbin
import lacuna.exceptions as err
import argparse, math, operator

class ExcavsReport(lacuna.binutils.libbin.Script):
    """ Gather and report on spy data by planet.
    """

    def __init__(self, testargs:dict = {}):
        self.version = '0.1'
        parser = argparse.ArgumentParser(
            description = 'Displays a report on excavators.',
            epilog      = "Full docs can be found at http://tmtowtdi.github.io/MontyLacuna/scripts/excavs_report.html",
        )
        parser.add_argument( 'name', 
            metavar     = '<planet>',
            action      = 'store',
            help        = "Produce report on excavs from this planet.  'all' to report on all planets."
        )
        parser.add_argument( '--fresh', 
            action      = 'store_true',
            help        = "Spy data is cached so you can run the report multiple times, quickly.  But if you run it once, then go assign or train spies and want a new report that includes those spies, you'll want fresh, not cached data.  In that case, pass this option on the second run."
        )
        super().__init__(parser, testargs = testargs)
        self.header_written = False
        self.planet         = ''
        self.archmin        = ''
        self.planets        = []

        ### keyed off planet name, value is sorted list of excavators.  An 
        ### attribute 'distance' is being added to each value.  This will be 
        ### the cartesian distance between self.planet and the planet hosting 
        ### the excavator.
        self.excavator_data = {}

        if self.args.fresh:
            self.client.cache_clear( 'my_colonies' )
            self.client.cache_clear( 'my_excavators' )
        self.set_planets()

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
        self.archmin = self.planet.get_buildings_bytype( 'archaeology', 1, 1, 100 )[0]
        self.client.cache_off()

    def _derive_planet_distance( self, body:lacuna.body.Body ):
        """ Returns the cartesian distance from the current planet (self.planet) 
        and the Body object passed in.  Returns a float.
        """
        return math.sqrt( (body.x - self.planet.x)**2 + (body.y - self.planet.y)**2 )

    def gather_excavator_data( self ):
        """ Gathers data on excavators sent out from the current planet.
        """
        self.client.cache_on( 'my_excavators', 3600 )
        excavs, maxnum, travelling = self.archmin.view_excavators()
        self.client.cache_off()
        bodies = []
        for e in excavs:
            e.body.distance = self._derive_planet_distance( e.body )
            bodies.append( e.body )
        self.excavator_data[ self.planet.name ] = sorted( bodies, key=operator.attrgetter('distance') )

    def _show_header( self, pname ):
        """ Displays a header before the data for a specific planet.  Pass in 
        the name of the planet.
        """
        n = self.summarize( pname, 50 )
        print( "{:^50}".format(n) )
        print( "{:^50}".format("=" * len(n)) )
        print( self.header_tmpl.format("EXCAVATED COLONY", "DISTANCE", "TYPE") )

    def show_report( self ):
        """ Shows a report on all of the excavator data gathered.
        """
        self.header_tmpl    = "{: <30}{: >10}     {: <5}"
        self.tmpl           = "{: <30}{:10.2f}     {: <5}"
        for planet_name in sorted( self.excavator_data.keys() ):
            self._show_header(planet_name)
            bodies = self.excavator_data[planet_name]
            for b in bodies:
                if b.name == self.planet.name:
                    b.surface_type = "p3"
                print( self.tmpl.format(self.summarize(str(b.name), 30), b.distance, b.surface_type) )

