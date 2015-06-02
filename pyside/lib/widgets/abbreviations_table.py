
from PySide.QtGui import QMainWindow, QTableWidget, QTableWidgetItem
from PySide.QtCore import *

import widgets
from appthreads import *


### CHECK
### If this tab doesn't have focus on login, the columns are not resizing 
### properly.  The user has to force a window resize to get the table to 
### display.
###
### On reset, the table should be cleared completely.  Don't leave just the 
### header row - that means we have to fart around trying to size it correctly 
### when it has no contents, which is silly.


class AbbreviationsTable():
    """ Manages the table that handles body abbreviations.

    Arguments:
        table (QTableWidget): The actual table widget.
        parent (QWidget): The widget that owns the table widget.
    """

    def __init__(self, table:QTableWidget, parent:QMainWindow):
        self.widget = table
        self.parent = parent
        self.reset()

    def clear(self):
        self.widget.clear()
        self.widget.setRowCount(0)
        self.widget.setColumnCount(0)

    def reset(self):
        """ Resets the table contents to the correct size and headers, whether 
        we're logged in or not.

        CHECK
        This is a mess.  This reset() needs to become init_for_data(), and the 
        resetting we're doing in here now needs to end up somewhere else.  See 
        one of the other _table.py modules for example.

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


