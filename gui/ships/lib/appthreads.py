
import datetime, functools, time
from PySide.QtCore import *



class BuildShipsInYards(QThread):
    sig_empty   = Signal(object)

    ### CHECK
    ### I'm currently not using the unchecked shipyard slots at all.  I'll 
    ### eventually need to collect those unchecked shipyards and count their 
    ### slots and add those slots to the active SYs.
    ### 
    ### CHECK
    ### Need to emit a message if the user didn't click any shipyards in the 
    ### previous table (hey dummy tell me which yards to use)
    ###
    ### It's possible to have more ships than ports, and we need to deal with 
    ### that (right now, we're ignoring the possibility).
    ### The easiest way to force this is:
    ###     - Fill all your ports
    ###     - Have some spies bugout
    ### The spies each build a bugout ship, which does occupy a port while 
    ### it's en route. 
    ###
    ###
    ### Right now. threads are still existing, and reporting that they have 
    ### ships left to add to the queue, but no more ships are being added or 
    ### built.  I dunno what's going on.  Gotta build lots of ships for this 
    ### to eventually happen.  Need much better and informative logging to 
    ### figure it out.

    def __init__(self, app, p_id, yards:list, ships_to_build:dict, parent = None):
        """ Builds ships.

        Emits sig_empty when there are no more ships left to queue up.  
        sig_empty will contain a single argument, the ID of the planet whose 
        builder has completed.

        Arguments:
            yards (list): :class:`lacuna.buildings.callable.shipyard`
            build (dict): "shiptype (str)": num_to_build (int)
        Returns:
            recall (datetime.datetime): The time that the first of our shipyards comes
                                        available again.  When this time comes, the 
                                        main thread should re-call us to add more ships
                                        to the queues.
                                        IF there are no more ships left to build, we're 
                                        done, so ``recall`` will be None.
                                        This is a naive datetime object.  Its value will 
                                        be in UTC, but the object itself will be unaware.
        """
        QThread.__init__(self, parent)
        self.app                    = app
        self.p_id                   = p_id
        self.ships                  = ships_to_build
        self.yards                  = yards
        self.earliest_recall_time   = None      # datetime.datetime
        self.built                  = {}        # shiptype(str) => num_built(int)

    def request(self):
        """ Adds ships to the planet's shipyard build queues.

        Returns:
            recall_time (datetime.datetime): This is the first time that a
                                             shipyard's queue ends, and 
                                             request() should be called again 
                                             to re-fill the queues.  If there 
                                             are no ships left to build, this 
                                             will be None.
        """
        self.start()    # Automatically calls run()
        while(self.isRunning()):
            self.app.processEvents()
            time.sleep(0.1)
        retval = None
        if self.ships:
            retval = self.earliest_recall_time
        else:
            self.sig_empty.emit(self.p_id)
        return retval

    def get_yard_slots(self, yard):
        _, num_building_now, _ = yard.view_build_queue()
        return( yard.level - num_building_now )

    def run(self):
        for yard in self.yards:
            slots = self.get_yard_slots(yard)

            for shiptype in self.ships.keys():
                ttl_to_build = self.ships[shiptype]
                num_to_build = ttl_to_build
                if num_to_build > slots:
                    num_to_build = slots
                    self.ships[shiptype] -= num_to_build
                else:
                    self.ships[shiptype] = 0
                slots -= num_to_build
                ### CHECK
                print( 
                    "{}: {} is adding {} {} to the shipyard at ({}, {})."
                    .format(datetime.datetime.now(), self.p_id, num_to_build, shiptype, yard.x, yard.y) 
                )
                if num_to_build > 0:
                    yard.build_ship( shiptype, num_to_build )

                if shiptype in self.built:
                    self.built[shiptype] += num_to_build
                else:
                    self.built[shiptype] = num_to_build

                if slots <= 0:
                    break

            ### Remove shiptypes if the number left to build is 0.
            self.ships = {k:self.ships[k] for k in self.ships if self.ships[k] > 0}

            if self.earliest_recall_time:
                if yard.work.end_dt < self.earliest_recall_time:
                    self.earliest_recall_time = yard.work.end_dt
            else:
                self.earliest_recall_time = yard.work.end_dt

    def ships_left(self):
        return functools.reduce( (lambda x, y: x + y), self.ships.values() )


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
        if not self.fresh:
            self.app.client.cache_on('my_planets', 3600)
        self.planet = self.app.client.get_body_byname( self.pname )
        self.app.client.cache_off()
        self.dataReady.emit(self.planet) 


class GetSingleBuilding(QThread):
    """ Gets a single random building of a specific type.  Any level building may be 
    returned, but will only return buildings at 100% health.

    Example:
        bldg_getter = GetSingleBuilding( self.app, self.planet, 'spaceport' )
        sp = bldg_getter.request()
    """
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
        if not self.fresh:
            self.app.client.cache_on('my_buildings', 3600)
        try:
            self.bldg = self.planet.get_buildings_bytype( self.btype, 1, 1, 100 )[0]
        except err.NoSuchBuildingError as e:
            self.app.poperr( self.parent, "You don't have a working {}.".format(self.btype) )
            self.app.client.cache_off()
            return
        self.app.client.cache_off()
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
        if not self.fresh:
            self.app.client.cache_on('my_buildings', 3600)
        try:
            self.bldg = self.planet.get_building_id( self.type, self.id )
        except err.NoSuchBuildingError as e:
            self.app.poperr( self.parent, "You don't have a working {}.".format(self.btype) )
            self.app.client.cache_off()
            return
        self.app.client.cache_off()
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
        if not self.fresh:
            self.app.client.cache_on('my_buildings', 3600)
        try:
            self.bldgs = self.planet.get_buildings_bytype( self.btype, 1, 0, 100 )
        except err.NoSuchBuildingError as e:
            self.app.poperr( self.parent, "You don't have any working {} buildings.".format(self.btype) )
            self.app.client.cache_off()
            return
        self.app.client.cache_off()
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
        if not self.fresh:
            self.app.client.cache_on('my_ships', 3600)
        self.ships, cnt = self.sp.view_all_ships(self.paging, self.filter, self.sort)
        self.app.client.cache_off()
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
        if self.ids:
            self.sp.mass_scuttle_ship( self.ids )
            self.app.client.cache_clear('my_buildings')
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
        if not self.fresh:
            self.app.client.cache_on('my_ships', 3600)
        self.ships, self.docks, self.bq_max, self.bq_used = self.sy.get_buildable()
        self.app.client.cache_off()
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
        if not self.fresh:
            self.app.client.cache_on('my_ships', 3600)
        self.ships, self.docks_free, self.docks_max = self.sp.view()
        self.app.client.cache_off()
        self.dataReady.emit(self.ships) 

