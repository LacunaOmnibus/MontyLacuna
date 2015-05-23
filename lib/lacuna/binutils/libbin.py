
import argparse, lacuna, os, sys
from lacuna.abbreviations import Abbreviations

class FindConfigFileAction( argparse.Action ):
    def __init__( self, option_strings, dest, nargs=None, **kwargs ):
        self.option_strings = option_strings
        self.dest = dest
        if nargs is not None:
            raise ValueError("nargs not allowed")
        super(FindConfigFileAction, self).__init__(option_strings, dest, **kwargs)

    def __call__( self, parser, namespace, value, option_string ):
        ### This only gets called if the user sends a "--file" argument.
        file = self.find_config_file( value )
        if file:
            setattr( namespace, self.dest, self.file )
        else:
            raise ValueError("I was unable to find your config file '{}'.".format(value) )

    def find_config_file( self, filecand ):
        bindir = os.path.abspath(os.path.dirname(sys.argv[0]))
        candpaths = (bindir + "/../etc", bindir + "/..", bindir )
        file = None
        for i in candpaths:
            f = i + "/" + filecand
            if os.path.isfile( f ):
                file = f
        return file


class Script:
    """ Base class for scripts.

    Arguments:
        - parser -- Required argparse parser
        - section -- Optional config section to read from.  Defaults to 
          'sitter'.

    Sample Code::

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

    Object Attributes::

        By inheriting from binutils.libbin.Script, your script's main class 
        will get the following:

        abbrv       :class:`lacuna.abbreviations.Abbreviations` object
        args        The user's arguments, passed from the command line.
        bindir      The full path to the directory containing the script
                    being run.
        client      A TLE client, connected using the empire and password
                    found in the requested config file section.
        parser      The argparse parser.
        version     The program version.  Generally this will be set in
                    the ``__init__`` method of the inheriting child class, but 
                    if it's not set there, this will default to '0.1'

        skip_argparse   Dispatch table of arguments that bypass 
                        argparse.parse_args().  See below.

                        If you want to include this attribute, you'll need to 
                        create it before calling super().__init().  See below.


    skip_argparse
        Sometimes you want to give the user the ability to pass an option that 
        will obviate the need for specifying any other options.
        
        For example, in the ``search_archmin.py script``, the ``--list`` (or 
        ``-l``) argument displays a list of all ores the user can chose from, 
        and then quits.
        
        In this case, there's no need for the user to supply the otherwise 
        required ``planet`` or ``glyph`` positional arguments.

        So we're going to set up a dispatch table containing the arguments 
        that will override the need for the other, usually-required arguments.

        The dispatch table's keys are the string args (in our example case, 
        both ``-l`` and ``--list`` would be keys), and the values are the 
        methods to call when those arguments are encountered.
        
        Remember to omit the parens -- you're specifying the method, not 
        calling it.  In our example, both of our keys have the same value of 
        ``self.list_ores``.
        
        eg::

            def list_ores( self ):
                # Code to list out all the ores in the game and then quit().

            self.skip_argparse = {
                '-l':       self.list_ores,
                '--list':   self.list_ores,
            }

            super().__init__(parser)

        We'd now need to create a ``list_ores()`` method that would be called 
        when either of those options are specified.

        Most of the time you're going to want your script to end after the 
        method specified in the dispatch table is run, so be sure to include a 
        ``quit()`` call at the end::

            def list_ores( self ):
                for i in list_of_ore_names:
                    print( i )
                quit()

    Parser
        The argparse parser handed in will have the following optional 
        arguments already set up:

            - ``--file``
            - ``--section``
            - ``-q``, ``--quiet``
            - ``-v``, ``--verbose``
        
        Any other arguments that are specific to your script will need to be 
        added before calling ``super().__init__()``.

    Skip Logging In
        There will occasionally be scripts that don't need to log in to the 
        TLE servers, but still want access to some of the features provided by 
        the Clients class, such as logging.  ``update.py`` is an example of 
        this.

        If you're creating such a script, set your module up as above, but 
        before calling ``__init__``, create an attribute called ``guest`` set 
        to a true value::
        
            self.guest = True;
            super().__init__(parser)

        Now your script's module will have a ``self.client`` attribute, from 
        which you can get ``self.client.user_logger``, but that client won't 
        need to log in.

        When skipping login like this, the --file and --section arguments 
        don't pertain, so they will automatically be omitted from the help 
        (-h) blurb.
    """
    def __init__(self, parser, section:str = 'sitter', testargs:dict = {}):
        self.bindir = os.path.abspath(os.path.dirname(sys.argv[0]))

        if not hasattr(self, 'guest') or not self.guest:
            parser.add_argument( '--file', dest        = 'config_file',
                metavar     = '<config_file>',
                action      = FindConfigFileAction,
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

        if testargs:
            ### testargs dict was passed in to impersonate command-line args; 
            ### we're most likely running a unit test.  Accept that dict and 
            ### don't involve Argparse.
            testargs['quiet'] = True
            testargs['verbose'] = 0
            self.set_testargs(testargs)
        else:
            self.args = parser.parse_args()
            self.connect()

        ### The update script uses a Guest client, not a Member client, and a 
        ### Guest client can't have abbreviations.
        if isinstance(self.client, lacuna.clients.Member):
            self.abbrv = Abbreviations(self.client)

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

    def set_planets(self):
        """ Set the list of working planets based on command-line arguments.

        Required argument:
            - name -- The name of the single planet to work on, or 'all' to
              include all of my planets.

        Sets ``self.planets`` to a list of planet name strings.
        """
        self.client.cache_on( 'my_colonies', 3600 )
        if self.args.name == 'all':
            for colname in self.client.empire.colony_names.keys():
                self.planets.append(colname)
        else:
            self.planets = [ self.abbrv.get_name(self.args.name) ]
        self.client.cache_off()

    def set_testargs( self, a:dict ):
        self.client = a['client']
        self.args = argparse.Namespace()
        for k, v in a.items():
            setattr(self.args, k, v)

    def connect( self ):
        """ Connects to the game server, using the config_file and 
        config_section arguments.

        If a script doesn't need to log in to the TLE servers 
        (eg ``update.py``), it can create a ``no_connect`` attribute and set it 
        to True.

        Sets self.client if ``no_connect`` is not True.
        """
        if hasattr(self, 'guest') and self.guest:
            self.client = lacuna.clients.Guest()
            return
        try:
            self.client = lacuna.clients.Member(
                config_file     = self.args.config_file,
                config_section  = self.args.config_section
            )
        except (lacuna.exceptions.ServerError, lacuna.exceptions.BadCredentialsError) as e:
            print( "The empire name or password in your config file is incorrect.  Edit etc/lacuna.cfg to fix." )
            quit()

    def summarize( self, string:str, mymax:int ):
        """ Summarizes a string, usually for inclusion in a report section 
        with a fixed width.

        Arguments:
            - string -- Some string to summarize
            - max -- Integer max length of the string.  Must be greater than 3.

        If the string is "abcdefghijk" and the max is 6, this will return 
        "abc..."

        Returns the summarized string, or the original string if it was shorter 
        than max.
        """
        mymax = 4 if mymax < 4 else mymax
        if len(str(string)) > mymax:
            submax = mymax - 3
            string = string[0:submax] + "..."
        return string

