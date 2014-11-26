
import argparse, lacuna, os, sys

class BuildShips:

    def __init__(self):
        self.bindir = os.path.abspath(os.path.dirname(sys.argv[0]))

        parser = argparse.ArgumentParser(
            description = 'Build ships in bulk.',
            epilog      = 'This shows at the end after help.',
        )
        ### https://docs.python.org/3.4/library/argparse.html#the-add-argument-method
        parser.add_argument( 'name', 
            metavar     = '<planet>',
            action      = 'store',
            help        = 'Name of planet on which to build ships.'
        )
        parser.add_argument( 'type', 
            metavar     = '<shiptype>',
            action      = 'store',
            help        = "Type of ship to build (eg 'scow_mega')."
        )

        parser.add_argument( '--num', 
            metavar     = '<count>',
            action      = 'store',
            type        = int,
            default     = 0,
            help        = "Number of ships to build.  Defaults to 'fill up all available build queue slots'."
        )
        parser.add_argument( '--level', 
            metavar     = '<lvl>',
            dest        = 'min_lvl',
            action      = 'store',
            type        = int,
            default     = 1,
            help        = 'Minimum shipyard level to use for building.  Defaults to 1.'
        )
        parser.add_argument( '--file', 
            dest        = 'config_file',
            metavar     = '<config_file>',
            action      = 'store',
            default     = self.bindir + "/../etc/lacuna.cfg",
            help        = "Path to the config file.  Defaults to 'ROOT/etc/lacuna.cfg'"
        )
        parser.add_argument( '--section', 
            dest        = 'config_section',
            metavar     = '<section>',
            action      = 'store',
            default     = 'sitter',
            help        = "Config file section.  Defaults to 'sitter'."
        )

        self.args   = parser.parse_args()


    def connect( self ):
        return lacuna.clients.Member(
            config_file     = self.args.config_file,
            config_section  = self.args.config_section
        )


    def get_shipyards( self, planet ):
        mymax = 0
        yards = planet.get_buildings_bytype( 'shipyard', self.args.min_lvl )
        if not yards:
            raise RuntimeError("You don't have any shipyards of the required level.")
        for y in yards:
            if hasattr(y, 'work'):
                ships, num, cost = y.view_build_queue()
                mymax += (int(y.level) - num)                    # SHIT y.level is a string.
            else:
                mymax += int(y.level)
        return( yards, mymax )






