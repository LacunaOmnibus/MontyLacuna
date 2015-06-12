
import functools

from PySide.QtGui import QMainWindow, QLabel, QPixmap, QPushButton, QSpinBox, QTableWidget, QTableWidgetItem
from PySide.QtCore import *

import widgets
from appthreads import *

class ShipsDeleteTable():
    """ Manages the table that handles ship scuttling.

    Arguments:
        table (QTableWidget): The actual table widget.
        parent (QWidget): The widget that owns the table widget.
        tabclass (widgets.tabs.scuttle_ships.main.ScuttleShipsTab): The tab class where
                                                                    this table appears.
    """

    ### Listing both, but the originals are square and I'm maintaining aspect 
    ### ratio, so whichever one is smaller will pertain to both.  So just set 
    ### them both to the save value.
    img_w = 30
    img_h = 30

    main_stats = {
        "combat": [ 
            'bleeder', 'drone', 'fighter', 'observatory_seeker', 
            'security_ministry_seeker', 'spaceport_seeker', 'snark', 'snark2', 
            'snark3', 'sweeper', 'thud'
        ],
        "hold": [
            'barge', 'cargo_ship', 'dory', 'freighter', 'galleon', 'hulk',
            'hulk_fast', 'hulk_huge', 'scow', 'scow_fast', 'scow_mega'
        ],
        "stealth": [
            'scanner', 'smuggler_ship', 'spy_pod', 'spy_shuttle', 'surveyor'
        ]
    }

    def __init__(self, table:QTableWidget, parent:QMainWindow, tabclass):
        self.widget     = table
        self.parent     = parent
        self.tabclass   = tabclass
        self.planet     = None
        self.clear()

    def setEnabled(self, flag:bool):
        self.widget.setEnabled(flag)

    def add_ships_for(self, pname:str):
        """ Adds ship summaries to the table for a given planet name.

        Arguments:
            pname (str): The planet name

        Raises no exceptions, but will poperr and return if a working spaceport 
        could not be found.

        This *does* clear the table before adding more ships, since the list of 
        ships it adds is complete for the requested planet.
        """
        self.parent.status("Getting planet...")
        planet_getter = GetPlanet( self.parent.app, pname )
        planet = planet_getter.request()

        self.parent.status("Getting spaceport...")
        bldg_getter = GetSingleBuilding( self.parent.app, planet, 'spaceport' )
        sp = bldg_getter.request()

        self.parent.status("Getting ships...")
        spviewer = GetSPView( self.parent.app, sp, fresh = True )
        docked_ships = spviewer.request()
        self.init_for_data()    # clear it before adding more ships.
        self.add_ships( docked_ships )
        self.parent.update_config_status();

    def add_ships(self, ships:dict):
        """ Adds ships from a dict to the table.

        Arguments:
            ships (dict): ``ship type (str) => quantity``

        This does *not* clear any existing entries before adding more ships. 
        If you want to pass an exhaustive dict, be sure to call ``reset`` first.

        You generally want ``add_ships_for`` instead of this.
        """
        row = 0
        delete_buttons = {}
        for type in sorted( ships.keys() ):
            ### Image
            lbl_icon = QLabel()
            img_ship = QPixmap(":/" + type + ".png").scaled(self.img_w, self.img_w, Qt.KeepAspectRatio)
            lbl_icon.setPixmap(img_ship)
            ### Type and Quantity
            itm_type        = QTableWidgetItem(type)
            itm_num_avail   = QTableWidgetItem("{:,}".format(ships[type]))
            ### Num to delete spinner
            del_spinner = QSpinBox()
            del_spinner.setMinimum(0)
            del_spinner.setMaximum(ships[type])
            ### Do Eet button
            btn_go = QPushButton("Go")

            ### functools.partial locks the arg's current value to the method.  
            ### A regular Python lambda would be late-binding, so all button 
            ### clicks would indicate the same (last) row.
            btn_go.clicked.connect( functools.partial(self.scuttle, row) )

            self.widget.insertRow(row)
            self.widget.setCellWidget(row, 0, lbl_icon)
            self.widget.setItem(row, 1, itm_type)
            self.widget.setItem(row, 2, itm_num_avail)
            self.widget.setCellWidget(row, 3, del_spinner)
            self.widget.setCellWidget(row, 4, btn_go)
            row +=1
        self.resize()


    def get_main_stat(self, shiptype:str):
        """ Gets the main statistic for a given shiptype.

        Arguments:
            type (str): The ship type (eg 'fighter', 'snark3', etc)
        Returns:
            stat (str): The most important stat for this type of ship.

        The "main stat" is not part of Lacuna, just a best guess at what's 
        best for a given type.  When deleting combat ships like sweepers, the 
        ships with the lowest combat scores will be deleted first.  For trade 
        ships like hulks, ships with the smallest hold size will go first.

        But some ships' best stats are arguable.  For Smugglers, this is going 
        to assume that stealth is the "main stat", but you might personally 
        prefer speed or hold size for those.  If that's the case, you'll need 
        to find another way to scuttle your ships.
        """
        if shiptype in self.main_stats['combat']:
            return 'combat'
        elif shiptype in self.main_stats['hold']:
            return 'hold'
        elif shiptype in self.main_stats['stealth']:
            return 'stealth'
        else:
            return 'speed'

    def clear(self):
        """ Clears the table
        """
        self.widget.clear()
        self.widget.setRowCount(0)
        self.widget.setColumnCount(0)

    def init_for_data(self):
        """ Resets the table contents to the correct size and headers
        """
        self.clear()
        self.widget.setRowCount(0)
        self.widget.setColumnCount(5)
        self.widget.setHorizontalHeaderLabels( ('', 'Ship Type', 'Quantity', 'Num', 'Scuttle') )

    def resize(self):
        """ Resizes the table.
        """
        self.widget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        hh_w    = self.widget.horizontalHeader().width()
        icon_w  = self.img_w + 4
        type_w  = int(hh_w * .30)
        quan_w  = int(hh_w * .30)
        del_w   = int(hh_w * .15)
        btn_w   = hh_w - (icon_w + type_w + quan_w + del_w)
        self.widget.setColumnWidth(0, icon_w)
        self.widget.setColumnWidth(1, type_w)
        self.widget.setColumnWidth(2, quan_w)
        self.widget.setColumnWidth(3, del_w)
        self.widget.setColumnWidth(4, btn_w)

    def scuttle(self, row:int):
        """ Scuttles the ships indicated by the settings on the indicated row.

        Arguments:
            row (int): Data from this table row (zero-indexed) will be pulled 
                       and the corresponding ships will be scuttled.
        """
        lbl_type    = self.widget.item(row, 1)
        lbl_ttl     = self.widget.item(row, 2)
        spin_del    = self.widget.cellWidget(row, 3)
        if spin_del.value() == 0:
            self.parent.app.poperr( self.parent, "You can't scuttle zero ships, Einstein." )
            return
        self.tabclass.disable_ui()

        self.parent.status("Getting planet...")
        pname = self.tabclass.cmb_colonies.currentText()
        planet_getter = GetPlanet( self.parent.app, pname )
        planet = planet_getter.request()

        self.parent.status("Getting spaceport...")
        bldg_getter = GetSingleBuilding( self.parent.app, planet, 'spaceport' )
        sp = bldg_getter.request()

        self.parent.status("Getting ships...")
        paging  = { 'no_paging': 1 }
        filter  = { 'type': lbl_type.text(), 'task': 'Docked' } # tested - combined filter _does_ work
        sort    = self.get_main_stat( lbl_type.text() )
        ### At this point, we definitely need fresh data.
        ships_getter = GetAllShipsView( self.parent.app, sp, paging, filter, sort, fresh = True )
        ships = ships_getter.request()
        ships.reverse() # sorted desc from the server; flip that to asc.

        delete_these = []
        for i in range(0, spin_del.value() ):
            try:
                delete_these.append( ships[i].id )
            except IndexError as e:
                print( "We're trying to scuttle a ship that doesn't exist; ignoring." )
        ships_scuttler = MassShipScuttler( self.parent.app, sp, delete_these )
        ships_scuttler.request()
        if self.parent.play_sounds:
            self.parent.app.play_sound('photon.wav')
        sp.mass_scuttle_ship( delete_these )
        self.parent.app.client.cache_clear('my_ships')
        self.parent.app.popmsg(self.parent, "I just scuttled {} ships of type {}."
            .format( len(delete_these), lbl_type.text() )
        )
        self.add_ships_for(pname)
        self.tabclass.enable_ui()

