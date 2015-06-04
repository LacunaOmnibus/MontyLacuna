
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

    def get_cell(self, row:int, col:int, is_widget:bool = False):
        """ Gets the cell contents at (row, col).  The header rows do _not_ 
        count as a row or a column, and offsets start at 0, so the row marked 
        as '1' is row 0 for the purposes of this method.

        Arguments:
            row (int): The row count
            col (int): The column count
            is_widget (bool): Whether or not the contained item is a widget.
                              Defaults to False.
        Returns:
            item (QTableWidgetItem or QWidget): If ``is_widget`` is false,
                                                returns a QTableWidgetItem, 
                                                else returns a QWidget.
        """
        if is_widget:
            itm = self.widget.cellWidget(row, col)
        else:
            itm = self.widget.item(row, col)
        return itm

    def columnCount(self):
        return self.widget.columnCount()

    def rowCount(self):
        return self.widget.rowCount()

    def get_included_shipyards(self):
        """ HERE
        """
        if not self.planet:
            return
        print( self.planet.name )

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
        self.planet = planet_getter.request()

        self.parent.status("Getting shipyards...")
        bldg_getter = GetAllWorkingBuildings( self.parent.app, self.planet, 'shipyard' )
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
            itm_id          = QTableWidgetItem(str(bldg.id))
            itm_x           = QTableWidgetItem(str(bldg.x))
            itm_y           = QTableWidgetItem(str(bldg.y))
            ### Should this SY be included?  Default to "no"
            checkbox = QCheckBox()
            checkbox.setCheckState(Qt.Unchecked)

            self.widget.insertRow(row)
            self.widget.setCellWidget(row, 0, lbl_icon)
            self.widget.setItem(row, 1, itm_level)
            self.widget.setItem(row, 2, itm_id)
            self.widget.setItem(row, 3, itm_x)
            self.widget.setItem(row, 4, itm_y)
            self.widget.setCellWidget(row, 5, checkbox)
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
        self.widget.setColumnCount(6)
        self.widget.setHorizontalHeaderLabels( ('', 'Level', 'ID', 'X', 'Y', 'Include?') )

    def resize(self):
        """ Resizes the table.
        """
        self.widget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        hh_w    = self.widget.horizontalHeader().width()
        icon_w  = self.img_w + 4
        level_w = int(hh_w * .20)
        id_w    = int(hh_w * .20)
        x_w     = int(hh_w * .10)
        y_w     = int(hh_w * .10)
        chk_w   = hh_w - (icon_w + level_w + id_w + x_w + y_w)
        self.widget.setColumnWidth(0, icon_w)
        self.widget.setColumnWidth(1, level_w)
        self.widget.setColumnWidth(2, id_w)
        self.widget.setColumnWidth(3, x_w)
        self.widget.setColumnWidth(4, y_w)
        self.widget.setColumnWidth(5, chk_w)

