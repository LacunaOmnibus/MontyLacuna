
import argparse, lacuna, os, sys

class Script:
    """ Base class for scripts.

    Arguments:
        - parser -- Required argparse parser
        - section -- Optional config section to read from.  Defaults to 
          'sitter'.

    Example::

        import binutils.libbin

        class MyScript( binutils.libbin.Script ):
            def __init__(self):
                parser = argparse.ArgumentParser(
                    description = "This shows above the options docs in help",
                    epilog      = "This shows below the options docs in help",
                )
                parser.add_argument( '--quiet',
                    dest        = 'quiet',
                    action      = 'store_true',
                    help        = "Silence all output."
                )
            super().__init__( parser )

    Attributes::

        args        The user's arguments, passed from the command line.
        bindir      The full path to the directory containing the script being 
                    run.
        client      A TLE client, connected using the empire and password found 
                    in the requested config file section.
        parser      The argparse parser.
        version     The program version.  Generally this will be set in the 
                    ``__init__`` method of the inheriting child class, but if 
                    it's not set there, this will default to '0.1'


    Parser
        The argparse parser handed in will have the optional arguments 
        ``--file`` and ``--section`` added to it.
        
        Any other arguments that are specific to your script will need to be 
        added before calling ``super().__init__()``.
    """
    def __init__(self, parser, section:str = 'sitter'):
        self.bindir = os.path.abspath(os.path.dirname(sys.argv[0]))

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
            default     = section,
            help        = "Config file section.  Defaults to '" + section + "'."
        )
        parser.add_argument( '-q', '--quiet', 
            dest        = 'quiet',
            action      = 'store_true',
            help        = "By default, information on what's happening gets displayed to the screen.  Including this will silence all output.  Overrides '-v'."
        )
        parser.add_argument( '-v', '--verbose', 
            dest        = 'verbose',
            action      = 'count',
            help        = "Increase output verbosity level -- produces more in-depth screen reporting on what's happening.  Has no effect if --quiet is used."
        )
        self.args   = parser.parse_args()
        self.client = self.connect()

        ### Set log level
        if not self.args.quiet:
            if self.args.verbose:
                self.client.user_log_stream_handler.setLevel('DEBUG')
            else:
                self.client.user_log_stream_handler.setLevel('INFO')

        ### Set version
        vers = '0.1'
        if hasattr(self, 'version'):
            vers = self.version
        else:
            self.version = vers
        parser.add_argument( '--version', 
            action      = 'version',
            version     = os.path.basename(sys.argv[0]) + ' ' + vers,
            help        = "Print program version and quit"
        )


    def connect( self ):
        try:
            client = lacuna.clients.Member(
                config_file     = self.args.config_file,
                config_section  = self.args.config_section
            )
        except (lacuna.exceptions.ServerError, lacuna.exceptions.BadCredentialsError) as e:
            print( "The empire name or password in your config file is incorrect.  Edit etc/lacuna.cfg to fix." )
            quit()
        return client


