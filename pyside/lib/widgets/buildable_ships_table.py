
import operator

from PySide.QtGui import QMainWindow, QCheckBox, QLabel, QPixmap, QSpinBox, QTableWidget, QTableWidgetItem
from PySide.QtCore import *

import widgets
from appthreads import *

class BuildableShipsTable():
    """ Manages the table that displays shipyards on a planet

    Arguments:
        table (QTableWidget): The actual table widget.
        parent (QWidget): The widget that owns the table widget.
        shipyard (lacuna.buildings.callable.shipyard): The shipyard to query
    """

    ### Listing both, but the originals are square and I'm maintaining aspect 
    ### ratio, so whichever one is smaller will pertain to both.  So just set 
    ### them both to the save value.
    img_w = 30
    img_h = 30

    def __init__(self, table:QTableWidget, parent:QMainWindow ):
        self.widget     = table
        self.parent     = parent
        self.ships      = []
        self.clear()

    def add_ships(self, shipyards:str):
        """ Lists the shiptypes that this planet can build.

        Arguments:
            shipyards (list): :class:`lacuna.buildings.callable.shipyard` objects 
                              on the planet.

        The list of buildable ships is taken from the highest-level shipyard's 
        get_buildable_ships() call.

        """
        self.shipyards = shipyards

        self.parent.status("Getting buildable ships...")
        sorted_shipyards    = sorted( self.shipyards, key=operator.attrgetter('level'), reverse=True )
        buildable_getter    = GetShipyardBuildable( self.parent.app, sorted_shipyards[0], fresh = True )
        self.ships          = buildable_getter.request()

        self.init_for_data()
        self._add_my_ships()
        self.parent.btn_build_ships.setEnabled(True)
        self.resize()
        self.parent.update_config_status();

    def _add_my_ships(self):
        """ Adds shipyards from a dict to the table.

        *Must* be called after (or by) add_shipyards_for(), since that's what 
        sets self.shipyards which this method depends on.
        """
        row = 0
        delete_buttons = {}
        for ship in sorted( self.ships, key=operator.attrgetter('type') ):
            ### Image
            lbl_icon = QLabel()
            img_bldg = QPixmap(":/" + ship.type + ".png").scaled(self.img_w, self.img_w, Qt.KeepAspectRatio)
            lbl_icon.setPixmap(img_bldg)
            ### Type
            itm_type    = QTableWidgetItem(ship.type)
            ### Num to build
            build_spinner = QSpinBox()
            build_spinner.setMinimum(0)
            self.widget.insertRow(row)
            self.widget.setCellWidget(row, 0, lbl_icon)
            self.widget.setItem(row, 1, itm_type)
            self.widget.setCellWidget(row, 2, build_spinner)
            row +=1

    def clear(self):
        """ Clears the table
        """
        self.widget.clear()
        self.widget.setRowCount(0)
        self.widget.setColumnCount(0)
        self.parent.btn_build_ships.setEnabled(False)

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

    def get_ships_to_build(self):
        """ Gets the types and numbers of ships the user wants to build.

        Returns:
            ships (dict): "shiptype": num_to_build
            total (int): Total number of ships to build across all types
        """
        ships   = {}
        ttl     = 0
        for row in range(0, self.widget.rowCount()):
            spin = self.get_cell(row, 2, True)
            if spin.value() > 0:
                ships[ self.get_cell(row, 1).text() ] = spin.value()
                ttl += spin.value()
        return ships, ttl


    def init_for_data(self):
        """ Clears out the table and then prepares it for receiving records
        """
        self.clear()
        self.widget.setRowCount(0)
        self.widget.setColumnCount(3)
        self.widget.setHorizontalHeaderLabels( ('', 'Type', 'Number to build') )

    def resize(self):
        """ Resizes the table.
        """
        self.widget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        hh_w    = self.widget.horizontalHeader().width()
        icon_w  = self.img_w + 4
        type_w  = int(hh_w * .30)
        num_w   = hh_w - (icon_w + type_w)
        self.widget.setColumnWidth(0, icon_w)
        self.widget.setColumnWidth(1, type_w)
        self.widget.setColumnWidth(2, num_w)

