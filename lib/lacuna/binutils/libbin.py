
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
                parser.add_argument( 'planet',
                    metavar     = '<planet>',
                    action      = 'store',
                    help        = "Name of the planet to run against."
                )
                ### 
                ### Add other arguments as needed
                ###
                super().__init__( parser )

    Attributes::

        By inheriting from binutils.libbin.Script, your script's main class 
        will get the following:

        args        The user's arguments, passed from the command line.
        bindir      The full path to the directory containing the script
                    being run.
        client      A TLE client, connected using the empire and password
                    found in the requested config file section.
        parser      The argparse parser.
        version     The program version.  Generally this will be set in
                    the ``__init__`` method of the inheriting child class, but 
                    if it's not set there, this will default to '0.1'

        If you need this attribute, you'll need to create it before calling 
        ``super().__init()``:

        skip_argparse   Dispatch table of arguments that bypass 
                        argparse.parse_args().  See below.

    skip_argparse
        Sometimes you want to give the user the ability to pass an option that 
        will obviate the need for specifying any other options.
        
        For example, in the ``search_archmin.py script``, the ``--list`` (or 
        ``-l``) arguments are meant to simply display a list of all ores the 
        user can chose from, as a convenience.  In this case, there would be 
        no need for the user to supply the otherwise required ``planet`` or 
        ``glyph`` positional arguments; we just want to display a list of ores 
        and quit.

        The dispatch table's keys are the string args (in our example case, 
        both ``-l`` and ``--list`` would be keys), and the values are the 
        methods to call.  Remember to omit the parens -- you're specifying the 
        method, not calling it.  In our example, both of our keys would have 
        the same value of ``self.list_ores``.  We'd then need to create a 
        ``list_ores()`` method that would be called when either of those 
        options are specified.

        eg::

            def list_ores( self ):
                # Code to list out all the ores in the game and then quit().

            self.skip_argparse = {
                '-l':       self.list_ores,
                '--list':   self.list_ores,
            }

            super().__init__(parser)

        Usually, you're going to want your script to end after the method 
        specified in the dispatch table is run, but it's possible that some 
        circumstance could crop up where that's not the case.  So if you do 
        want the script to quit after your method is run, be sure to include a 
        ``quit()`` call in your method.

    Parser
        The argparse parser handed in will have the following optional 
        arguments:

            - ``--file``
            - ``--section``
            - ``-q``, ``--quiet``
            - ``-v``, ``--verbose``
        
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

        if not hasattr(self, 'skip_argparse'):
            self.skip_argparse = {}
        for i in sys.argv:
            if i in self.skip_argparse:
                print( "Skipping argparse because of existence of ", i )
                self.skip_argparse[ i ]()

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


