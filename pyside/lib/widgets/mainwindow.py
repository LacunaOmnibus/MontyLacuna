
### Search on CHECK

import configparser, copy, functools, os, sys, time
import lacuna, lacuna.exceptions as err
from lacuna.abbreviations import Abbreviations
from lacuna.utils import Utils
from PySide.QtGui import *
from PySide.QtCore import *
import gui
from gui import Ui_MainWindow
import widgets

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
        self.actionClear_All_Caches.setEnabled(False)

        self.add_graphical_toolbars()
    
        self.obj_cmb_colonies_scuttle = BodiesComboBox( self.cmb_planets, self )
        self.obj_tbl_abbrv = AbbreviationsTable( self.tbl_abbrv, self )
        self.obj_tbl_scuttle = ShipsDeleteTable( self.tbl_ships, self )

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
        self.actionChose_Config_File.activated.connect( self.chose_config_file )
        self.actionChose_Config_Section.activated.connect( self.chose_config_section )
        self.actionConfig_File_Status.activated.connect( self.update_config_status_throb )
        self.actionLog_In.activated.connect( self.do_login )
        self.actionLog_Out.activated.connect( self.do_logout )
        self.actionTest.activated.connect( self.test )

        self.actionAbout.activated.connect( self.show_about_dialog )
        self.actionClear_All_Caches.activated.connect( self.clear_caches )

    def clear_caches(self):
        if self.app.is_logged_in:
            self.parent.app.client.cache_clear('my_planets')
            self.parent.app.client.cache_clear('my_buildings')
            self.parent.app.client.cache_clear('my_ships')
            self.app.popmsg(self, "All caches have been cleared.")

    def get_ships_summary(self):
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
        self.obj_tbl_scuttle.resize(self.ships_listed)

    def tab_changed(self, num):
        """ Called when the user switches to the third tab to force the table 
        to resize properly.
        """
        pass
        if num == 2:
            self.obj_tbl_abbrv.resize()
        
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
        self.status("Logging in...")
        self.app.login()
        self.reset_gui(True)
        self.statusbar.repaint()
        self.obj_tbl_abbrv.reset()
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
            self.actionClear_All_Caches.setEnabled(True)
            self.obj_cmb_colonies_scuttle.add_colonies()
        else:
            self.btn_get_empire_status.setEnabled(False)
            self.btn_get_ships.setEnabled(False)
            self.actionLog_In.setEnabled(True)
            self.actionLog_Out.setEnabled(False)
            self.actionClear_All_Caches.setEnabled(False)
            self.obj_cmb_colonies_scuttle.clear()
        self.obj_tbl_abbrv.reset()
        self.obj_tbl_scuttle.reset()
        self.txt_status.setPlainText( "" )

    def status(self, message:str):
        self.statusbar.showMessage(message)
        self.statusbar.repaint()

    def update_config_status_throb(self):
        self.update_config_status(True);

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
        self.statusbar.repaint()

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
        self.txt_status.setPlainText( "\n".join(out) )

    def show_about_dialog(self):
        """ Displays the About dialog.

        Arguments:
            parent (QWidget): The dialog's parent.
        """
        dialog = widgets.About(self)
        dialog.show()


class AbbreviationsTable():
    """ Manages the table that handles body abbreviations.

    Arguments:
        table (QTableWidget): The actual table widget.
        parent (QWidget): The widget that owns the table widget.
    """

    def __init__(self, table:QTableWidget, parent:MainWindow):
        self.widget = table
        self.parent = parent
        self.reset()

    def clear(self):
        self.widget.clear()

    def reset(self):
        """ Resets the table contents to the correct size and headers, whether 
        we're logged in or not.
        """
        self.widget.setHorizontalHeaderLabels( ('Name', 'Abbreviation') )
        if self.parent.app.is_logged_in:
            ### Turn off sorting while we add items, then turn it back on 
            ### again when we're finished.
            self.widget.setSortingEnabled(False)
            row = 0
            for n in sorted(self.parent.app.client.empire.planet_names):
                itm_name = QTableWidgetItem(n)
                try:
                    itm_abbrv = QTableWidgetItem(self.parent.app.abbrv.get_abbrv(n))
                except KeyError as e:
                    itm_abbrv = QTableWidgetItem("<None>")
                fl = itm_name.flags()
                fl &= ~Qt.ItemIsEditable
                itm_name.setFlags(fl)
                self.widget.insertRow(row)
                self.widget.setItem( row, 0, itm_name )
                self.widget.setItem( row, 1, itm_abbrv )
                row += 1
            self.widget.setSortingEnabled(True)
        else:
            self.widget.setRowCount(0)
        self.resize()
        self.widget.itemChanged.connect( self.update )

    def resize(self):
        tbl_w   = self.widget.width()
        ### Have to modify the width a hair to avoid scrollbars.
        if self.parent.app.is_logged_in:
            tbl_w -= 50 # deals with left number column
        else:
            tbl_w -= 2  # deals with borders
        name_w  = int(tbl_w * .60)
        abbrv_w = tbl_w - name_w
        self.widget.setColumnWidth(0, name_w)
        self.widget.setColumnWidth(1, abbrv_w)

    def update(self, itm_abbrv):
        itm_name = self.widget.item( itm_abbrv.row(), 0 )
        self.parent.app.abbrv.save( itm_name.text(), itm_abbrv.text() )


class ShipsDeleteTable():
    """ Manages the table that handles ship scuttling.

    Arguments:
        table (QTableWidget): The actual table widget.
        parent (QWidget): The widget that owns the table widget.
    """

    main_stats = {
        "combat": [ 
            'bleeder', 'drone', 'fighter', 'observatory_seeker', 
            'security_ministry_seeker', 'spaceport_seeker', 'snark', 'snark2', 
            'snark3', 'sweeper', 'thud'
        ],
        "hold": [
            'barge', 'cargo_ship', 'dory', 'freighter', 'galleon', 'hulk',
            'hulk_fast', 'hulk_huge', 'scow', 'scow_fast', 'scow_mega'
        ],
        "stealth": [
            'scanner', 'smuggler_ship', 'spy_pod', 'spy_shuttle', 'surveyor'
        ]
    }

    def __init__(self, table:QTableWidget, parent:MainWindow):
        self.widget = table
        self.parent = parent
        self.planet = None
        self.reset()

    def add_ships_for(self, pname:str):
        """ Adds ship summaries to the table for a given planet name.

        Arguments:
            pname (str): The planet name

        Raises no exceptions, but will poperr and return if a working spaceport 
        could not be found.

        This *does* clear the table before adding more ships, since the list of 
        ships it adds is complete for the requested planet.
        """
        self.reset()    # clear it before adding more ships.
        self.parent.status("Getting planet...")
        planet_getter = GetPlanet( self.parent.app, pname )
        planet = planet_getter.request()

        self.parent.status("Getting spaceport...")
        bldg_getter = GetSingleBuilding( self.parent.app, planet, 'spaceport' )
        sp = bldg_getter.request()

        self.parent.status("Getting ships...")
        spviewer = GetSPView( self.parent.app, sp )
        docked_ships = spviewer.request()
        self.add_ships( docked_ships )
        self.parent.update_config_status();

    def add_ships(self, ships:dict):
        """ Adds ships to the table.

        Arguments:
            ships (dict): ``ship type (str) => quantity``

        This does *not* clear any existing entries before adding more ships. 
        If you want to pass an exhaustive dict, be sure to call ``reset`` first.
        """
        row = 0
        delete_buttons = {}
        for type in sorted( ships.keys() ):
            del_spinner = QSpinBox()
            del_spinner.setMinimum(0)
            del_spinner.setMaximum(ships[type])
            btn_go = QPushButton("Go")

            ### functools.partial locks the arg's current value to the method.  
            ### A regular Python lambda would be late-binding, so all button 
            ### clicks would indicate the same (last) row.
            btn_go.clicked.connect( functools.partial(self.scuttle, row) )

            itm_type        = QTableWidgetItem(type)
            itm_num_avail   = QTableWidgetItem("{:,}".format(ships[type]))
            self.widget.insertRow(row)
            self.widget.setItem(row, 0, itm_type)
            self.widget.setItem(row, 1, itm_num_avail)
            self.widget.setCellWidget(row, 2, del_spinner)
            self.widget.setCellWidget(row, 3, btn_go)
            row +=1
        self.ships_listed = row
        self.resize(row)

    def clear(self):
        """ Clears the table
        """
        self.widget.clear()

    def get_main_stat(self, shiptype:str):
        """ Gets the main statistic for a given shiptype.

        Arguments:
            type (str): The ship type (eg 'fighter', 'snark3', etc)
        Returns:
            stat (str): The most important stat for this type of ship.

        The "main stat" is not part of Lacuna, just a best guess at what's 
        best for a given type.  When deleting combat ships like sweepers, the 
        ships with the lowest combat scores will be deleted first.  For trade 
        ships like hulks, ships with the smallest hold size will go first.

        But some ships' best stats are arguable.  For Smugglers, this is going 
        to assume that stealth is the "main stat", but you might personally 
        prefer speed or hold size for those.  If that's the case, you'll need 
        to find another way to scuttle your ships.
        """
        if shiptype in self.main_stats['combat']:
            return 'combat'
        elif shiptype in self.main_stats['hold']:
            return 'hold'
        elif shiptype in self.main_stats['stealth']:
            return 'stealth'
        else:
            return 'speed'

    def reset(self):
        """ Resets the table contents to the correct size and headers
        """
        self.widget.setHorizontalHeaderLabels( ('Ship Type', 'Quantity', 'Num', 'Scuttle') )
        self.widget.setRowCount(0)
        self.resize()

    def resize(self, count = 0):
        """ Resizes the table.

        Arguments:
            count (int): The number of rows in the table.
        """
        tbl_w   = self.widget.width()
        if count == 0:
            tbl_w -= 2                          # No number column, but borders.
        elif count < 10:
            tbl_w -= 20                         # Single-digit left number column
        elif count >= 10:
            pass                                # Double-digit left number column
            tbl_w -= 41
        if tbl_w > self.parent.width():
            tbl_w = self.parent.width() - 42    # This happens during initial app display
        type_w  = int(tbl_w * .35)
        quan_w  = int(tbl_w * .25)
        del_w   = int(tbl_w * .15)
        btn_w   = tbl_w - (type_w + quan_w + del_w)
        self.widget.setColumnWidth(0, type_w)
        self.widget.setColumnWidth(1, quan_w)
        self.widget.setColumnWidth(2, del_w)
        self.widget.setColumnWidth(3, btn_w)

    def scuttle(self, row:int):
        """ Scuttles the ships indicated by the settings on the indicated row.

        Arguments:
            row (int): Data from this table row (zero-indexed) will be pulled 
                       and the corresponding ships will be scuttled.
        """
        lbl_type    = self.widget.item(row, 0)
        lbl_ttl     = self.widget.item(row, 1)
        spin_del    = self.widget.cellWidget(row, 2)

        self.parent.status("Getting planet...")
        pname = self.parent.obj_cmb_colonies_scuttle.currentText()
        planet_getter = GetPlanet( self.parent.app, pname )
        planet = planet_getter.request()

        self.parent.status("Getting spaceport...")
        bldg_getter = GetSingleBuilding( self.parent.app, planet, 'spaceport' )
        sp = bldg_getter.request()

        self.parent.status("Getting ships...")
        paging  = { 'no_paging': 1 }
        filter  = { 'type': lbl_type.text(), 'task': 'Docked' } # tested - combined filter _does_ work
        sort    = self.get_main_stat( lbl_type.text() )
        ### At this point, we definitely need fresh data.
        ships_getter = GetAllShipsView( self.parent.app, sp, paging, filter, sort, fresh = True )
        ships = ships_getter.request()
        ships.reverse() # sorted desc from the server; flip that to asc.

        delete_these = []
        for i in range(0, spin_del.value() ):
            delete_these.append( ships[i].id )
        ships_scuttler = MassShipScuttler( self.parent.app, sp, delete_these )
        ships_scuttler.request()
        #sp.mass_scuttle_ship( delete_these )
        self.parent.app.client.cache_clear('my_ships')
        self.parent.app.popmsg(self.parent, "I just scuttled {} ships of type {}."
            .format( len(delete_these), lbl_type.text() )
        )
        self.add_ships_for(pname)

class BodiesComboBox():
    """ Manages a combo box containing body names

    Arguments:
        combo (QTableWidget): The actual table widget.
        parent (QWidget): The widget that owns the table widget.
    """

    def __init__(self, combo:QComboBox, parent:MainWindow):
        self.widget = combo
        self.parent = parent

    def add_colonies(self):
        """ Add colony names owned by the current client's empire to the combo box
        """
        for pname in sorted( self.parent.app.client.empire.colony_names.keys() ):
            self.widget.addItem( pname )
        self.widget.repaint()

    def currentText(self):
        """ Get the current text (body name) from the combo box
        """
        return self.widget.currentText()

    def clear(self):
        """ Clear the combo box
        """
        self.widget.clear()


###########################
# Threaded TLE requestors #
###########################

class GetPlanet(QThread):
    dataReady = Signal(object)

    def __init__(self, app, pname, fresh = False, parent = None):
        QThread.__init__(self, parent)
        self.app    = app
        self.fresh  = fresh
        self.pname  = pname
        self.planet = None

    def request(self):
        self.start()    # Automatically calls run()
        while(self.isRunning()):
            self.app.processEvents()
            time.sleep(0.1)
        return self.planet

    def run(self):
        if self.fresh:
            self.app.client.cache_clear('my_planets')
        self.app.client.cache_on('my_planets', 3600)
        self.planet = self.app.client.get_body_byname( self.pname )
        self.dataReady.emit(self.planet) 

class GetSingleBuilding(QThread):
    dataReady = Signal(object)

    def __init__(self, app, planet, btype, fresh = False, parent = None):
        QThread.__init__(self, parent)
        self.app    = app
        self.bldg   = None
        self.btype  = btype
        self.fresh  = fresh
        self.planet = planet

    def request(self):
        self.start()
        while(self.isRunning()):
            self.app.processEvents()
            time.sleep(0.1)
        return self.bldg

    def run(self):
        if self.fresh:
            self.app.client.cache_clear('my_buildings')
        self.app.client.cache_on('my_buildings', 3600)
        try:
            self.bldg = self.planet.get_buildings_bytype( self.btype, 1, 1, 100 )[0]
        except err.NoSuchBuildingError as e:
            self.app.poperr(self.parent, "You don't have a working spaceport")
            return
        self.dataReady.emit(self.bldg) 


class GetAllShipsView(QThread):
    dataReady = Signal(object)

    def __init__(self, app,
        sp, paging:dict = {}, filter:dict = {}, sort:str = None, fresh = False, 
        parent = None
    ):
        QThread.__init__(self, parent)
        self.app    = app
        self.filter = filter
        self.fresh  = fresh
        self.paging = paging
        self.ships  = []
        self.sort   = sort
        self.sp     = sp

    def request(self):
        self.start()
        while(self.isRunning()):
            self.app.processEvents()
            time.sleep(0.1)
        return self.ships

    def run(self):
        if self.fresh:
            self.app.client.cache_clear('my_ships')
        self.app.client.cache_on('my_ships', 3600)
        self.ships, cnt = self.sp.view_all_ships(self.paging, self.filter, self.sort)
        self.dataReady.emit(self.ships) 


class MassShipScuttler(QThread):
    dataReady = Signal(object)

    def __init__(self, app, sp, ship_ids:list, parent = None):
        QThread.__init__(self, parent)
        self.app    = app
        self.ids    = ship_ids
        self.sp     = sp

    def request(self):
        self.start()
        while(self.isRunning()):
            self.app.processEvents()
            time.sleep(0.1)
        return self.ids

    def run(self):
        self.sp.mass_scuttle_ship( self.ids )
        self.dataReady.emit(True) 


class GetSPView(QThread):
    dataReady = Signal(object)

    def __init__(self, app, sp, fresh = False, parent = None):
        QThread.__init__(self, parent)
        self.app        = app
        self.fresh      = fresh
        self.ships      = []
        self.docks_free = None
        self.docks_max  = None
        self.sp         = sp

    def request(self):
        self.start()
        while(self.isRunning()):
            self.app.processEvents()
            time.sleep(0.1)
        return self.ships

    def run(self):
        if self.fresh:
            self.app.client.cache_clear('my_ships')
        self.app.client.cache_on('my_ships', 3600)
        self.ships, self.docks_free, self.docks_max = self.sp.view()
        self.dataReady.emit(self.ships) 

