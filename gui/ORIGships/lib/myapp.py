
import configparser, datetime, os, pytz, sys, textwrap, time
from PySide.phonon import Phonon
from PySide.QtCore import *
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

        Returns:
            path (str): Canonical path to the install directory.

        Raises: (SystemError): If the install directory could not be found.
        """
        dir = os.path.dirname(os.path.realpath(__file__))
        while(1):
            cand = os.path.dirname(os.path.realpath(dir))
            if cand == os.path.dirname(os.path.realpath('/')):
                raise SystemError("Cannot find MontyLacuna's install directory.")
            cand1 = cand + "/bin"
            cand2 = cand + "/doc"
            cand3 = cand + "/etc"
            if os.path.isdir(cand1) and os.path.isdir(cand2) and os.path.isdir(cand3):
                return cand
            else:
                dir += "/.."

    def my_xor(self, a, b):
        """ Logical xor that accepts different types.

        Arguments:
            a: A value that can evaluate to a boolean
            b: A value that can evaluate to a boolean
        Returns:
            xor (bool): True if the arguments xor, False if they do not.
        """
        if (a and not b) or (b and not a):
            return True
        return False

    def get_ms_between(self, start:datetime, end:datetime):
        """ Returns the number of milliseconds between two dates.

        Order of the dates doesn't matter; the earlier date may be either the 
        first or second argument.

        If one of the dates is naive (timezone-unaware) but the other is 
        timezone-aware, the naive date will be localized to the timezone-aware 
        one.  It's very likely that this is going to return results you didn't 
        want.  Imagine:

            now = current datetime aware that it's in the America/New_York tz
            future = datetime in the future.  Its value is in UTC, but that
                     UTC tz is not set on the datetime object for whatever 
                     reason, so the object is naive.

        Localizing that future object to America/New_York will work, but it 
        will still be four or five hours in the future, since it was naive in 
        the first place and didn't recognize that it was in UTC, so its value 
        couldn't be changed accurately.

        TL;DR - either send both objects aware of their timezone, and set to 
        the same timezone, or send them both as unaware (naive) objects whose 
        values are both in the same timezone.

        Arguments:
            date_one (datetime.datetime): The first date
            date_two (datetime.datetime): The second date
        Returns:
            milliseconds (int)
        """
        s_tz = start.tzinfo
        e_tz = end.tzinfo

        if self.my_xor(s_tz, e_tz):
            ### Ugly and probably wrong from the user's perspective, but we 
            ### can't compare a naive datetime to an aware one.  So it's 
            ### either make them both aware or bail.
            if s_tz:
                end = s_tz.localize(end)
            else:
                start = e_tz.localize(start)

        if start > end:
            (start, end) = (end, start)
        delta = end - start
        return int(delta.total_seconds() * 1000)

    def get_ms_until(self, future:datetime):
        """ Returns the number of milliseconds from now until a specified date.

        If the specified date is in the past, milliseconds returned will still 
        be a positive integer, since we're simply returning the number of ms 
        between the two dates.

        The future datetime argument is allowed to be timezone-unaware, but if 
        it is you'll probably get goofy results.  You should really be sure 
        that it's timezone-aware before calling this.

        If that future datetime *is* timezone-aware, it doesn't matter what 
        timezone it's in.  The TZ will be determined, and the correct result 
        will get returned.

        Arguments:
            future (datetime.datetime): The future date.
        Returns:
            milliseconds (int)
        """
        tz = future.tzinfo
        if tz:
            now = datetime.datetime.now(tz)
        else:
            now = datetime.datetime.now()
        return self.get_ms_between( now, future )

    def login(self):
        """ Logs in to TLE using the credentials stored in our currently-set 
        config file and section.
        """
        client_getter = GetClient(self, self.config_file, self.config_section)
        self.client = client_getter.request()
        self.is_logged_in = True
        self.abbrv = Abbreviations(self.client, vardir = self.instdir + "/var")

    def logout(self):
        """ Logs out of TLE.
        """
        self.is_logged_in   = False
        self.abbrv          = None
        self.client         = None

    def play_sound(self, alias):
        """ Plays a sound
        
        Arguments:
            alias (str): The name of a sound file alias as specified in a .qrc
                         file, eg "mysound.wav"
        """
        speakers = Phonon.AudioOutput(Phonon.MusicCategory, self)
        media   = Phonon.MediaObject(self)
        speakers.setVolume(0.5)
        Phonon.createPath(media, speakers)
        media.setCurrentSource( ":/{}".format(alias) )
        ### If we let the media file play all the way through, we get a nasty 
        ### static squelch at the end.  Set it to stop playing 30 milliseconds 
        ### before the end.
        media.setPrefinishMark(30)
        media.prefinishMarkReached.connect( media.stop )
        media.play()

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
        self.processEvents()

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



###########################
# Threaded TLE requestors #
###########################

class GetClient(QThread):
    dataReady = Signal(object)

    def __init__(self, app, config_file, config_section, parent = None):
        QThread.__init__(self, parent)
        self.app            = app
        self.config_file    = config_file
        self.config_section = config_section
        self.client         = None

    def request(self):
        self.start()
        while(self.isRunning()):
            self.app.processEvents()
            time.sleep(0.1)
        return self.client

    def run(self):
        self.client = lacuna.clients.Member( # don't catch the exception if it happens
            config_file     = self.config_file,
            config_section  = self.config_section,
        )
        self.dataReady.emit(self.client) 

