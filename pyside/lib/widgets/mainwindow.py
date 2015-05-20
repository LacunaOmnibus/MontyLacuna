
### Search on CHECK

import configparser, copy, os, sys, time
import lacuna, lacuna.exceptions as err
from lacuna.abbreviations import Abbreviations
from lacuna.utils import Utils
from PySide.QtGui import *
from PySide.QtCore import *
import gui
from gui import Ui_MainWindow
import widgets

import platform

class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        self.app            = QCoreApplication.instance()
        self.is_logged_in   = False
        self.ships_listed   = 0
        self.utils          = Utils()

        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.set_events()

        self.setWindowTitle( self.app.name )
        self.actionLog_In.setEnabled(True)
        self.actionLog_Out.setEnabled(False)
        self.btn_get_empire_status.setEnabled(False)
        self.btn_get_ships.setEnabled(False)
        self.add_graphical_toolbars()
        self.setup_abbrv_table()

    def add_graphical_toolbars(self):
        file_toolbar = self.addToolBar('File')
        self.actionConfig_File_Status.setIcon( QIcon(":/question.png") )
        self.actionLog_In.setIcon( QIcon(":/login.png") )
        self.actionLog_Out.setIcon( QIcon(":/logout.png") )
        self.actionQuit.setIcon( QIcon(":/close.png") )
        file_toolbar.addAction(self.actionLog_In)
        file_toolbar.addAction(self.actionConfig_File_Status)
        file_toolbar.addAction(self.actionLog_Out)
        file_toolbar.addSeparator()
        file_toolbar.addAction(self.actionQuit)


    def test(self, text="foo"):
        #print( self.app.popconf(self, "flurble?") )
        #self.app.poperr(self, "flurble!")
        self.app.popmsg(self, "flurble.")

    def set_events(self):
        self.btn_get_empire_status.clicked.connect( self.get_empire_status )
        self.btn_get_ships.clicked.connect( self.get_ships_summary )
        self.tabWidget.currentChanged.connect( self.tab_changed )
        self.actionAbout.activated.connect( self.show_about_dialog )
        self.actionChose_Config_File.activated.connect( self.chose_config_file )
        self.actionChose_Config_Section.activated.connect( self.chose_config_section )
        self.actionConfig_File_Status.activated.connect( self.update_config_status_throb )
        self.actionLog_In.activated.connect( self.do_login )
        self.actionLog_Out.activated.connect( self.do_logout )
        self.actionTest.activated.connect( self.test )

    def get_ships_summary(self):
        self.app.client.cache_on('my_ships', 3600)
        pname = self.cmb_planets.currentText()
        self.smsg("Getting planet...")
        planet = self.app.client.get_body_byname( pname )
        self.smsg("Getting ships...")
        sp = planet.get_buildings_bytype( 'spaceport', 1, 1, 100 )[0]
        self.app.client.cache_off()
        if not sp:
            self.poperr( "You don't have any working spaceports on {}!".format(pname) )
            return
        docked_ships, docks_free, docks_maxed = sp.view()
        self.add_ships_to_table( docked_ships )
        self.update_config_status();

    def add_ships_to_table(self, ships:dict):
        """ Adds ships to the ships table.

        Arguments:
            ships (dict): ``ship type (str) => quantity``
        """
        self.tbl_ships.setHorizontalHeaderLabels( ('Ship Type', 'Quantity', 'Num', 'Scuttle') )
        row = 0
        delete_buttons = {}
        for type in sorted( ships.keys() ):
            del_spinner = QSpinBox()
            del_spinner.setMinimum(0)
            del_spinner.setMaximum(ships[type])

### CHECK
### I think I need to promote tbl_ships from a TableWidget to a TableView and 
### see what happens there.
            btn_go = QPushButton("Go {}".format(type))
            btn_go.clicked.connect( lambda: self.scuttle_ships(row) )

            itm_type        = QTableWidgetItem(type)
            itm_num_avail   = QTableWidgetItem(str(ships[type]))
            self.tbl_ships.insertRow(row)
            self.tbl_ships.setItem(row, 0, itm_type)
            self.tbl_ships.setItem(row, 1, itm_num_avail)
            self.tbl_ships.setCellWidget(row, 2, del_spinner)
            self.tbl_ships.setCellWidget(row, 3, btn_go)
            row +=1
        self.ships_listed = row
        self.resize_ships_table(row)

    def scuttle_ships(self, row:int):
        print( "scuttle_ships {}".format(row) )

    def resize_ships_table(self, count = 0):
        """ Resizes the ships table.

        Arguments:
            count (int): The number of rows in the table.
        """
        tbl_w   = self.tbl_ships.width()
        if count > 0 and count < 10:
            ### Single-digit left number column
            tbl_w -= 20
        elif count >= 10:
            ### Double-digit left number column
            pass
            tbl_w -= 41
        if tbl_w > self.width():
            ### This happens during initial app display
            tbl_w = self.width() - 42
        type_w  = int(tbl_w * .35)
        quan_w  = int(tbl_w * .25)
        del_w   = int(tbl_w * .15)
        btn_w   = tbl_w - (type_w + quan_w + del_w)
        self.tbl_ships.setColumnWidth(0, type_w)
        self.tbl_ships.setColumnWidth(1, quan_w)
        self.tbl_ships.setColumnWidth(2, del_w)
        self.tbl_ships.setColumnWidth(3, btn_w)

    def clear_planets_combo_box(self):
        print( "clearing planets combo box" )
        pass

    def add_planets_to_combo_box(self):
        for pname in sorted( self.app.client.empire.colony_names.keys() ):
            self.cmb_planets.addItem( pname )
        self.cmb_planets.repaint()

    def resizeEvent(self, event):
        """ Called automatically when the app initializes, and then again any 
        time the main window gets resized.

        This doesn't actually get called until the user releases the mouse 
        button.  So during a resize event, it doesn't get called incessantly 
        every time the x/y changes, just at the end of the event.
        """
        self.resize_abbrv_table()
        self.resize_ships_table(self.ships_listed)

    def tab_changed(self, num):
        """ Called when the user switches to the third tab to force the table 
        to resize properly.
        """
        pass
        if num == 2:
            self.resize_abbrv_table()
        
    def chose_config_file(self):
        """ Allows the user to select an alternate config file by opening a 
        file chooser dialog.
        """
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
        self.smsg("Logging in...")
        self.app.login()
        self.reset_gui(True)
        self.statusbar.repaint()
        self.setup_abbrv_table()
        self.update_config_status()

    def do_logout(self):
        """ Logs out of TLE, then updates the GUI to reflect that logged-out status.
        """
        self.app.logout()
        self.reset_gui(False)
        self.update_config_status()

    def reset_gui(self, is_loggedin:bool = True):
        """ Resets all GUI elements.

        Arguments:
            is_loggedin (bool): Should we reset elements as if the user's 
            empire is logged in?  Defaults to True.
        """
        if is_loggedin:
            self.btn_get_empire_status.setEnabled(True)
            self.btn_get_ships.setEnabled(True)
            self.actionLog_In.setEnabled(False)
            self.actionLog_Out.setEnabled(True)
            self.add_planets_to_combo_box()
        else:
            self.btn_get_empire_status.setEnabled(False)
            self.btn_get_ships.setEnabled(False)
            self.actionLog_In.setEnabled(True)
            self.actionLog_Out.setEnabled(False)
            self.clear_planets_combo_box()
        self.tbl_abbrv.setRowCount(0)
        self.txt_status.setPlainText( "" )

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

    def smsg(self, message:str):
        self.statusbar.showMessage(message)
        self.statusbar.repaint()

    def update_abbrv(self, itm_abbrv):
        itm_name = self.tbl_abbrv.item( itm_abbrv.row(), 0 )
        self.app.abbrv.save( itm_name.text(), itm_abbrv.text() )

    def update_config_status_throb(self):
        self.update_config_status(True);

    def update_config_status(self, show_throbber:bool = False):
        """ Displays login status on the statusbar.

        Arguments:
            show_throbber (bool): If true, a little visual nonsense is diplayed to let the 
                                  user know something actually happened.
        """
        if show_throbber:
            self.smsg("")
            self.smsg("Checking status...")
            for i in range(0,10):
                time.sleep(0.1)
                self.app.processEvents()
            self.smsg("")

        if self.app.is_logged_in:
            self.smsg("Logged in as '{}' from config file section '{}'." .format(self.app.client.empire.name, self.app.config_section))
        else:
            self.smsg("Using config file section '{}'.  Not currently logged in." .format(self.app.config_section))
        self.statusbar.repaint()

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

