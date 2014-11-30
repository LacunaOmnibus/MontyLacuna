
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

        bindir      The full path to the script being run.
        connect     Method; connects to the server and returns a
                    lacuna.clients.Member object.  Checks for bad credentials 
                    and produces reasonably friendly output if the login 
                    failed.
        parser      The argparse parser.

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
        self.args   = parser.parse_args()


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


