
import lacuna, os

rootdir = os.path.join( os.path.abspath(os.path.dirname(__file__)), "..", "..", ".." )
etcdir  = os.path.join( rootdir, "etc" )

class Connector():
    """ Provides connected clients to test scripts.
    """
    def tle_connect(self):
        """ Connects to TLE twice, once with a sitter and once with a real 
        password.  Loglevels are set to CRITICAL so exceptions are not logged 
        to the terminal.

        Your test class is expected to inherit from Connector (as well as from 
        unittest.TestCase).  When calling tle_connect in your setUpClass, you'll 
        need to pass self as the first argument (I don't understand why)::

            self.tle_connect( self )
        """
        self.config_file = 'lacuna.cfg'
        self.sitter = lacuna.clients.Member(
            config_file     = os.path.join( etcdir, self.config_file ),
            config_section  = 'test_sitter'
        )
        self.real = lacuna.clients.Member(
            config_file     = os.path.join( etcdir, self.config_file ),
            config_section  = 'test_real'
        )
        ### We're going to be raising exceptions in our tests on purpose, and 
        ### don't want the logger to output any of those to the screen.
        self.sitter.request_log_stream_handler.setLevel('CRITICAL')
        self.real.request_log_stream_handler.setLevel('CRITICAL')

