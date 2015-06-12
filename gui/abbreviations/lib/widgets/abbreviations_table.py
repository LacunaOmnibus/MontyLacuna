
from PySide.QtGui import QMainWindow, QHeaderView, QTableWidget, QTableWidgetItem
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
        self.widget         = table
        self.parent         = parent
        self.num_planets    = 0
        self.clear()

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
            self.num_planets += 1
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
        self.widget.itemChanged.connect( self.update )
        self.resize(True)

    def resize(self, initial:bool = False):
        self.widget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.widget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

        """ Ugh.

        The "Vertical Header" is the column of row numbers down the left side 
        of the table.

        Before the table gets built, there are zero rows, so the vertical 
        header has no width.

        If the user is on any other tab when they log in (which builds the 
        table), then, when they click the Abbreviations tab, the vertical 
        header width is known.  Since there's a conditional in here that's 
        resizing the table when the Abbreviations tab gets clicked, this 
        results in the table being displayed properly.
        
        However, if the user happens to already be on the Abbreviations tab 
        before logging in, there's no table yet, so that vertical header has 
        no width yet.

        In that case, when we figure the horizontal header width (hh_w below), 
        it does not factor the vertical header width in yet (since there 
        currently is no vertical header!)

        The resulting table is just a little bit too wide, because of the 
        vertical header that eventually pops into existence and pushes 
        everything else over to the right.

        To make matters worse, that vertical header's width changes based on 
        its contents.  On ubuntu, with fewer than 10 planets (so the vert 
        header contains only 1-digit numbers), its width is 18.  When it 
        contains 2-digit numbers, its width is 26, and when it contains 
        3-digit numbers, its width is 34.

        I could modify the hh_w based on those numbers, but I very much 
        suspect that those numbers are specific to OS/resolution/Qt 
        style/phases of the moon etc.

        SO... if we're already on the Abbreviations tab when the table 
        initially gets built, we're going to quickly change to another tab and 
        then back here again.  This happens quickly enough that the user 
        doesn't see a flash, and when we get back here, our Vertical Header 
        has width.  Huzzah.
        """
        if initial and self.parent.tabWidget.currentIndex() == 1:
            self.parent.tabWidget.setCurrentPage(0)
            self.parent.tabWidget.setCurrentPage(1)
        hh_w    = self.widget.horizontalHeader().width()
        name_w  = int(hh_w * .60)
        abbrv_w = hh_w - name_w
        self.widget.setColumnWidth(0, name_w)
        self.widget.setColumnWidth(1, abbrv_w)

    def update(self, itm_abbrv):
        itm_name = self.widget.item( itm_abbrv.row(), 0 )
        self.parent.app.abbrv.save( itm_name.text(), itm_abbrv.text() )

