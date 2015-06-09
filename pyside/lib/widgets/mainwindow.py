
import configparser, copy, functools, os, pytz, sys, time
import lacuna, lacuna.exceptions as err
from lacuna.abbreviations import Abbreviations
from lacuna.utils import Utils

from PySide.QtGui import *
from PySide.QtCore import *

import gui
from gui import Ui_MainWindow

from appthreads import *

import widgets

class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        self.app            = QCoreApplication.instance()
        self.is_logged_in   = False
        self.play_sounds    = True
        self.utils          = Utils()
        ### UI initialization
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        ### UI customization
        self.setWindowTitle( self.app.name )
        self.actionLog_In.setEnabled(True)
        self.actionLog_Out.setEnabled(False)
        self.btn_build_ships.setEnabled(False)
        self.btn_get_empire_status.setEnabled(False)
        self.btn_get_ships_scuttle.setEnabled(False)
        self.btn_get_shipyards_build.setEnabled(False)
        self.actionClear_All_Caches.setEnabled(False)
        self.add_graphical_toolbars()
        self.soundon()
        ### Set up more complex widgets
        self.obj_cmb_colonies_scuttle   = widgets.BodiesComboBox( self.cmb_planets_scuttle, self )
        self.obj_cmb_colonies_build     = widgets.BodiesComboBox( self.cmb_planets_build, self )
        self.obj_tbl_abbrv              = widgets.AbbreviationsTable( self.tbl_abbrv, self )
        self.obj_tbl_sy_build           = widgets.ShipyardsTable( self.tbl_shipyards_build, self )
        self.obj_tbl_buildable_ships    = widgets.BuildableShipsTable( self.tbl_ships_build, self )
        self.obj_tbl_scuttle            = widgets.ShipsDeleteTable( self.tbl_ships_scuttle, self )
        ### Set events on all of the widgets
        self.set_events()

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
        self.btn_build_ships.clicked.connect( self.build_ships )
        self.btn_get_empire_status.clicked.connect( self.get_empire_status )
        self.btn_get_ships_scuttle.clicked.connect( self.get_ships_for_scuttle )
        self.btn_get_shipyards_build.clicked.connect( self.get_shipyards_for_build )
        self.tabWidget.currentChanged.connect( self.tab_changed )
        self.actionChose_Config_File.activated.connect( self.chose_config_file )
        self.actionChose_Config_Section.activated.connect( self.chose_config_section )
        self.actionConfig_File_Status.activated.connect( self.update_config_status_throb )
        self.actionMute.activated.connect( self.soundoff )
        self.actionUnmute.activated.connect( self.soundon )
        self.actionLog_In.activated.connect( self.do_login )
        self.actionLog_Out.activated.connect( self.do_logout )
        self.actionTest.activated.connect( self.test )
        self.actionAbout.activated.connect( self.show_about_dialog )
        self.actionClear_All_Caches.activated.connect( self.clear_caches )

    def timertest(self):
        print( "in timertest" )

    def get_shipyards_for_build(self):
        """ Modifies two tables - the list of shipyards on the planet, and the 
        list of buildable ships (based on what the first shipyard is able to 
        build).
        """
        pname = self.obj_cmb_colonies_build.currentText()

        ### Get number of available ports
        ###     List in lbl_build_ports_available

        ### Get SY objects
        ###     List in obj_tbl_sy_build
        self.obj_tbl_sy_build.add_shipyards_for(pname)

        ### Get buildable ships
        self.obj_tbl_buildable_ships.add_ships( self.obj_tbl_sy_build.shipyards )

    def build_ships(self):
        ###
        ### I should probably add a shipyards_tab.py to contain all of this 
        ### stuff.
        ###

        ### Get active shipyards from obj_tbl_sy_build
        shipyards = self.obj_tbl_sy_build.get_included_shipyards()

        ### Get types and numbers to build from obj_tbl_buildable_ships
        ships_dict, num_left_to_build = self.obj_tbl_buildable_ships.get_ships_to_build()

        ### In a thread, start building those ships at those shipyards.
        ### 
        ### This currently works - build 31 barges and 2 cargo ships on 
        ### bmots01 (with one SY), and it builds 30, sleeps the correct amount 
        ### of time, then builds one more barge and the 2 cargos.
        ### 
        ### TBD CHECK
        ###
        ### DON'T DO ANY OF THIS YET.  First, move all code relating to the 
        ### Build Ships tab off to its own module.  This one is getting messy.
        ###  
        ### - If the user doesn't click any SY checkboxes before clicking the 
        ###   Build! button, poperr() and bail.
        ###
        ### - should respond to a "cancel all queues" request.
        ###     - Maybe we just set ship_builder.quit to a true value, and 
        ###       have the thread check for that just before it runs, and end 
        ###       itself if it sees that.  Not sure yet.
        ###
        ### - After a ship_builder is created for a given planet, that builder 
        ###   should get cached in a dict somewhere, keyed of the planet name 
        ###   (or ID probably).  When the Build Ships tab is brought up for a 
        ###   specific planet, if there's an existing ship_builder for that 
        ###   planet, the entire interface should be greyed out.
        ###
        ### - There's a label on that Build Ships tab just under the select 
        ###   box and Get shipyards button (it has no text now).  For planets 
        ###   that are not currently building anything, it should show 
        ###   available/maxed docks counts (spaceport.view()).  For planets 
        ###   that _are_ currently building, it should show the number and 
        ###   type left in the queue.
        ### 
        ### - Count up the number of ships the user's trying to build.  If 
        ###   it's greater than the number of available docs, just poperr() 
        ###   and don't build anything so they can fix their numbers.
        ### 
        ### - Once a builder is finished, it should close down.  I'm currently 
        ###   leaving the thread open.
        ###
        self.status("Adding ships to your build queues...")
        ship_builder = BuildShipsInYards( self.app, shipyards, ships_dict )
        self._set_shipbuild_thread( ship_builder )

        #print( ship_builder.ships ) # works 
        self.update_config_status()

    def _set_shipbuild_thread(self, builder):
        recall_time = builder.request()    # datetime.datetime
        if recall_time:
            recall_time = recall_time.replace(tzinfo=pytz.UTC)
            sleeptime_ms = self.app.get_ms_until(recall_time)
            timer = QTimer(self)
            timer.setSingleShot(True)
            timer.timeout.connect( lambda: self._set_shipbuild_thread(builder) )
            timer.start(sleeptime_ms)
            
    def soundon(self):
        self.play_sounds = True
        self.actionMute.setEnabled(True)
        self.actionUnmute.setEnabled(False)

    def soundoff(self):
        self.play_sounds = False
        self.actionMute.setEnabled(False)
        self.actionUnmute.setEnabled(True)

    def clear_caches(self):
        if self.app.is_logged_in:
            self.app.client.cache_clear('my_planets')
            self.app.client.cache_clear('my_buildings')
            self.app.client.cache_clear('my_ships')
            self.app.popmsg(self, "All caches have been cleared.")

    def get_ships_for_scuttle(self):
        pname = self.obj_cmb_colonies_scuttle.currentText()
        self.obj_tbl_scuttle.add_ships_for(pname)

    def resizeEvent(self, event):
        """ Called automatically when the app initializes, and then again any 
        time the main window gets resized.

        This doesn't actually get called until the user releases the mouse 
        button.  So during a resize event, it doesn't get called incessantly 
        every time the x/y changes, just at the end of the event.
        """
        self.obj_tbl_abbrv.resize()
        self.obj_tbl_scuttle.resize()
        self.obj_tbl_sy_build.resize()
        self.obj_tbl_buildable_ships.resize()

    def tab_changed(self, num):
        """ Resizes a tab's contents when a user clicks on it.

        The resizeEvent resizes its contents properly only for the 
        currently-visible tab.  Widgets in inactive tabs do get resized, but 
        never correctly; there's always a bit of a gap.

        By forcing a resize() call when the table's tab is clicked, the table 
        always just looks right to the user.
        """
        if num == 0:
            self.obj_tbl_sy_build.resize()
        elif num == 1:
            self.obj_tbl_scuttle.resize()
        elif num == 3:
            self.obj_tbl_abbrv.resize()
        
    def chose_config_file(self):
        """ Allows the user to select an alternate config file by opening a 
        file chooser dialog.
        """
        file, filter = QFileDialog.getOpenFileName( self, "Open Image", self.app.instdir + "/etc", "Config Files (*.cfg)" )
        if file:
            self.app.config_file = file
            self.do_logout();
        else:
            ### If file comes back false, the user hit Cancel on the file 
            ### chooser dialog, in which case we don't do anything.
            pass

    def chose_config_section(self):
        """ Opens a list widget containing available sections of the current config file.
        """
        try:
            cp = self.app.readconfig()
        except IOError as e:
            self.app.poperr(self, "'{}' is not a valid config file; please choose one first.".format(self.app.config_file))
            return
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
        self.status("Logging in...")
        self.app.login()
        if self.play_sounds:
            self.app.play_sound('door.wav')
        self.reset_gui(True)
        self.statusbar.repaint()
        self.obj_tbl_abbrv.set_abbreviations( self.app.client.empire )
        self.update_config_status()

    def do_logout(self):
        """ Logs out of TLE, then updates the GUI to reflect that logged-out status.
        """
        self.app.logout()
        if self.play_sounds:
            self.app.play_sound('livelong.wav')
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
            self.btn_get_ships_scuttle.setEnabled(True)
            self.btn_get_shipyards_build.setEnabled(True)
            self.actionLog_In.setEnabled(False)
            self.actionLog_Out.setEnabled(True)
            self.actionClear_All_Caches.setEnabled(True)
            self.obj_cmb_colonies_scuttle.add_colonies()
            self.obj_cmb_colonies_build.add_colonies()
        else:
            self.btn_build_ships.setEnabled(False)
            self.btn_get_empire_status.setEnabled(False)
            self.btn_get_ships_scuttle.setEnabled(False)
            self.btn_get_shipyards_build.setEnabled(False)
            self.actionLog_In.setEnabled(True)
            self.actionLog_Out.setEnabled(False)
            self.actionClear_All_Caches.setEnabled(False)
            self.obj_cmb_colonies_scuttle.clear()
            self.obj_cmb_colonies_build.clear()
            self.obj_tbl_sy_build.clear()
            self.obj_tbl_scuttle.clear()
            self.obj_tbl_buildable_ships.clear()
            self.obj_tbl_abbrv.clear()
            self.txt_empire_status.setPlainText( "" )

    def status(self, message:str):
        """ Display a message in the status bar.

        Arguments:
            message (str): The message to display.
        Returns:
            prev_msg (str): The message that your new message replaced.  Might be the 
                            empty string.
        """
        msg = self.statusbar.currentMessage()
        self.statusbar.showMessage(message)
        self.statusbar.repaint()
        return msg

    def update_config_status_throb(self):
        self.update_config_status(True);
        if self.play_sounds:
            self.app.play_sound('intercom.wav')

    def update_config_status(self, show_throbber:bool = False):
        """ Displays login status on the statusbar.

        Arguments:
            show_throbber (bool): If true, a little visual nonsense is diplayed to let the 
                                  user know something actually happened.
        """
        if show_throbber:
            self.status("")
            self.status("Checking status...")
            for i in range(0,10):
                time.sleep(0.1)
                self.app.processEvents()
            self.status("")

        if self.app.is_logged_in:
            self.status("Logged in as '{}' from config file section '{}'." .format(self.app.client.empire.name, self.app.config_section))
        else:
            self.status("Using config file section '{}'.  Not currently logged in." .format(self.app.config_section))

    def get_empire_status(self):
        if not self.app.is_logged_in:
            self.app.poperr(self, "You must log in first.")
            return
        out = []
        if int(self.app.client.empire.self_destruct_active) > 0:
            out.append("*** SELF DESTRUCT IS ACTIVE! ***")
            out.append("")
        out.append("ID: {}".format(self.app.client.empire.id) )
        out.append("RPC Usage: {}".format(self.app.client.empire.rpc_count) )
        out.append("Status Message: {}".format(self.app.client.empire.status_message) )
        out.append("New Mail Messages: {}".format(self.app.client.empire.has_new_messages) )
        out.append("Essentia: {}".format(self.app.client.empire.essentia) )
        out.append("Tech Level: {}".format(self.app.client.empire.tech_level) )
        out.append("")
        out.append("Planets: ")
        for p in sorted( self.app.client.empire.colony_names.keys() ):
            out.append("\t" + p)
        self.txt_empire_status.setPlainText( "\n".join(out) )

    def show_about_dialog(self):
        """ Displays the About dialog.

        Arguments:
            parent (QWidget): The dialog's parent.
        """
        dialog = widgets.About(self)
        dialog.show()

