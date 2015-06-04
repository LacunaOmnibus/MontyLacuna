
import operator

from PySide.QtGui import *
from PySide.QtCore import *

import widgets
from appthreads import *

class ShipyardsTable():
    """ Manages the table that displays shipyards on a planet

    Arguments:
        table (QTableWidget): The actual table widget.
        parent (QWidget): The widget that owns the table widget.
    """

    ### Listing both, but the originals are square and I'm maintaining aspect 
    ### ratio, so whichever one is smaller will pertain to both.  So just set 
    ### them both to the save value.
    img_w = 30
    img_h = 30


    def __init__(self, table:QTableWidget, parent:QMainWindow):
        self.widget     = table
        self.parent     = parent
        self.planet     = None
        self.shipyards  = []
        self.clear()

    def setVisible(self, toggle:bool = True):
        self.widget.setVisible(toggle)

    def add_shipyards_for(self, pname:str):
        """ Lists the shipyards on the selected planet

        Arguments:
            pname (str): The planet name

        This *does* clear the table before adding the shipyards, since the list 
        it adds is complete for the requested planet.
        """
        self.parent.status("Getting planet...")
        planet_getter = GetPlanet( self.parent.app, pname )
        planet = planet_getter.request()

        self.parent.status("Getting shipyards...")
        bldg_getter = GetAllWorkingBuildings( self.parent.app, planet, 'shipyard' )
        self.shipyards   = bldg_getter.request()

        self.init_for_data()
        self._add_shipyards()
        self.parent.update_config_status();

    def _add_shipyards(self):
        """ Adds shipyards from a dict to the table.

        *Must* be called after (or by) add_shipyards_for(), since that's what 
        sets self.shipyards which this method depends on.
        """
        row = 0
        for bldg in sorted( self.shipyards, key=operator.attrgetter('level'), reverse=True ):
            ### Image
            lbl_icon = QLabel()
            img_bldg = QPixmap(":/" + bldg.image + ".png").scaled(self.img_w, self.img_w, Qt.KeepAspectRatio)
            lbl_icon.setPixmap(img_bldg)
            ### Type and Quantity
            itm_level       = QTableWidgetItem(str(bldg.level))
            itm_x           = QTableWidgetItem(str(bldg.x))
            itm_y           = QTableWidgetItem(str(bldg.y))
            ### Should this SY be included?  Default to "no"
            checkbox = QCheckBox()
            checkbox.setCheckState(Qt.Unchecked)

            self.widget.insertRow(row)
            self.widget.setCellWidget(row, 0, lbl_icon)
            self.widget.setItem(row, 1, itm_level)
            self.widget.setItem(row, 2, itm_x)
            self.widget.setItem(row, 3, itm_y)
            self.widget.setCellWidget(row, 4, checkbox)
            row +=1
        self.resize()

    def clear(self):
        """ Clears the table
        """
        self.widget.clear()
        self.widget.setRowCount(0)
        self.widget.setColumnCount(0)

    def init_for_data(self):
        """ Clears out the table and then prepares it for receiving records
        """
        self.clear()
        self.widget.setRowCount(0)
        self.widget.setColumnCount(5)
        self.widget.setHorizontalHeaderLabels( ('', 'Level', 'X', 'Y', 'Include?') )

    def resize(self):
        """ Resizes the table.
        """
        self.widget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        hh_w    = self.widget.horizontalHeader().width()
        icon_w  = self.img_w + 4
        level_w = int(hh_w * .20)
        x_w     = int(hh_w * .10)
        y_w     = int(hh_w * .10)
        chk_w   = hh_w - (icon_w + level_w + x_w + y_w)
        self.widget.setColumnWidth(0, icon_w)
        self.widget.setColumnWidth(1, level_w)
        self.widget.setColumnWidth(2, x_w)
        self.widget.setColumnWidth(3, y_w)
        self.widget.setColumnWidth(4, chk_w)

