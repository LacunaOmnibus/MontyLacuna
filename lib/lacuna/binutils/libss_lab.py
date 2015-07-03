
import lacuna, lacuna.binutils.libbin, lacuna.types
import lacuna.exceptions as err
import argparse, os, sys
import lacuna.exceptions as err
import lacuna.utils

class SSLab(lacuna.binutils.libbin.Script):

    plan_names = [
        'art', 'command', 'food', 'ibs', 'opera', 'parliament', 'policestation', 'warehouse'
    ]

    def __init__(self):
        self.version = '0.1'
        parser = argparse.ArgumentParser(
            description = 'CHECK.',
            epilog      = "Full docs can be found at http://tmtowtdi.github.io/MontyLacuna/scripts/ss_lab.html",
        )
        parser.add_argument( 'planet', 
            metavar     = '<planet name>',
            action      = 'store',
            help        = 'Name of planet with an SS Lab where you want to build plans.'
        )
        parser.add_argument( 'plan', 
            metavar     = '<plan>',
            action      = 'store',
            choices     = self.plan_names,
            help        = "Name of plan to build.  One of {}.".format(self.plan_names)
        )
        parser.add_argument( '--num', 
            metavar     = '<number>',
            action      = 'store',
            type        = int,
            default     = 1,
            help        = "Number of plans to build.  Defaults to 1."
        )
        parser.add_argument( '--level', 
            metavar     = '<level>',
            dest        = 'level',
            action      = 'store',
            type        = int,
            default     = 1,
            help        = 'Level of plan to build.  Defaults to 1.'
        )
        parser.add_argument( '--sub', 
            action      = 'store_true',
            default     = False,
            help        = "BE CAREFUL WITH THIS.  If you include this argument, any plans you specified will be built and their build times will all be subsidized at the cost of 2 E each.",
        )
        super().__init__(parser)
        if self.args.level > 30:
            raise KeyError("You can't build plans higher than level 30.")
        self.ute = lacuna.utils.Utils()
        self.client.cache_on( 'my_colonies', 3600 )
        self._set_planet()
        self.client.cache_off()
        self._set_lab()


    def _set_planet( self ):
        pname       = self.abbrv.get_name( self.args.planet )
        self.planet = self.client.get_body_byname( pname )

    def _set_lab( self ):
        try:
            self.lab = self.planet.get_buildings_bytype('ssla', 0, 1, 100)[0]
        except err.ServerError as e:
            print( "You don't have a working SSLab building on {}.".format(self.planet.name) )

    def build_plan( self ):
        """ Builds the plan requested by the command-line arguments.

        Returns:
            seconds (int): Number of seconds until this build completes.
        Raises:
            KeyError if the requested plan level is higher than the level of the lab.
        """
        if self.args.level > self.lab.level:
            raise KeyError("Your lab level is {}, so you can't make plans of higher level.".format(self.lab.level) )
        try:
            view = self.lab.make_plan(self.args.plan, self.args.level) 
        except err.ServerError as e:
            ### The request logger already spit the reason for not being able 
            ### to build out to STDERR; no need to reproduce that message, so 
            ### just quit.
            quit()
        return self.lab.work.seconds

    def subsidize_plan( self ):
        try:
            self.lab.subsidize_plan()
        except err.ServerError as e:
            quit()
            
