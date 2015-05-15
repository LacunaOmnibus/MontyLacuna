
### Search on CHECK

import configparser, os, sys
import lacuna, lacuna.exceptions as err
from lacuna.abbreviations import Abbreviations
from lacuna.utils import Utils
### I may just end up with "import *" below.
from PySide.QtGui import QApplication, QFileDialog, QMainWindow, QTableWidgetItem
from PySide.QtCore import *
from gui import Ui_MainWindow
import widgets

class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None, config_file=None):
        self.abbrv          = None
        self.client         = None
        self.config_file    = config_file
        self.config_section = 'sitter'
        self.is_logged_in   = False
        self.utils          = Utils()
        self.vardir         = os.path.abspath(sys.argv[0] + "/../../../var")

        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.set_events()

        self.btn_get_empire_status.setEnabled(False)

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
        self.btn_login.clicked.connect( self.login )
        self.btn_logout.clicked.connect( self.logout )
        self.btn_logout.setEnabled( False ) 
        self.btn_get_empire_status.clicked.connect( self.get_empire_status )
        self.tabWidget.currentChanged.connect( self.tab_changed )
        self.btn_check_status.clicked.connect( self.update_config_status )
        self.actionChose_Config_File.activated.connect( self.chose_config_file )
        self.actionChose_Config_Section.activated.connect( self.chose_config_section )
        self.actionConfig_File_Status.activated.connect( self.update_config_status )
        self.actionConfig_File_Status.activated.connect( self.update_config_status )
        self.actionLog_In.activated.connect( self.login )
        self.actionTest.activated.connect( self.test )

    def resizeEvent(self, event):
        """ Called when the app initializes, and then again any time the main 
        window gets resized.
        """
        self.resize_abbrv_table()

    def tab_changed(self, num):
        """ Called when the user switches to the third tab.
        """
        pass
        if num == 2:
            self.resize_abbrv_table()
        
    def find_vardir(self):
        """ Finds the MontyLacuna var/ dir, provided it's a sibilng or 
        grand-cousin of the directory containing this file (which it 
        should be).

        Returns (str): Canonical path to the var/ directory

        Raises (SystemError): If the var/ directory could not be found.
        """
        dir = os.path.dirname(os.path.realpath(__file__))
        while(1):
            cand = os.path.dirname(os.path.realpath(dir))
            if cand == os.path.dirname(os.path.realpath('/')):
                raise SystemError("Cannot find MontyLacuna's var/ directory.")
            cand += "/var"
            if os.path.isdir( cand ):
                return cand
            else:
                dir += "/.."

    def chose_config_file(self):
        config_dir = self.utils.mytry( self.find_vardir )

        file, filter = QFileDialog.getOpenFileName( self, "Open Image", dir, "Config Files (*.cfg)" )
        if file:
            self.config_file = file
        self.logout();

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
        self.logout();

        ### Display list of available sections
        mylist = [i for i in sorted(cp)]
        pick = widgets.PickList( self )
        pick.add( mylist )
        rv = pick.pickone() # -sitter-, -real-, etc, but might also be None if user didn't pick anything.
        if rv:
            if rv != self.config_section:
                self.client = None
            self.config_section = rv

        self.update_config_status()

    def login(self):
        self.is_logged_in = True
        self.statusbar.showMessage("Logging in...")
        self.statusbar.repaint()
        self.client = lacuna.clients.Member( # don't catch the exception if it happens
            config_file     = self.config_file,
            config_section  = self.config_section,
        )
        self.abbrv = Abbreviations(self.client, vardir = self.vardir)
        self.setup_abbrv_table()
        self.btn_login.setEnabled(False)
        self.btn_logout.setEnabled( True ) 
        self.btn_get_empire_status.setEnabled(True)
        self.update_config_status()

    def logout(self):
        self.is_logged_in   = False
        self.abbrv          = None
        self.reset_gui()

    def resize_abbrv_table(self):
        ### The "-50" accounts for the line number column on the left.
        tbl_w   = self.tbl_abbrv.width() - 50
        name_w  = int(tbl_w * .75)
        abbrv_w = tbl_w - name_w
        self.tbl_abbrv.setColumnWidth(0, name_w)
        self.tbl_abbrv.setColumnWidth(1, abbrv_w)

    def setup_abbrv_table(self):
        self.tbl_abbrv.setHorizontalHeaderLabels( ('Name', 'Abbreviation') )
        row = 0
        self.tbl_abbrv.setSortingEnabled(False)

        for n in sorted(self.client.empire.planet_names):
            itm_name = QTableWidgetItem(n)
            try:
                itm_abbrv = QTableWidgetItem(self.abbrv.get_abbrv(n))
            except KeyError as e:
                itm_abbrv = QTableWidgetItem("<None>")

            fl = itm_name.flags()
            fl &= ~Qt.ItemIsEditable
            itm_name.setFlags(fl)
            self.tbl_abbrv.insertRow(row)
            self.tbl_abbrv.setItem( row, 0, itm_name )
            self.tbl_abbrv.setItem( row, 1, itm_abbrv )
            row += 1

        self.resize_abbrv_table()
        self.tbl_abbrv.setSortingEnabled(True)
        self.tbl_abbrv.itemChanged.connect( self.update_abbrv )

    def update_abbrv(self, itm_abbrv):
        itm_name = self.tbl_abbrv.item( itm_abbrv.row(), 0 )
        self.abbrv.save( itm_name.text(), itm_abbrv.text() )

    def reset_gui(self, is_loggedout:bool = True):
        """ Resets all GUI elements.

        Arguments:
            is_loggedout (bool): Should we reset elements as if the user's 
            empire is logged out?  Defaults to True.
        """
        if is_loggedout:
            self.btn_login.setEnabled(True)
            self.btn_logout.setEnabled( False ) 
            self.btn_get_empire_status.setEnabled(False)
        self.tbl_abbrv.setRowCount(0)
        self.txt_status.setPlainText( "" )

    def update_config_status(self):
        if self.client:
            self.statusbar.showMessage("Logged in as {} from config file section {}." .format(self.client.empire.name, self.config_section))
        else:
            self.statusbar.showMessage("Using config file section {}.  Not currently logged in." .format(self.config_section))

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

