
import argparse, lacuna, os, sys

class RecallAllSpies:

    def __init__(self):
        self.bindir = os.path.abspath(os.path.dirname(sys.argv[0]))

        parser = argparse.ArgumentParser(
            description = "Fetch home all spies based on a given planet, regardless of where they're currently located.  Spies will be fetched using the fastest ship you have available that can carry occupants.",
            epilog      = "EXAMPLE: python3 bin/recall_all_spies Earth",
        )
        parser.add_argument( 'name', 
            metavar     = '<planet>',
            action      = 'store',
            help        = 'All spies from this planet will be recalled.'
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

    
    def find_nothome_spies( self, home_id:int, intmin ):
        """
        Returns a dict of all of the bodies where you've got spies assigned, 
        not including your current planet (home_id).

        The returned dict is:
            planet_id: planet_name
        """
        bodies = {}
        spies = intmin.view_all_spies()
        for s in spies:
            if s.assigned_to.body_id == home_id:
                continue
            else:
                bodies[ s.assigned_to.body_id ] = s.assigned_to.name
        return bodies


