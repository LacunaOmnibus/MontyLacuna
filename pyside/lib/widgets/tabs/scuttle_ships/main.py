
from PySide.QtGui import *
from PySide.QtCore import *

from appthreads import *
import widgets

class ScuttleShipsTab():
    """ The contents of the Scuttle Ships tab.

    Most classes representing a piece of the GUI have a ``self.widget`` 
    attribute, which contains the actual Qt widget that the class represents.

    However, a single tab is not, itself, a widget.  The QTabWidget is the 
    widget that creates and manages the tabs, but the individual tabs are just 
    pieces of that parent widget.
    """

    def __init__( self, tab_holder:QTabWidget, main_window:QMainWindow ):
        self.mw             = main_window
        self.tab_holder     = tab_holder

        self.cmb_colonies   = widgets.BodiesComboBox( self.mw.cmb_planets_scuttle, self.mw )
        self.tbl_scuttle    = widgets.tabs.ShipsDeleteTable( self.mw.tbl_ships_scuttle, self.mw, self )

        self._init_ui()
        self._set_events()

    def _init_ui(self):
        self.mw.btn_get_ships_scuttle.setEnabled(False)

    def _set_events(self):
        self.mw.btn_get_ships_scuttle.clicked.connect( self.get_ships_for_scuttle )

    def adjust_gui_login(self):
        """ To be called when the user logs an empire in to TLE
        """
        self.mw.btn_get_ships_scuttle.setEnabled(True)
        self.cmb_colonies.add_colonies()

    def adjust_gui_logout(self):
        """ To be called when the user logs their empire out
        """
        self.mw.btn_get_ships_scuttle.setEnabled(False)
        self.cmb_colonies_scuttle.clear()
        self.tbl_scuttle.clear()

    def disable_ui(self):
        """ Disables all widgets on the tab.
        """
        self.tbl_scuttle.setEnabled(False)

    def enable_ui(self):
        """ Enables all widgets on the tab.
        """
        self.tbl_scuttle.setEnabled(True)

    def resize(self):
        """ To be called after a mainwindow resize event
        """
        self.tbl_scuttle.resize()

    def get_ships_for_scuttle(self):
        pname = self.cmb_colonies.currentText()
        self.tbl_scuttle.add_ships_for(pname)

