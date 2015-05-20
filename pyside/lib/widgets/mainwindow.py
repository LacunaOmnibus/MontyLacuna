
### Search on CHECK

import configparser, os, sys
import lacuna, lacuna.exceptions as err
from lacuna.abbreviations import Abbreviations
from lacuna.utils import Utils
### I may just end up with "import *" below.
from PySide.QtGui import QApplication, QFileDialog, QIcon, QMainWindow, QTableWidgetItem
from PySide.QtCore import *
import gui
from gui import Ui_MainWindow
import widgets

import platform

class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        self.app            = QCoreApplication.instance()
        self.is_logged_in   = False
        self.utils          = Utils()

        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle( self.app.name )
        self.set_events()

        self.add_graphical_toolbars()
        self.setup_abbrv_table()
        self.btn_get_empire_status.setEnabled(False)

    def add_graphical_toolbars(self):
        ### This is mostly just for testing multiple toolbars.  I certainly 
        ### don't need a toolbar for the About window.
        file_toolbar = self.addToolBar('File')
        self.actionChose_Config_File.setIcon( QIcon(":/file.png") )
        self.actionChose_Config_Section.setIcon( QIcon(":/section.png") )
        self.actionConfig_File_Status.setIcon( QIcon(":/question.png") )
        self.actionLog_In.setIcon( QIcon(":/login.png") )
        self.actionLog_Out.setIcon( QIcon(":/logout.png") )
        self.actionQuit.setIcon( QIcon(":/close.png") )
        file_toolbar.addAction(self.actionChose_Config_File)
        file_toolbar.addAction(self.actionChose_Config_Section)
        file_toolbar.addAction(self.actionConfig_File_Status)
        file_toolbar.addAction(self.actionLog_In)
        file_toolbar.addAction(self.actionLog_Out)
        file_toolbar.addAction(self.actionQuit)

        help_toolbar = self.addToolBar('Help')
        self.actionAbout.setIcon( QIcon(":/about.png") )
        help_toolbar.addAction(self.actionAbout)

    def test(self, text="foo"):
        #print( self.app.popconf(self, "flurble?") )
        #self.app.poperr(self, "flurble!")
        self.app.popmsg(self, "flurble.")

    def set_events(self):
        self.btn_login.clicked.connect( self.do_login )
        self.btn_logout.clicked.connect( self.do_logout )
        self.btn_logout.setEnabled( False ) 
        self.btn_get_empire_status.clicked.connect( self.get_empire_status )
        self.tabWidget.currentChanged.connect( self.tab_changed )
        self.btn_check_status.clicked.connect( self.update_config_status )
        self.actionAbout.activated.connect( self.show_about_dialog )
        self.actionChose_Config_File.activated.connect( self.chose_config_file )
        self.actionChose_Config_Section.activated.connect( self.chose_config_section )
        self.actionConfig_File_Status.activated.connect( self.update_config_status )
        self.actionConfig_File_Status.activated.connect( self.update_config_status )
        self.actionLog_In.activated.connect( self.do_login )
        self.actionLog_Out.activated.connect( self.do_logout )
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
        
    def chose_config_file(self):
        file, filter = QFileDialog.getOpenFileName( self, "Open Image", self.app.instdir + "/etc", "Config Files (*.cfg)" )
        if file:
            self.app.config_file = file
        self.do_logout();

    def chose_config_section(self):
        """ Opens a list widget containing available sections of the current config file.
        """
        try:
            cp = self.app.readconfig()
        except IOError as e:
            self.app.poperr(self, "'{}' is not a valid config file; please choose one first.".format(self.app.config_file))
            return
        self.do_logout();
        mylist = [i for i in sorted(cp) if i is not 'DEFAULT']
        pick = widgets.PickList( self )
        pick.add( mylist )
        rv = pick.pickone() # -sitter-, -real-, etc, but might also be None if user didn't pick anything.
        if rv:
            if rv != self.app.config_section:
                self.do_logout()
            self.app.config_section = rv
        self.update_config_status()

    def do_login(self):
        """ Logs in to TLE, then updates the GUI to reflect that logged-in status.
        """
        self.app.login()
        self.statusbar.showMessage("Logging in...")
        self.statusbar.repaint()
        self.setup_abbrv_table()
        self.btn_login.setEnabled(False)
        self.btn_logout.setEnabled( True ) 
        self.btn_get_empire_status.setEnabled(True)
        self.update_config_status()

    def do_logout(self):
        """ Logs out of TLE, then updates the GUI to reflect that logged-out status.
        """
        self.app.logout()
        self.reset_gui()
        self.update_config_status()

    def resize_abbrv_table(self):
        tbl_w   = self.tbl_abbrv.width()
        if self.app.is_logged_in:
            ### Subtract 50 to account for the line number column on the left, 
            ### which will only be shown if the user is logged in.
            tbl_w -= 50
        name_w  = int(tbl_w * .60)
        abbrv_w = tbl_w - name_w
        self.tbl_abbrv.setColumnWidth(0, name_w)
        self.tbl_abbrv.setColumnWidth(1, abbrv_w)

    def setup_abbrv_table(self):
        self.tbl_abbrv.setHorizontalHeaderLabels( ('Name', 'Abbreviation') )

        if self.app.is_logged_in:
            ### Turn off sorting while we add items, then turn it back on 
            ### again when we're finished.
            self.tbl_abbrv.setSortingEnabled(False)
            row = 0
            for n in sorted(self.app.client.empire.planet_names):
                itm_name = QTableWidgetItem(n)
                try:
                    itm_abbrv = QTableWidgetItem(self.app.abbrv.get_abbrv(n))
                except KeyError as e:
                    itm_abbrv = QTableWidgetItem("<None>")
                fl = itm_name.flags()
                fl &= ~Qt.ItemIsEditable
                itm_name.setFlags(fl)
                self.tbl_abbrv.insertRow(row)
                self.tbl_abbrv.setItem( row, 0, itm_name )
                self.tbl_abbrv.setItem( row, 1, itm_abbrv )
                row += 1
            self.tbl_abbrv.setSortingEnabled(True)

        self.resize_abbrv_table()
        self.tbl_abbrv.itemChanged.connect( self.update_abbrv )

    def update_abbrv(self, itm_abbrv):
        itm_name = self.tbl_abbrv.item( itm_abbrv.row(), 0 )
        self.app.abbrv.save( itm_name.text(), itm_abbrv.text() )

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
        if self.app.is_logged_in:
            self.statusbar.showMessage("Logged in as '{}' from config file section '{}'." .format(self.app.client.empire.name, self.app.config_section))
        else:
            self.statusbar.showMessage("Using config file section '{}'.  Not currently logged in." .format(self.app.config_section))

    def get_empire_status(self):
        if not self.app.is_logged_in:
            self.app.poperr(self, "You must log in first.")
            return
        out = []
        if int(self.app.client.empire.self_destruct_active) > 0:
            out.append("*** SELF DESTRUCT IS ACTIVE! ***")
            out.append("")
        out.append("ID: " + self.app.client.empire.id )
        out.append("RPC Usage: " + str(self.app.client.empire.rpc_count) )
        out.append("Status Message: " + self.app.client.empire.status_message )
        out.append("New Mail Messages: " + str(self.app.client.empire.has_new_messages) )
        out.append("Essentia: " + str(self.app.client.empire.essentia) )
        out.append("Tech Level: " + str(self.app.client.empire.tech_level) )
        out.append("")
        out.append("Planets: ")
        for p in sorted( self.app.client.empire.colony_names.keys() ):
            out.append("\t" + p)
        self.txt_status.setPlainText( "\n".join(out) )

    def show_about_dialog(self):
        """ Displays the About dialog.

        Arguments:
            parent (QWidget): The dialog's parent.
        """
        dialog = widgets.About(self)
        dialog.show()

