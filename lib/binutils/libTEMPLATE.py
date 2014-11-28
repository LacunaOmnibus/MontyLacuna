
import argparse, lacuna, os, sys

class RecallAllSpies:

    def __init__(self):
        self.bindir = os.path.abspath(os.path.dirname(sys.argv[0]))

        parser = argparse.ArgumentParser(
            description = 'I SHOW UP ABOVE THE OPTIONS SECTION IN HELP',
            epilog      = 'I SHOW UP BELOW THE OPTIONS SECTION IN HELP',
        )
        parser.add_argument( 'name', 
            metavar     = '<planet>',
            action      = 'store',
            help        = 'Name of planet on which to build ships.'
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
        parser.add_argument( '--quiet', 
            dest        = 'quiet',
            action      = 'store_true',
            help        = "Silence all output."
        )
        self.args   = parser.parse_args()


    def connect( self ):
        return lacuna.clients.Member(
            config_file     = self.args.config_file,
            config_section  = self.args.config_section
        )

