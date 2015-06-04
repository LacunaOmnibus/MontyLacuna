
from PySide.QtGui import QMainWindow, QTableWidget, QTableWidgetItem
from PySide.QtCore import *

import widgets
from appthreads import *

class AbbreviationsTable():
    """ Manages the table that handles body abbreviations.

    Arguments:
        table (QTableWidget): The actual table widget.
        parent (QWidget): The widget that owns the table widget.
    """

    def __init__(self, table:QTableWidget, parent:QMainWindow):
        self.widget = table
        self.parent = parent
        self.clear()
        #self.reset()

    def clear(self):
        self.widget.clear()
        self.widget.setRowCount(0)
        self.widget.setColumnCount(0)

    def init_for_data(self):
        self.clear()
        self.widget.setRowCount(0)
        self.widget.setColumnCount(2)
        self.widget.setHorizontalHeaderLabels( ('Name', 'Abbreviation') )

    def set_abbreviations(self, empire):
        """ Clears the abbreviations table, then adds the abbreviations for the current 
        empire to it.

        Arguments:
            empire (lacuna.empire.MyEmpire): The empire whose abbreviations we'll show.
        """
        self.init_for_data()
        self.widget.setSortingEnabled(False)
        row = 0
        for n in sorted(empire.planet_names):
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
        self.widget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        hh_w    = self.widget.horizontalHeader().width()
        name_w  = int(hh_w * .60)
        abbrv_w = hh_w - name_w
        self.widget.setColumnWidth(0, name_w)
        self.widget.setColumnWidth(1, abbrv_w)

    def update(self, itm_abbrv):
        itm_name = self.widget.item( itm_abbrv.row(), 0 )
        self.parent.app.abbrv.save( itm_name.text(), itm_abbrv.text() )


