
import configparser, os, sys, textwrap
from PySide.QtGui import QApplication
import lacuna, widgets
from lacuna.abbreviations import Abbreviations
from lacuna.utils import Utils

class MyApp(QApplication):
    """ The main application class.

    Attributes:
        abbrv (lacuna.abbreviations.Abbreviations): Set when logged in, None
                                                    when logged out.
        client (lacuna.clients.Member): Set when logged in, None when logged
                                        out.
        config_file (str): FQ path to the config file.  Defaults to 'lacuna.cfg' 
                           in MONTY/etc/.
        config_section (str): The config file section we're using.  Defaults to 
                              'sitter'.
        instdir (str): FQ path to the MontyLacuna install directory.
        is_logged_in (bool): True when logged in, False when logged out.

    """

    name        = 'My Cool App'
    __version__ = '0.1'

    def __init__(self, argv):
        super().__init__(argv)
        self.instdir        = self.find_installdir()
        self.abbrv          = False
        self.client         = False
        self.config_file    = self.instdir + "/etc/lacuna.cfg"
        self.config_section = 'sitter'
        self.is_logged_in   = False

    def run(self):
        frame = widgets.MainWindow()
        frame.show()
        sys.exit( self.exec_() )

    def find_installdir(self):
        """ Finds the MontyLacuna install dir, provided it's a parent 
        of the directory containing this file (which it should be).

        Returns (str): Canonical path to the install directory.

        Raises (SystemError): If the install directory could not be found.
        """
        dir = os.path.dirname(os.path.realpath(__file__))
        while(1):
            cand = os.path.dirname(os.path.realpath(dir))
            if cand == os.path.dirname(os.path.realpath('/')):
                raise SystemError("Cannot find MontyLacuna's install directory.")
            cand1 = cand + "/bin"
            cand2 = cand + "/doc"
            cand3 = cand + "/etc"
            cand4 = cand + "/pyside"
            if os.path.isdir(cand1) and os.path.isdir(cand2) and os.path.isdir(cand3) and os.path.isdir(cand4):
                return cand
            else:
                dir += "/.."

    def login(self):
        """ Logs in to TLE using the credentials stored in our currently-set 
        config file and section.
        """
        self.client = lacuna.clients.Member( # don't catch the exception if it happens
            config_file     = self.config_file,
            config_section  = self.config_section,
        )
        self.is_logged_in = True
        self.abbrv = Abbreviations(self.client, vardir = self.instdir + "/var")

    def logout(self):
        """ Logs out of TLE.
        """
        self.is_logged_in   = False
        self.abbrv          = None
        self.client         = None

    def popconf(self, parent, text, width:int = 60):
        """ Pops up a yes/no question in a new dialog, along with "Yes" and "No"
        buttons, then returns the user's response.

        Arguments:
            parent (QWidget): The dialog's parent.
            text (str): The question to display in the popup.
            width (int): Number of columns at which to wrap the text.  Defaults 
                         to 60.
        
        Returns (int): 0 if the user clicked No, 1 if they clicked Yes.
        """
        dialog = widgets.ConfBox(parent)
        text = "\n".join( textwrap.wrap(text, width) )
        return dialog.set_message( text )

    def poperr(self, parent, text, width:int = 60):
        """ Pops up a message in a new dialog, along with a single "Cancel" button.

        Arguments:
            parent (QWidget): The dialog's parent.
            text (str): The text to display in the popup.
            width (int): Number of columns at which to wrap the text.  Defaults 
                         to 60.
        """
        dialog = widgets.ErrBox(parent)
        text = "\n".join( textwrap.wrap(text, width) )
        dialog.set_message( text )
        dialog.show()

    def popmsg(self, parent, text, width:int = 60):
        """ Pops up a message in a new dialog, along with a single "OK" button.

        Arguments:
            parent (QWidget): The dialog's parent.
            text (str): The text to display in the popup.
            width (int): Number of columns at which to wrap the text.  Defaults 
                         to 60.
        """
        dialog = widgets.MsgBox(parent)
        text = "\n".join( textwrap.wrap(text, width) )
        dialog.set_message( text )
        dialog.show()

    def readconfig(self):
        """ Reads and returns the current config file.

        Returns:
            cp (dict): The config file as a dict, with each section as a top-level key.

        Raises:
            IOError: If self.config_file could not be found or parsed as a config file.
        """
        if not os.path.isfile( self.config_file ):
            raise IOError("{}: No such file.")
        cp = configparser.ConfigParser( interpolation = None )
        try:
            cp.read( self.config_file )
        except configparser.MissingSectionHeaderError as e:
            raise IOError("{} is not a valid config file.".format(self.config_file))
        return cp

