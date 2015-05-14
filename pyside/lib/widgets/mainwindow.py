
###
### Left off at CHECK
###

import configparser, os 
import lacuna, lacuna.exceptions as err
from PySide.QtGui import QApplication, QFileDialog, QMainWindow
from gui import Ui_MainWindow
import widgets

class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None, config_file=None):
        self.client         = None
        self.config_file    = config_file
        self.config_section = 'sitter'
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.set_events()

    def test(self, text="foo"):
        print( self.popconf("flurble?") )

    def popconf(self, text):
        dialog = widgets.ConfBox(self)
        return dialog.set_message( text )

    def poperr(self, text):
        dialog = widgets.ErrBox(self)
        dialog.set_message( text )

    def popmsg(self, text):
        dialog = widgets.MsgBox(self)
        dialog.set_message( text )

    def set_events(self):
        #self.btn_login.clicked.connect( self.login )
        self.btn_get_empire_status.clicked.connect( self.get_empire_status )
        #self.btn_show_config_status.clicked.connect( self.update_config_status )
        self.actionChose_Config_File.activated.connect( self.chose_config_file )
        self.actionChose_Config_Section.activated.connect( self.chose_config_section )
        self.actionConfig_File_Status.activated.connect( self.update_config_status )
        self.actionConfig_File_Status.activated.connect( self.update_config_status )
        self.actionLog_In.activated.connect( self.login )
        self.actionTest.activated.connect( self.test )
        
    def chose_config_file(self):
        ### assumes we're in MONTY/pyside/lib/widgets
        dir = os.path.dirname(os.path.realpath(__file__)) + "/../../../etc"

        ### The filter rv below is just the same filter ("Config Files..." 
        ### that we passed to getOpenFileName().  I dunno why we're getting it 
        ### back again.)
        ### The file rv is the full path to the chosen file.
        ### If the user cancels the file choser, the file rv is an empty 
        ### string.
        file, filter = QFileDialog.getOpenFileName( self, "Open Image", dir, "Config Files (*.cfg)" )
        if file:
            self.config_file = file

    def chose_config_section(self):
        ### Make sure self.config_file is an existing file
        if not os.path.isfile( self.config_file ):
            self.popmsg("Chose a config file first.")
            return

        ### Try to parse it as a config file
        cp = configparser.ConfigParser( interpolation = None )
        try:
            cp.read( self.config_file )
        except configparser.MissingSectionHeaderError as e:
            self.poperr("{} is not a valid config file.".format(self.config_file))
            return

        ### Display list of available sections
        mylist = [i for i in sorted(cp)]
        pick = widgets.PickList( self )
        pick.add( mylist )
        rv = pick.pickone() # -sitter-, -real-, etc, but might also be None if user didn't pick anything.
        if rv:
            if rv != self.config_section:
                self.client = None
            self.config_section = rv

    def login(self):
        self.statusbar.showMessage("Logging in...")
        self.statusbar.repaint()
        self.client = lacuna.clients.Member( # don't catch the exception if it happens
            config_file     = self.config_file,
            config_section  = self.config_section,
        )
        self.update_config_status()

    def update_config_status(self):
        if self.client:
            self.statusbar.showMessage("Logged in as {} from config file section {}."
                #.format(cp[self.config_section]['username'], self.config_section)
                .format(self.client.empire.name, self.config_section)
            )
        else:
            self.statusbar.showMessage("Using config file section {}."
                .format(self.config_section)
            )

    def get_empire_status(self):
        if not self.client:
            self.poperr("You must log in first.")
            return

        out = []

        if int(self.client.empire.self_destruct_active) > 0:
            out.append("*** SELF DESTRUCT IS ACTIVE! ***")
            out.append("")

        out.append("ID: " + self.client.empire.id )
        out.append("RPC Usage: " + str(self.client.empire.rpc_count) )
        out.append("Status Message: " + self.client.empire.status_message )
        out.append("New Mail Messages: " + str(self.client.empire.has_new_messages) )
        out.append("Essentia: " + str(self.client.empire.essentia) )
        out.append("Tech Level: " + str(self.client.empire.tech_level) )
        out.append("")
        out.append("Planets: ")
        for p in sorted( self.client.empire.colony_names.keys() ):
            out.append("\t" + p)

        self.txt_status.setPlainText( "\n".join(out) )

