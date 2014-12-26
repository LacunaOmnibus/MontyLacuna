
import lacuna, lacuna.exceptions, lacuna.binutils.libbin
import argparse, os, sys

class SendExcavs(lacuna.binutils.libbin.Script):
    """
    Attributes::

        ally            The user's lacuna.alliance.MyAlliance object, or False 
                        if the user is not in an alliance.
        arch            The Archaeology Ministry on self.planet.
        args            Command-line arguments set by the user; the result of
                        self.parser.parse_args()
        bad_stations    Dict of names ( {name: 1} ) of stations we've 
                        encountered that won't accept excavs (MO laws).
        cell_number     The cell we're working on.  Starts at 1.
        client          lacuna.clients.Member object
        excav_sites     A list of lacuna.ship.Excavator objects.  Starts
                        as an empty list, set to the correct value by 
                        get_excav_count().  Does not include the current planet 
                        in the list.
        map             lacuna.map.Map object
        num_excavs      Number of excavs to be sent from self.planet.  Starts
                        at 0, set to the correct value by get_excav_count().
        parser          argparse.ArgumentParser object
        planet          lacuna.body.MyBody object for the planet name passed
                        at the command line.
        ring_offset     The ring offset we're working on.  Starts at 0.
        sp              A Space Port on self.planet (doesn't matter which one).
        travelling      Dict of bodies we have excavators on their way to right 
                        now.  { destination_body_id: 1 }
        version         '0.1'
    """

    def __init__(self):
        self.version = '0.1'
        parser = argparse.ArgumentParser(
            description = '''
                    Sends available excavators out to nearby planets of the 
                    requested type or types.
                ''',
            epilog = 'Example: python bin/send_excavs.py -tp33 -tp35 Earth',
        )
        parser.add_argument( 'name', 
            metavar     = '<planet>',
            action      = 'store',
            help        = 'The planet from which to send excavators.'
        )
        parser.add_argument( '-t', '--t',
            dest        = 'ptypes',
            metavar     = '<ptype>',
            action      = 'append',
            choices     = [ 'p'+ str(i) for i in range(1,41) ],
            help        = 'The types of planets to send excavators towards.  You can include multiple planets by repeating "-t <ptype>" for each type you want to send to.'
        )
        parser.add_argument( '--max_ring', 
            metavar     = '<max_ring>',
            action      = 'store',
            type        = int,
            default     = 3,
            help        = "Each 'ring' represents a 54 unit square ring around the original planet.  The bigger max_ring is, the farther away we'll send excavators.  Defaults to 3."
        )
        parser.add_argument( '--max_send', 
            metavar     = '<max_send>',
            action      = 'store',
            type        = int,
            default     = 99,
            help        = "Will send this number of excavators, maximum.  If you want to send an even number of excavators to, say, p11 and p12 planets, run this program once for each type, with a max_send of 10 for each."
        )

        super().__init__(parser)

        self.client.cache_on( 'my_colonies', 3600 )
        self.planets = []
        if self.args.name == 'all':
            for colname in self.client.empire.colony_names.keys():
                self.planets.append(colname)
        else:
            self.planets = self.args.name
        self.client.cache_off()

        self.client.user_logger.debug( "Getting user's alliance." )
        self.ally           = self.client.get_my_alliance()
        self.excav_sites    = []
        self.bad_stations   = {}
        self.client.user_logger.debug( "Getting star map." )
        self.map            = self.client.get_map()
        self.num_excavs     = 0
        self.travelling     = {}


    def set_planet( self, pname:str ):
        self.planet = self.client.get_body_byname( pname )
        self.client.user_logger.info( "----- Sending excavs from " + pname + "." )
        self.planet = self.client.get_body_byname( pname )
        self.ring   = Ring(self.planet, 0)
        self.client.user_logger.debug( "Getting Arch Min for {}.".format(pname) )
        self.arch   = self.planet.get_buildings_bytype( 'archaeology', 1, 1, 100 )[0]
        self.client.user_logger.debug( "Getting Space Port." )
        self.sp     = self.planet.get_buildings_bytype( 'spaceport', 1, 1, 100 )[0]
        self.client.user_logger.debug( "Making note of travelling excavs." )
        self.note_travelling_excavators()
        self.client.user_logger.debug( "Getting usable excav count." )
        self.get_excav_count()


    def get_ready_excavators(self):
        """ Returns the number of excavators onsite that have completed building
        """
        paging = {}
        filter = {'type': 'excavator'}
        ships, excavs = self.sp.view_all_ships( paging, filter )
        excavs_built = []
        for i in ships:
            if i.task == 'Docked':
                excavs_built.append(i)
        return len(excavs_built)


    def note_travelling_excavators(self):
        """ Makes a note of any planets we currently have excavators travelling 
        to.  Returns nothing, but sets self.travelling.
        """
        paging = {}
        filter = {'task': 'Travelling'}
        travelling_ships, travelling_count = self.sp.view_all_ships( paging, filter )
        for s in travelling_ships:
            if s.type == 'excavator':
                self.travelling[ s.to.id ] = 1


    def get_excav_count( self ):
        """ Set the number of excavs this planet is able to send right now.

        Returns nothing, but sets ``self.num_excavs``.
        """
        self.client.cache_off() # we need fresh data for this method

        ### Omit the first excav site; it's our current planet.
        excav_sites, excav_max, num_travelling = self.arch.view_excavators()
        self.excav_sites = excav_sites[1:]

        ### Get count of built and ready excavators onsite
        num_excavs_ready = self.get_ready_excavators()

        ### Here, num_excavs is the number of additional excavators that the 
        ### Arch Min has room for, taking into account its available slots and 
        ### what's out there travelling.
        self.num_excavs = (excav_max - (len(self.excav_sites) + num_travelling) )
        self.client.user_logger.info( "Arch min has {} slots available.".format(self.num_excavs) )
        if self.num_excavs <= 0:
            return

        ### If we have fewer excavators ready to go than the Arch Min has 
        ### slots available, shorten self.num_excavs.
        self.client.user_logger.debug( "Space port has {} excavators ready.".format(num_excavs_ready) )
        if num_excavs_ready < self.num_excavs:
            self.num_excavs = num_excavs_ready
        self.client.user_logger.info( "We're ready to send out {} more excavators.".format(self.num_excavs) )

        ### Last, if the user specified a max_send, make sure we're limiting 
        ### the number to send this run to the user's spec.
        if self.num_excavs > self.args.max_send:
            self.client.user_logger.debug( "We have more excavators ready than you wanted to use - limiting to your spec." )
            self.num_excavs = self.args.max_send


    def get_map_square( self ):
        """ Gets a list of stars in the next map square.  

        ``self.ring`` keeps track of which map square is "next", so no arguments 
        need be passed in.

        Returns a list of lacuna.map.Star objects.
        """
        ### Get the next cell in our current ring.  If we've exhausted our 
        ### current ring, move out one more ring.
        req_cell = self.ring.get_next_cell()
        if not req_cell:
            next_offset = self.ring.ring_offset + 1
            if next_offset > self.args.max_ring:
                ### We've exhausted our allowed range, so there are no more 
                ### excavs to send.
                self.num_excavs = 0
                return
            self.ring = Ring( self.planet, next_offset )
            req_cell = self.ring.get_next_cell()

        self.client.user_logger.debug( 
            "Requested cell {} offset {}, row {}, col {}, centerpoint is ({}, {})."
            .format(
                self.ring.this_cell_number, self.ring.ring_offset, 
                req_cell.row, req_cell.col, req_cell.center_x, req_cell.center_y
            )
        )
        self.client.user_logger.debug( "Requested cell top {}, bottom {}, left {}, right {}."
            .format(req_cell.top, req_cell.bottom, req_cell.left, req_cell.right)
        )

        star_list = self.map.get_star_map({
            'top':      req_cell.top,   'right':    req_cell.right,
            'bottom':   req_cell.bottom, 'left':    req_cell.left 
        })
        return star_list


    def star_seizure_forbids_excav( self, star ):
        """ Lets you know if the laws affecting a star forbid you from sending 
        excavators to that star's planets.

        **NO WORKY WORKY**
            This currently (12/16/2014) works on PT, but not on US1 yet.

        Arguments:
            - star -- lacuna.map.Star object

        Returns True if the star's laws forbids you from excavating its planets, 
        False otherwise.
        """
        if not hasattr(star, 'station'):
            return False
        if star.station.name in self.bad_stations:
            self.client.user_logger.debug("This star's station has already been found to have MO Excav law turned on." )
            return True
        if self.ally:
            if star.station.id == self.ally.id:
                self.client.user_logger.debug("This star has been seized, but it's by my alliance." )
                return False
        laws = star.view_nonseizure_laws()
        for l in laws:
            if l.name == 'Members Only Excavation':
                self.client.user_logger.debug("Whoops - this star has MO Excav law turned on, and not by my alliance.  Skipping." )
                self.bad_stations[star.station.name] = 1
                return True
        return False

    def send_excavs_to_bodies_orbiting(self, stars:list):
        """ Sends excavators to the bodies around each star in a list, provided 
        each body is of one of the requested types.

        Arguments:
            - stars -- list of lacuna.map.Star objects

        Returns the number of excavators sent.
        """
        cnt = 0
        for s in stars:
            if self.star_seizure_forbids_excav( s ):
                self.client.user_logger.debug("Station {} has MO Excav law on.  Skipping." .format(s.station.name) )
                continue
            cnt += self.send_excavs_to_bodies( s, s.bodies )
            if self.num_excavs <= 0:
                return cnt
        return cnt


    def send_excavs_to_bodies(self, star, bodies:list):
        """ Tries to send an excavator to each body in a list of bodies, 
        provided each body is of one of the requested types.

        Arguments:
            - bodies -- list of body.Body objects

        Returns the integer count of excavators sent.
        """
        cnt = 0
        for b in bodies:
            cnt += self.send_excav_to_matching_body(star, b)
            if self.num_excavs <= 0:
                return cnt
        return cnt

    def get_available_excav_for( self, target:dict ):
        """ Finds a single excavator to be sent to target.

        Arguments:
            - target -- Standard target dict

        Returns
            - excavator -- Either a single lacuna.ship.ExistingShip object 
              representing an excavator, or False if no available excavators 
              could be found.
        """
        avail = self.sp.get_available_ships_for( target )
        for s in avail:
            if s.type == 'excavator':
                return s
        return False

    def send_excav_to_matching_body(self, star, body):
        """ Tries to send an excavator to a body.

        Arguments:
            - body -- A lacuna.body.Body object

        If the body is not one of the requested types, or we already have an 
        excavator there, or the body's star is seized by another alliance's 
        Space Station and it has Members Only Excavation law set, this will 
        fail to send an excavator and return 0.

        If everything works out, this will send an excavator, decrement 
        self.num_excavs, and return 1.
        """
        if hasattr(body, 'empire'):
            self.client.user_logger.debug("Planet {} ({},{}) is inhabited.  Next!" .format(body.name, body.x, body.y) )
            return 0

        if body.id in self.travelling:
            self.client.user_logger.info("We already have an excav on the way to {}.  Next!" .format(body.name) )
            return 0

        if body.type != 'habitable planet':
            self.client.user_logger.debug("Planet {} is not habitable." .format(body.name) )
            return 0

        if body.surface_type in self.args.ptypes:
            self.client.user_logger.debug("Planet {} ({},{}) is habitable, uninhabited, and the correct type." .format(body.name, body.x, body.y) )
        else:
            self.client.user_logger.debug("Planet {} is not the correct type." .format(body.name) )
            return 0

        for e in self.excav_sites:
            if e.body == body.name:
                self.client.user_logger.debug("We already have an excav at {}." .format(body.name) )
                return 0

        target  = { "body_name": body.name }
        excav = self.get_available_excav_for( target )
        if not excav:
            self.client.user_logger.debug("We can't send an excavator to this target.  We probably already sent an excav from a previous run.")
            return 0

        try:
            self.sp.send_ship( excav.id, target )
        except lacuna.exceptions.ServerError as e:
            self.client.user_logger.debug("Encountered ServerError code {}, message {}."
                .format(e.code, e.text)
            )
            return 0
        except Exception as e:
            ### Probably either MO excavation is on or if we already have an 
            ### excavator en route to this body.
            ### MO Excav laws _should_ have already been checked, but a race 
            ### condition exists here; it's possible the law was just now 
            ### passed, after the check was performed.
            self.client.user_logger.debug("Encountered {}, ({}) trying to send excav to {} ({}, {})."
                .format(type(e), e, body.name, body.x, body.y)
            )
            return 0
        else:
            self.client.user_logger.info( "We just sent an excavator to {} ({},{}).".format(body.name, body.x, body.y) )
            self.num_excavs -= 1
            return 1

class Ring():
    """ A ring of cells radiating out from a planet.

    Attributes::

        cell_size           Integer size of the sides of the cells in the ring.
        cells_per_row       Number of cells per row (3 for a ring_offset of 1)
        cells_this_ring     Total number of cells in this ring only (8 for a 
                            ring_offset of 1)
        center_cell_number  the cell_number of the center cell (1 for a 
                            ring_offset of 0, 5 for a ring_offset of 1, etc)
        center_col          The column occupied by the center cell.  0-based. 
        center_row          The row occupied by the center cell.  0-based.  
        this_cell_number    Integer number of the cell just returned by
                            get_next_cell().  Starts at 0, which is not a 
                            valid cell number.
        planet              lacuna.body.MyBody object everything is relative 
        to.
        ring_offset         Integer offset from the center (center is 0)
        total_cells         Total number of cells in the square, including all 
                            rings (9 for a ring_offset of 1)

    cell_size
        The max area that ``lacuna.map.Map.get_star_map()`` will return is 
        3001.  The closest square to that is 54x54 (giving an area of 2916), 
        so the length of any dimension of any cell is hardcoded at 54.

    Rings Diagram
        The diagram below shows ring_offset 0 and, surrounding it, 
        ring_offset 1.

        In the diagram, the center_cell_number is either 1 (at ring_offset 0) 
        or 5 (at ring_offset  1).  The other cells are numbered assuming 
        ring_offset  1, since those other cells don't exist for ring_offset 0.

        Each increase in ring_offset  will add another layer of cells 
        around the previous layer, just as ring_offset  1 adds a full 
        layer of cells wrapped around the single cell at ring_offset  0::

            +----------+ +----------+ +----------+
            | offset 1 | | offset 1 | | offset 1 |
            |          | |          | |          |
            | count 1  | | count 2  | | count 3  |
            +----------+ +----------+ +----------+
            +----------+ +----------+ +----------+
            | offset 1 | |offset 0/1| | offset 1 |
            |          | |    o     | |          |
            | count 4  | |count 1/5 | | count 6  |
            +----------+ +----------+ +----------+
            +----------+ +----------+ +----------+
            | offset 1 | | offset 1 | | offset 1 |
            |          | |          | |          |
            | count 7  | | count 8  | | count 9  |
            +----------+ +----------+ +----------+

    """
    def __init__( self, planet, ring_offset:int = 0 ):
        self.planet                         = planet
        self.ring_offset                    = ring_offset
        self.cells_this_ring                = int( 8 * self.ring_offset )
        self.cells_per_row                  = int( (2 * self.ring_offset + 1) )
        self.total_cells                    = int( self.cells_per_row**2 )
        self.center_cell_number             = int( (self.total_cells + 1) / 2 )
        self.next_cell_number               = 0
        self.cell_size                      = 54
        self._set_center_location()

    def _set_center_location(self):
        self.center_row = 0
        self.center_col = self.center_cell_number - 1 # cell numbers start at 1
        while( self.center_col > self.cells_per_row ):
            self.center_row += 1
            self.center_col -= self.cells_per_row

    def _get_cell_location(self, num):
        row         = 0
        col         = num - 1
        center_x    = 0
        center_y    = 0
        while( col > self.cells_per_row ):
            row += 1
            col -= self.cells_per_row
        if row < self.center_row:
            center_y = (self.planet.y - self.cell_size) * (self.center_row - row)
        elif row > self.center_row:
            center_y = (self.planet.y + self.cell_size) * (row - self.center_row)
        if col < self.center_col:
            center_x = (self.planet.x - self.cell_size) * (self.center_col - col)
        elif col > self.center_col:
            center_x = (self.planet.x + self.cell_size) * (col - self.center_col)
        return( col, row, center_x, center_y )

    def get_next_cell(self):
        """ Gets the next cell in the ring.

        Starts at cell 1, the upper-left-most cell on the first call, then 
        proceeds left-to-right, top-to-bottom on successive calls.

        After returning the final cell in the ring, the next call will return 
        False and then reset the count.
        """
        if not hasattr(self, 'next_cell'):
            self.next_cell = self._gen_next_cell()
        try:
            return next(self.next_cell)
        except StopIteration:
            self.next_cell = self._gen_next_cell()
            return False

    def _gen_next_cell(self):
        for i in range(1, self.total_cells + 1):
            self.this_cell_number = i
            col, row, x, y = self._get_cell_location( i )
            yield Cell( col, row, x, y, self.cell_size )

class Cell():
    """

    Attributes::

        bottom              Y coordinate of the bottom boundary of the cell
        center_x            X coordinate of the center point of the cell.
        center_y            Y coordinate of the center point of the cell.
        col                 The column occupied by the current cell.  0-based.
        left                X coordinate of the left boundary of the cell
        cell_size           Size of the sides of the cell
        right               X coordinate of the right boundary of the cell
        row                 The row occupied by the current cell.  0-based.
        top                 Y coordinate of the top boundary of the cell

    **Cell Diagram**
    In ring.ring_offset == 0::

        +--------+
        | cell 1 |
        | col 0  |
        | row 0  |
        +--------+

    cell 1 from the ring_offset == 0 above becomes cell 5 when ring_offset 
    == 1::

        +--------++--------++--------+
        | cell 1 || cell 2 || cell 3 |
        | col 0  || col 1  || col 2  |
        | row 0  || row 0  || row 0  |
        +--------++--------++--------+
        +--------++--------++--------+
        | cell 4 || cell 5 || cell 6 |
        | col 0  || col 1  || col 2  |
        | row 1  || row 1  || row 1  |
        +--------++--------++--------+
        +--------++--------++--------+
        | cell 7 || cell 8 || cell 9 |
        | col 0  || col 1  || col 2  |
        | row 2  || row 2  || row 2  |
        +--------++--------++--------+
    """

    def __init__( self, col, row, x, y, cell_size ):
        self.col        = col
        self.row        = row
        self.center_x   = x
        self.center_y   = y
        self.cell_size  = cell_size
        self._set_bounding_points()

    def _set_bounding_points(self):
        self.left    = self.center_x - (self.cell_size / 2)
        self.right   = self.center_x + (self.cell_size / 2)
        self.top     = self.center_y + (self.cell_size / 2)
        self.bottom  = self.center_y - (self.cell_size / 2)

        if self.top < -1500 or self.bottom > 1500 or self.left > 1500 or self.right < -1500:
            ### CHECK this needs to do something more reasonable than bailing.
            self.client.user_logger.debug( "This cell is entirely out of bounds." )
            quit()
        ### At least part of the cell is in bounds.  But parts of it might lap 
        ### over the boundaries -- fix anything outside the limits of the map.
        self.top     =  1500 if self.top     > 1500 else self.top
        self.right   =  1500 if self.right  >  1500 else self.right
        self.bottom  = -1500 if self.bottom < -1500 else self.bottom
        self.left    = -1500 if self.left   < -1500 else self.left

