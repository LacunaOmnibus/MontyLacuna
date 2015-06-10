
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
        self.tab_holder     = tab_holder
        self.mw             = main_window

        self.mw.btn_build_ships.setEnabled(False)
        self.obj_cmb_colonies_build     = widgets.BodiesComboBox( self.mw.cmb_planets_build, self.mw )
        self.obj_tbl_sy_build           = widgets.tabs.ShipyardsTable( self.mw.tbl_shipyards_build, self.mw )
        self.obj_tbl_buildable_ships    = widgets.tabs.BuildableShipsTable( self.mw.tbl_ships_build, self.mw )

        self.set_events()

    def set_events(self):
        self.mw.btn_get_shipyards_build.clicked.connect( self.get_shipyards_for_build )
        self.mw.btn_build_ships.clicked.connect( self.build_ships )

    def adjust_gui_login(self):
        self.obj_cmb_colonies_build.add_colonies()

    def adjust_gui_logout(self):
        self.self.mw.btn_build_ships.setEnabled(False)
        self.obj_cmb_colonies_build.clear()
        self.obj_tbl_sy_build.clear()
        self.obj_tbl_buildable_ships.clear()

    def resize(self):
        self.obj_tbl_sy_build.resize()
        self.obj_tbl_buildable_ships.resize()

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
        self.mw.status("Adding ships to your build queues...")
        ship_builder = BuildShipsInYards( self.mw.app, shipyards, ships_dict )
        self._set_shipbuild_thread( ship_builder )
        self.mw.update_config_status()

    def _set_shipbuild_thread(self, builder):
        recall_time = builder.request()    # datetime.datetime
        if recall_time:
            recall_time = recall_time.replace(tzinfo=pytz.UTC)
            sleeptime_ms = self.mw.app.get_ms_until(recall_time)
            timer = QTimer(self)
            timer.setSingleShot(True)
            timer.timeout.connect( lambda: self._set_shipbuild_thread(builder) )
            timer.start(sleeptime_ms)

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



