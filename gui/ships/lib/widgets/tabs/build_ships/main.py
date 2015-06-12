
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
        self.planet         = None  # lacuna body object; filled by update_yards_and_ships_tables
        self.sp             = None  # spaceport; filled by update_yards_and_ships_tables
        self.view_getter    = None  # spaceport view() thread; filled by update_yards_and_ships_tables

        self.mw.btn_build_ships.setEnabled(False)
        self.cmb_bodies         = widgets.BodiesComboBox( self.mw.cmb_planets_build, self.mw )
        self.tbl_shipyards      = widgets.tabs.ShipyardsTable( self.mw.tbl_shipyards_build, self.mw )
        self.tbl_build_ships    = widgets.tabs.BuildableShipsTable( self.mw.tbl_ships_build, self.mw )

        self._init_ui()
        self._set_events()

    def _init_ui(self):
        self.mw.btn_get_shipyards_build.setEnabled(False)

    def _set_events(self):
        self.mw.btn_get_shipyards_build.clicked.connect( self.update_yards_and_ships_tables )
        self.mw.btn_build_ships.clicked.connect( self.build_ships )

    def adjust_gui_login(self):
        """ To be called when the user logs an empire in to TLE
        """
        self.mw.btn_get_shipyards_build.setEnabled(True)
        self.cmb_bodies.add_colonies()
        self.sp             = None
        self.view_getter    = None

    def adjust_gui_logout(self):
        """ To be called when the user logs their empire out
        """
        self.mw.btn_get_shipyards_build.setEnabled(False)
        self.mw.btn_build_ships.setEnabled(False)
        self.cmb_bodies.clear()
        self.tbl_shipyards.clear()
        self.tbl_build_ships.clear()
        self.sp             = None
        self.view_getter    = None

    def disable_ui(self):
        """ Disables all widgets on the tab.
        """
        self.mw.btn_build_ships.setEnabled(False)
        self.tbl_shipyards.setEnabled(False)
        self.tbl_build_ships.setEnabled(False)

    def enable_ui(self):
        """ Enables all widgets on the tab.
        """
        self.cmb_bodies.setEnabled(True)
        self.mw.btn_get_shipyards_build.setEnabled(True)
        self.mw.lbl_build_ports_available.setEnabled(True)
        self.mw.btn_build_ships.setEnabled(True)
        self.tbl_shipyards.setEnabled(True)
        self.tbl_build_ships.setEnabled(True)

    def resize(self):
        """ To be called after a mainwindow resize event
        """
        self.tbl_shipyards.resize()
        self.tbl_build_ships.resize()

    def build_ships(self):
        """ Called when the user clicks the Build! button.  Builds the 
        specified ships in a separate thread.
        """
        shipyards = self.tbl_shipyards.get_included_shipyards()
        if not shipyards:
            self.mw.app.poperr(self.mw, "You must select the shipyard or yards at which to build ships by checking their checkboxes first.")
            return
        ships_dict, num_left_to_build = self.tbl_build_ships.get_ships_to_build()
        if self.tbl_build_ships.available_docks is not None:
            if num_left_to_build > self.tbl_build_ships.available_docks:
                ### With 10 SY slots left, the user could try to build 9 of 
                ### one shiptype and 2 of another.  They'll get a poperr() 
                ### warning that they're over the total, but they might ignore 
                ### it, in which case this will hit.
                self.mw.app.poperr(self.mw, 
                    "You're trying to build more ships than you have available docks!"
                )
                return
        self.disable_ui()

        self.mw.status("Adding ships to your build queues...")
        if not self.planet.name in self.builders:
            self.builders[self.planet.id] = BuildShipsInYards( self.mw.app, self.planet.id, shipyards, ships_dict )
            self.builders[self.planet.id].sig_empty.connect( self._build_thread_isempty )
        self._set_shipbuild_thread( self.builders[self.planet.id] )
        self.mw.update_config_status()
        ui_should_be_enabled = self.update_docks_label()
        if ui_should_be_enabled:
            self.enable_ui()

        if self.planet.id in self.builders:
            if self.builders[self.planet.id].ships_left():
                self.mw.app.popmsg(self.mw,
                    """
                    <span>
                    The shipyard build queues on {0} are full, but there <br>
                    are more ships to add.<p> 
                    As long as you leave this app running, the additional ships will get<br>
                    added to the build queues as they become available.<p> 
                    To see how many ships still need to be added to the queue, return<br>
                    to the Build Ships tab at any time and click the 'Get shipyards'<br>
                    button for {0} again. 
                    </span>
                    """
                    .format( self.planet.name )
                )

    def _build_thread_isempty(self, planet_id ):
        if planet_id in self.builders:
            del(self.builders[planet_id])

    def _set_shipbuild_thread(self, builder):
        recall_time = builder.request()     # datetime.datetime
        if recall_time:
            recall_time = recall_time.replace(tzinfo=pytz.UTC)
            sleeptime_ms = self.mw.app.get_ms_until(recall_time)
            sleeptime_ms += 5000            # add 5 second buffer
            timer = QTimer(self.mw)
            timer.setSingleShot(True)
            timer.timeout.connect( lambda: self._set_shipbuild_thread(builder) )
            timer.start(sleeptime_ms)

    def update_docks_label(self):
        """ Updates the label above the shipyards table with either the number 
        of available docks, or a note stating that a build thread is currently 
        active.

        Returns:
            ui_should_be_enabled (bool): Whether or not we should re-enable the UI.
                                         If a build thread is currently active, this 
                                         will return False.
        """
        ui_should_become_enabled = True
        if self.planet:
            if self.planet.id in self.builders:
                if self.builders[self.planet.id]:
                    num     = self.builders[self.planet.id].ships_left()
                    noun    = "ship" if num == 1 else "ships"
                    self.mw.lbl_build_ports_available.setText( 
                        "This planet has {} more {} to add to the build queues." 
                        .format( num, noun )
                    )
                    ui_should_become_enabled = False
                    return ui_should_become_enabled
        if self.view_getter:
            self.view_getter.request()
            self.mw.lbl_build_ports_available.setText(
                "{} of {} docks are available."
                .format(self.view_getter.docks_free, self.view_getter.docks_max)
            )
        return ui_should_become_enabled

    def update_yards_and_ships_tables(self):
        """ Modifies two tables - the list of shipyards on the planet, and the 
        list of buildable ships (based on what the first shipyard is able to 
        build).
        """
        self.disable_ui()
        self.tbl_shipyards.clear()
        self.tbl_build_ships.clear()
        self.mw.lbl_build_ports_available.setText('')

        pname = self.cmb_bodies.currentText()

        self.mw.status("Getting planet...")
        planet_getter = GetPlanet( self.mw.app, pname )
        self.planet = planet_getter.request()

        self.mw.status("Getting shipyards...")
        self.tbl_shipyards.add_shipyards_for( self.planet )

        self.mw.status("Getting available port counts...")
        bldg_getter = GetSingleBuilding( self.mw.app, self.planet, 'spaceport', fresh = True )
        self.sp = bldg_getter.request()
        self.view_getter = GetSPView( self.mw.app, self.sp, fresh = True )
        ui_should_be_enabled = self.update_docks_label()

        self.mw.status("Getting buildable ships...")
        self.tbl_build_ships.add_ships( self.tbl_shipyards.shipyards )
        self.tbl_build_ships.set_available_docks(self.view_getter.docks_free)

        if ui_should_be_enabled:
            self.enable_ui()
        self.mw.update_config_status();

