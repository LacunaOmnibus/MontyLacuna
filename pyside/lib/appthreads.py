
import datetime, time
from PySide.QtCore import *



class BuildShipsInYards(QThread):
    dataReady = Signal(object)

    ### CHECK
    ### I'm currently not using the unchecked shipyard slots at all.  I'll 
    ### eventually need to collect those unchecked shipyards and count their 
    ### slots and add those slots to the active SYs

    def __init__(self, app, yards:list, ships_to_build:dict, parent = None):
        QThread.__init__(self, parent)
        self.app                    = app
        self.earliest_recall_time   = None     # datetime.datetime
        self.yards                  = yards
        self.ships                  = ships_to_build
        self.built                  = {}

    def request(self):
        self.start()    # Automatically calls run()
        while(self.isRunning()):
            self.app.processEvents()
            time.sleep(0.1)
        return self.num_built

    def get_yard_slots(self, yard):
        _, num_building_now, _ = yard.view_build_queue()
        return( yard.level - num_building_now )

    def run(self):
        for yard in self.yards:
            slots = self.get_yard_slots(yard)

            for shiptype in self.ships.keys():
                ttl_to_build = ships[shiptype]
                num_to_build = ttl_to_build
                if num_to_build > slots:
                    num_to_build = slots
                    self.ships[shiptype] -= num_to_build
                else:
                    del self.ships[shiptype]
                yard.build_ship( shiptype, num_to_build )

                if shiptype in self.built:
                    self.built[shiptype] += num_to_build
                else:
                    self.built[shiptype] = num_to_build

            if self.earliest_recall_time:
                if yard.end_dt < self.earliest_recall_time:
                    self.earliest_recall_time = yard.end_dt
            else:
                self.earliest_recall_time = yard.end_dt

        ### CHECK
        ### What I really want to do here is to re-call myself at the 
        ### earliest_recall_time, and keep doing so until self.ships indicates 
        ### there are no more ships to build.
        ### I think the "if you need more control" bit in the pyside README 
        ### (thread section) gives us what we need.
        self.dataReady.emit(self.earliest_recall_time) 

class GetPlanet(QThread):
    dataReady = Signal(object)

    def __init__(self, app, pname, fresh = False, parent = None):
        QThread.__init__(self, parent)
        self.app    = app
        self.fresh  = fresh
        self.pname  = pname
        self.planet = None

    def request(self):
        self.start()    # Automatically calls run()
        while(self.isRunning()):
            self.app.processEvents()
            time.sleep(0.1)
        return self.planet

    def run(self):
        if self.fresh:
            self.app.client.cache_clear('my_planets')
        self.app.client.cache_on('my_planets', 3600)
        self.planet = self.app.client.get_body_byname( self.pname )
        self.dataReady.emit(self.planet) 


class GetSingleBuilding(QThread):
    dataReady = Signal(object)

    def __init__(self, app, planet, btype, fresh = False, parent = None):
        QThread.__init__(self, parent)
        self.app    = app
        self.bldg   = None
        self.btype  = btype
        self.fresh  = fresh
        self.planet = planet

    def request(self):
        self.start()
        while(self.isRunning()):
            self.app.processEvents()
            time.sleep(0.1)
        return self.bldg

    def run(self):
        if self.fresh:
            self.app.client.cache_clear('my_buildings')
        self.app.client.cache_on('my_buildings', 3600)
        try:
            self.bldg = self.planet.get_buildings_bytype( self.btype, 1, 1, 100 )[0]
        except err.NoSuchBuildingError as e:
            self.app.poperr( self.parent, "You don't have a working {}.".format(self.btype) )
            return
        self.dataReady.emit(self.bldg) 


class GetBuildingById(QThread):
    dataReady = Signal(object)

    def __init__(self, app, planet, id, type, fresh = False, parent = None):
        QThread.__init__(self, parent)
        self.app    = app
        self.bldg   = None
        self.id     = id
        self.type   = type
        self.fresh  = fresh
        self.planet = planet

    def request(self):
        self.start()
        while(self.isRunning()):
            self.app.processEvents()
            time.sleep(0.1)
        return self.bldg

    def run(self):
        if self.fresh:
            self.app.client.cache_clear('my_buildings')
        self.app.client.cache_on('my_buildings', 3600)
        try:
            self.bldg = self.planet.get_building_id( self.type, self.id )
        except err.NoSuchBuildingError as e:
            self.app.poperr( self.parent, "You don't have a working {}.".format(self.btype) )
            return
        self.dataReady.emit(self.bldg) 


class GetAllWorkingBuildings(QThread):
    dataReady = Signal(object)

    def __init__(self, app, planet, btype, fresh = False, parent = None):
        QThread.__init__(self, parent)
        self.app    = app
        self.bldgs  = []
        self.btype  = btype
        self.fresh  = fresh
        self.planet = planet

    def request(self):
        self.start()
        while(self.isRunning()):
            self.app.processEvents()
            time.sleep(0.1)
        return self.bldgs

    def run(self):
        if self.fresh:
            self.app.client.cache_clear('my_buildings')
        self.app.client.cache_on('my_buildings', 3600)
        try:
            self.bldgs = self.planet.get_buildings_bytype( self.btype, 1, 0, 100 )
        except err.NoSuchBuildingError as e:
            self.app.poperr( self.parent, "You don't have any working {} buildings.".format(self.btype) )
            return
        self.dataReady.emit(self.bldgs) 


class GetAllShipsView(QThread):
    dataReady = Signal(object)

    def __init__(self, app,
        sp, paging:dict = {}, filter:dict = {}, sort:str = None, fresh = False, 
        parent = None
    ):
        QThread.__init__(self, parent)
        self.app    = app
        self.filter = filter
        self.fresh  = fresh
        self.paging = paging
        self.ships  = []
        self.sort   = sort
        self.sp     = sp

    def request(self):
        self.start()
        while(self.isRunning()):
            self.app.processEvents()
            time.sleep(0.1)
        return self.ships

    def run(self):
        if self.fresh:
            self.app.client.cache_clear('my_ships')
        self.app.client.cache_on('my_ships', 3600)
        self.ships, cnt = self.sp.view_all_ships(self.paging, self.filter, self.sort)
        self.dataReady.emit(self.ships) 


class MassShipScuttler(QThread):
    dataReady = Signal(object)

    def __init__(self, app, sp, ship_ids:list, parent = None):
        QThread.__init__(self, parent)
        self.app    = app
        self.ids    = ship_ids
        self.sp     = sp

    def request(self):
        self.start()
        while(self.isRunning()):
            self.app.processEvents()
            time.sleep(0.1)
        return self.ids

    def run(self):
        self.sp.mass_scuttle_ship( self.ids )
        self.dataReady.emit(True) 


class GetShipyardBuildable(QThread):
    dataReady = Signal(object)

    def __init__(self, app, sy, fresh = False, parent = None):
        QThread.__init__(self, parent)
        self.app        = app
        self.fresh      = fresh
        self.ships      = []
        self.sy         = sy
        self.bq_max     = 0     # build_queue_max
        self.bq_used    = 0     # build_queue_used
        self.docks      = 0

    def request(self):
        self.start()
        while(self.isRunning()):
            self.app.processEvents()
            time.sleep(0.1)
        return self.ships

    def run(self):
        if self.fresh:
            self.app.client.cache_clear('my_ships')
        self.app.client.cache_on('my_ships', 3600)
        self.ships, self.docks, self.bq_max, self.bq_used = self.sy.get_buildable()
        self.dataReady.emit(self.ships) 


class GetSPView(QThread):
    dataReady = Signal(object)

    def __init__(self, app, sp, fresh = False, parent = None):
        QThread.__init__(self, parent)
        self.app        = app
        self.fresh      = fresh
        self.ships      = []
        self.docks_free = None
        self.docks_max  = None
        self.sp         = sp

    def request(self):
        self.start()
        while(self.isRunning()):
            self.app.processEvents()
            time.sleep(0.1)
        return self.ships

    def run(self):
        if self.fresh:
            self.app.client.cache_clear('my_ships')
        self.app.client.cache_on('my_ships', 3600)
        self.ships, self.docks_free, self.docks_max = self.sp.view()
        self.dataReady.emit(self.ships) 

