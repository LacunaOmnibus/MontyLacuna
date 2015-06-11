
import pytz

from PySide.QtGui import *
from PySide.QtCore import *

from appthreads import *
import widgets

class BuildShipsTab():
    """ The contents of the Build Ships tab.

    Most classes representing a piece of the GUI have a ``self.widget`` 
    attribute, which contains the actual Qt widget that the class represents.

    However, a single tab is not, itself, a widget.  The QTabWidget is the 
    widget that creates and manages the tabs, but the individual tabs are just 
    pieces of that parent widget.
    """

    def __init__( self, tab_holder:QTabWidget, main_window:QMainWindow ):
        self.mw             = main_window
        self.tab_holder     = tab_holder

        self.builders       = {}    # planet_id => BuildShipsInYards() objects; filled by build_ships()
        self.planet         = None  # lacuna body object; filled by get_shipyards_for_build
        self.sp             = None  # spaceport; filled by get_shipyards_for_build
        self.view_getter    = None  # spaceport view() thread; filled by get_shipyards_for_build

        self.mw.btn_build_ships.setEnabled(False)
        self.obj_cmb_colonies_build     = widgets.BodiesComboBox( self.mw.cmb_planets_build, self.mw )
        self.obj_tbl_sy_build           = widgets.tabs.ShipyardsTable( self.mw.tbl_shipyards_build, self.mw )
        self.obj_tbl_buildable_ships    = widgets.tabs.BuildableShipsTable( self.mw.tbl_ships_build, self.mw )

        self._init_ui()
        self._set_events()

    def _init_ui(self):
        self.mw.btn_get_shipyards_build.setEnabled(False)

    def _set_events(self):
        self.mw.btn_get_shipyards_build.clicked.connect( self.get_shipyards_for_build )
        self.mw.btn_build_ships.clicked.connect( self.build_ships )

    def adjust_gui_login(self):
        self.mw.btn_get_shipyards_build.setEnabled(True)
        self.obj_cmb_colonies_build.add_colonies()
        self.sp             = None
        self.view_getter    = None

    def adjust_gui_logout(self):
        self.mw.btn_get_shipyards_build.setEnabled(False)
        self.self.mw.btn_build_ships.setEnabled(False)
        self.obj_cmb_colonies_build.clear()
        self.obj_tbl_sy_build.clear()
        self.obj_tbl_buildable_ships.clear()
        self.sp             = None
        self.view_getter    = None

    def disable_ui(self):
        """ Disables all widgets on the tab.
        """
        self.mw.btn_get_shipyards_build.setEnabled(False)
        self.mw.btn_build_ships.setEnabled(False)
        self.mw.lbl_build_ports_available.setEnabled(False)
        self.obj_cmb_colonies_build.setEnabled(False)
        self.obj_tbl_sy_build.setEnabled(False)
        self.obj_tbl_buildable_ships.setEnabled(False)

    def enable_ui(self):
        """ Enables all widgets on the tab.
        """
        self.mw.btn_get_shipyards_build.setEnabled(True)
        self.mw.btn_build_ships.setEnabled(True)
        self.mw.lbl_build_ports_available.setEnabled(True)
        self.obj_cmb_colonies_build.setEnabled(True)
        self.obj_tbl_sy_build.setEnabled(True)
        self.obj_tbl_buildable_ships.setEnabled(True)

    def resize(self):
        self.obj_tbl_sy_build.resize()
        self.obj_tbl_buildable_ships.resize()

    def build_ships(self):
        self.disable_ui()

        ### Get active shipyards from obj_tbl_sy_build
        shipyards = self.obj_tbl_sy_build.get_included_shipyards()
        if not shipyards:
            self.mw.app.poperr(self.mw, "You must select the shipyard or yards at which to build ships by checking their checkboxes first.")
            return

        ### Get types and numbers to build from obj_tbl_buildable_ships
        ships_dict, num_left_to_build = self.obj_tbl_buildable_ships.get_ships_to_build()
        if self.obj_tbl_buildable_ships.available_docks is not None:
            if num_left_to_build > self.obj_tbl_buildable_ships.available_docks:
                ### Even with the spinners in the buildable ships table 
                ### checking for overrun, all they're doing is popping an 
                ### error at the user.  The user might ignore the warning or 
                ### just be bad at math and try building anyway.
                self.mw.app.poperr(self.mw, 
                    "You're trying to build more ships than you have available docks!"
                )
                return

        ### In a thread, start building those ships at those shipyards.
        ### 
        ### This currently works - build 31 barges and 2 cargo ships on 
        ### bmots01 (with one SY), and it builds 30, sleeps the correct amount 
        ### of time, then builds one more barge and the 2 cargos.
        ### 
        ### TBD CHECK
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
        ###   that are currently building, it should show the number and type 
        ###   left in the queue. (or maybe just the number; there's not a lot 
        ###   of space in that label.)
        ### 
        ### - Once a builder is finished, it should close down.  I'm currently 
        ###   leaving the thread open.
        ###
        self.mw.status("Adding ships to your build queues...")
        if not self.planet.name in self.builders:
            self.builders[self.planet.id] = BuildShipsInYards( self.mw.app, self.planet.id, shipyards, ships_dict )
            self.builders[self.planet.id].sig_empty.connect( self._build_thread_isempty )
        self._set_shipbuild_thread( self.builders[self.planet.id] )
        self.mw.update_config_status()
        ui_should_be_enabled = self.update_docks_label()
        if ui_should_be_enabled:
            self.enable_ui()

    def _build_thread_isempty(self, planet_id ):
        if planet_id in self.builders:
            del(self.builders[planet_id])

        ### Doing this would re-enable the UI when any build thread ends, 
        ### regardles of what planet's shipyards we're currently looking at, 
        ### so don't do this.
        #self.enable_ui()
        ### Once the UI has been disabled because a build thread is in 
        ### progress, I'm going to decide that the user has to refresh that 
        ### planet's view to get the UI back rather than having it be 
        ### automatic.


    def _set_shipbuild_thread(self, builder):
        recall_time = builder.request()    # datetime.datetime
        if recall_time:
            recall_time = recall_time.replace(tzinfo=pytz.UTC)
            sleeptime_ms = self.mw.app.get_ms_until(recall_time)
            timer = QTimer(self.mw)
            timer.setSingleShot(True)
            timer.timeout.connect( lambda: self._set_shipbuild_thread(builder) )
            timer.start(sleeptime_ms)

    def update_docks_label(self):
        """ Updates the QLabel with either the number of available docks, or a note 
        stating that a build thread is currently active.

        Returns:
            ui_should_become_enabled (bool): Whether or not we should re-enable the UI.
                                             If a build thread is currently active, this 
                                             will return False.
        """
        ui_should_become_enabled = True
        ### CHECK
        ### This eventually should be able to know whether we've got a build 
        ### ships thread working or not.  If we do, this should display how 
        ### many ships are left in our queue (not in the actual shipyard queue 
        ### in-game, how many are left to be added to that shipyard queue).
        if self.planet:
            if self.planet.id in self.builders:
                if self.builders[self.planet.id]:
                    self.mw.lbl_build_ports_available.setText( "This planet currently has a build already scheduled." )
                    ui_should_become_enabled = False
                    return ui_should_become_enabled

        if self.view_getter:
            self.view_getter.request()
            self.mw.lbl_build_ports_available.setText(
                "{} of {} docks are available."
                .format(self.view_getter.docks_free, self.view_getter.docks_max)
            )
        return ui_should_become_enabled

    def get_shipyards_for_build(self):
        """ Modifies two tables - the list of shipyards on the planet, and the 
        list of buildable ships (based on what the first shipyard is able to 
        build).
        """
        self.disable_ui()
        pname = self.obj_cmb_colonies_build.currentText()

        self.mw.status("Getting planet...")
        planet_getter = GetPlanet( self.mw.app, pname )
        self.planet = planet_getter.request()

        self.mw.status("Getting shipyards...")
        self.obj_tbl_sy_build.add_shipyards_for( self.planet )

        self.mw.status("Getting available port counts...")
        bldg_getter = GetSingleBuilding( self.mw.app, self.planet, 'spaceport', fresh = True )
        self.sp = bldg_getter.request()
        self.view_getter = GetSPView( self.mw.app, self.sp, fresh = True )
        ui_should_be_enabled = self.update_docks_label()

        self.mw.status("Getting buildable ships...")
        self.obj_tbl_buildable_ships.add_ships( self.obj_tbl_sy_build.shipyards )
        self.obj_tbl_buildable_ships.set_available_docks(self.view_getter.docks_free)

        if ui_should_be_enabled:
            self.enable_ui()
        self.mw.update_config_status();

