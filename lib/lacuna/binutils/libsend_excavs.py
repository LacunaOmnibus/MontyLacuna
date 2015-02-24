
import lacuna, lacuna.exceptions, lacuna.binutils.libbin
import argparse, operator, os, sys
from enum import Enum

class BodyCache():
    """ We don't want to use a request cache for any part of send_excavs, but we 
    do want to keep track of stations, stars, and bodies that we know are no 
    good for whatever reason.
    """
    def __init__(self):
        self.stations   = {}
        self.stars      = {}
        self.planets    = {}

    def is_bad(self, body_name, type = 'planet'):
        """ Checks to see if a given body is known to be bad.

        Arguments:
            - body_name -- Str name of the body to mark as bad.
            - type -- Str type of body.  Either 'star', 'station', or 'planet'.  
              Defaults to 'planet'.

        Returns a boolean.  True if the body is known to be bad.
        """
        if body_name in self.stations:
            return True
        elif body_name in self.stars:
            return True
        elif body_name in self.planets:
            return True
        return False

    def mark_as_bad(self, body_name, type = 'planet'):
        """ Marks a given body as 'bad' in the cache.

        Arguments:
            - body_name -- Str name of the body to mark as bad.
            - type -- Str type of body.  Either 'star', 'station', or 'planet'.
              Defaults to 'planet'.
        """
        if type == 'planet':
            self.planets[body_name] = True
        elif type == 'station':
            self.stations[body_name] = True
        elif type == 'star':
            self.stars[body_name] = True
        else:
            raise Exception("{}: illegal type.".format(type))
        return False


class SendExcavs(lacuna.binutils.libbin.Script):
    """
    Attributes::

        ally            The user's lacuna.alliance.MyAlliance object, or False 
                        if the user is not in an alliance.
        ally_members    List of Strings; the names of the members of my 
                        alliance.  Used to determine if an inhabited planet is 
                        hostile or not.
        arch            The Archaeology Ministry on self.planet.
        args            Command-line arguments set by the user; the result of
                        self.parser.parse_args()
        body_cache      A libsend_excavs.BodyCache object.
        cell_number     The cell we're working on.  Starts at 1.
        client          lacuna.clients.Member object
        excav_sites     A list of lacuna.ship.Excavator objects.  Starts
                        as an empty list, set to the correct value by 
                        set_excav_count().  Does not include the current planet 
                        in the list.
        map             lacuna.map.Map object
        num_excavs      Number of excavs to be sent from self.planet.  Starts
                        at 0, set to the correct value by set_excav_count().
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
            epilog = 'Full docs can be found at http://tmtowtdi.github.io/MontyLacuna/scripts/send_excavs.html',
        )
        parser.add_argument( 'name', 
            metavar     = '<planet>',
            action      = 'store',
            help        = "The planet from which to send excavators.  Enter 'all' to send from all of your planets."
        )
        parser.add_argument( '-t', '--t',
            dest        = 'ptypes',
            metavar     = '<ptype>',
            action      = 'append',
            choices     = [ 'p'+ str(i) for i in range(1,41) ],
            required    = 1,
            help        = 'The types of planets to send excavators towards.  You can include multiple planets by repeating "-t <ptype>" for each type you want to send to.  Defaults to any planet type (so you probably want to specify this).'
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

        self.ally           = None
        self.ally_members   = []
        self.body_cache     = BodyCache()
        self.excav_sites    = []
        self.num_excavs     = 0
        self.planets        = []
        self.travelling     = {}

        self._set_planets()
        self._set_alliance()
        self.map = self.client.get_map()

    
    def _set_planets(self):
        self.client.cache_on( 'my_colonies', 3600 )
        if self.args.name == 'all':
            for colname in self.client.empire.colony_names.keys():
                self.planets.append(colname)
        else:
            self.planets = [ self.args.name ]
        self.client.cache_off()

    def _set_alliance(self):
        self.client.user_logger.debug( "Getting user's alliance." )
        self.ally = self.client.get_my_alliance()
        if self.ally:
            self._set_alliance_members()

    def _set_alliance_members(self):
        for m in self.ally.members:
            self.ally_members.append( m.name )

    def set_planet( self, pname:str ):
        self.client.user_logger.info( "Sending excavs from " + pname + "." )
        self.planet = self.client.get_body_byname( pname )
        self.ring   = Ring(self.planet, 0)
        self.client.user_logger.debug( "Getting Arch Min for {}.".format(pname) )
        self.arch   = self.planet.get_buildings_bytype( 'archaeology', 1, 1, 100 )[0]

        ### Get the number of excav slots before doing anything else - if we 
        ### have no available slots left, there's no need to continue.
        excav_sites, excav_max, num_travelling = self.arch.view_excavators()
        self.excav_sites = excav_sites[1:] # Omit the first excav site; it's our current planet.
        self.num_excavs = (excav_max - (len(self.excav_sites) + num_travelling) )
        self.client.user_logger.info( "Arch min has {} slots available.".format(self.num_excavs) )
        if self.num_excavs <= 0:
            return

        self.client.user_logger.debug( "Getting Space Port." )
        self.sp     = self.planet.get_buildings_bytype( 'spaceport', 1, 1, 100 )[0]
        self.client.user_logger.debug( "Making note of travelling excavs." )
        self.note_travelling_excavators()
        self.client.user_logger.debug( "Getting usable excav count." )
        self.set_excav_count()


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


    def set_excav_count( self ):
        """ Set the number of excavs this planet is able to send right now.

        Returns nothing, but sets ``self.num_excavs``.
        """
        self.client.cache_off() # we need fresh data for this method

        ### Get count of built and ready excavators onsite
        num_excavs_ready = self.get_ready_excavators()

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
                self.client.user_logger.debug( "We've checked out to our max_ring; done." )
                self.num_excavs = 0
                return
            self.client.user_logger.debug( "Moving out to ring number {}.".format(next_offset) )
            self.ring = Ring( self.planet, next_offset )
            req_cell = self.ring.get_next_cell()
        self.client.user_logger.debug( "Checking cell number {}.  Top {}, bottom {}, left {}, right {}."
            .format(self.ring.this_cell_number, req_cell.top, req_cell.bottom, req_cell.left, req_cell.right)
        )

        if req_cell.top <= -1500 or req_cell.bottom >= 1500 or req_cell.left <= -1500 or req_cell.right >= 1500:
            self.client.user_logger.debug( "This cell is out of bounds." )
            return []

        star_list = self.map.get_star_map({
            'top':      req_cell.top,   'right':    req_cell.right,
            'bottom':   req_cell.bottom, 'left':    req_cell.left 
        })
        ### The order of the stars returned doesn't really matter too much, 
        ### but having them sorted makes it easier to debug.
        return sorted( star_list, key=operator.attrgetter('x', 'y') )


    def star_seizure_forbids_excav( self, star ):
        """ Lets you know if the laws affecting a star forbid you from sending 
        excavators to that star's planets.

        Arguments:
            - star -- lacuna.map.Star object

        Returns True if the star's laws forbids you from excavating its planets, 
        False otherwise.
        """
        if not hasattr(star, 'station'):
            return False
        if self.body_cache.is_bad(star.station.name, 'station'):
            self.client.user_logger.debug("This star's station has already been found to have MO Excav law turned on." )
            return True
        if self.ally:
            if star.station.alliance.id == self.ally.id:
                self.client.user_logger.debug("This star has been seized, but it's by my alliance." )
                return False
        laws = star.view_nonseizure_laws()
        for l in laws:
            if l.name == 'Members Only Excavation':
                self.client.user_logger.debug("Whoops - this star has MO Excav law turned on, and not by my alliance.  Skipping." )
                self.body_cache.mark_as_bad(star.station.name, 'station')
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
            self.client.user_logger.info("Checking on star '{}'." .format(s.name) )
            if self.body_cache.is_bad(s.name, 'star'):
                self.client.user_logger.debug("We've already discovered that the star {} is no good.  Skipping."
                    .format(s.name))
                continue
            if self.star_seizure_forbids_excav( s ):
                self.client.user_logger.debug("Station {} has MO Excav law on.  Skipping." .format(s.station.name) )
                self.body_cache.mark_as_bad(s.name, 'star')
                continue
            if self.system_contains_hostiles( s ):
                self.client.user_logger.debug("Star {} has at least one hostile colony that would shoot down our excav.  Skipping."
                    .format(s.name))
                self.body_cache.mark_as_bad(s.name, 'star')
                continue
            cnt += self.send_excavs_to_bodies( s, s.bodies )
            if self.num_excavs <= 0:
                self.client.user_logger.debug("We're out of excavators (or slots) so can't send out any more.  Done on {}."
                    .format(self.planet.name))
                return cnt
        return cnt

    
    def system_contains_hostiles( self, star ):
        """ Checks if any of the planets orbiting a star is owned by a hostile 
        empire.

        Arguments:
            - star -- lacuna.Map.Star object

        Returns True if there's a hostile colony orbiting the star, False 
        otherwise.
        """
        if not hasattr(star, 'bodies'): # Pretty rare, but possible, I guess.
            return False
        for b in star.bodies:
            if not hasattr(b, 'empire'):
                continue
            if b.empire.name in self.ally_members:
                continue
            else:
                self.body_cache.mark_as_bad(star.name, 'star')
                return True
        return False
            


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
            if self.body_cache.is_bad(star.name, 'star'):
                ### send_excav_to_matching_body() found that a planet in this 
                ### system is inhabited, so the whole star is bad.  No need to 
                ### continue checking this system.
                return cnt
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
        avail = self.sp.get_task_ships_for( target, 'available' )
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
        if self.body_cache.is_bad(body.name, 'planet'):
            self.client.user_logger.debug("A previous check showed that {} is no good.  Next!" .format(body.name) )
            return 0

        if hasattr(body, 'empire'):
            self.client.user_logger.debug("Planet {} ({},{}) is inhabited.  Next!" 
                .format(body.name, body.x, body.y)
            )
            ### A body in the system is inhabited; this makes the entire 
            ### system bad, so mark the star, not just the body.
            self.body_cache.mark_as_bad(star.name, 'star')

            self.body_cache.mark_as_bad(body.name, 'planet')
            return 0

        if body.id in self.travelling:
            self.client.user_logger.info("We already have an excav on the way to {}.  Next!" .format(body.name) )
            self.body_cache.mark_as_bad(body.name, 'planet')
            return 0

        if body.type != 'habitable planet':
            self.client.user_logger.debug("Planet {} is not habitable." .format(body.name) )
            self.body_cache.mark_as_bad(body.name, 'planet')
            return 0

        if body.surface_type in self.args.ptypes:
            self.client.user_logger.debug("Planet {} ({},{}) is habitable, uninhabited, and the correct type ({})." 
                .format(body.name, body.x, body.y, body.surface_type)
            )
        else:
            self.client.user_logger.debug("Planet {} is not the correct type ({})." .format(body.name, body.surface_type) )
            self.body_cache.mark_as_bad(body.name, 'planet')
            return 0

        for e in self.excav_sites:
            if e.body.name == body.name:
                self.client.user_logger.debug("We already have an excav at {}." .format(body.name) )
                self.body_cache.mark_as_bad(body.name, 'planet')
                return 0

        target  = { "body_id": body.id }    # don't use body_name to avoid unicode names.
        excav = self.get_available_excav_for( target )
        if not excav:
            self.client.user_logger.debug("We can't send an excavator to this target.  We probably already have an excav there.")
            self.body_cache.mark_as_bad(body.name, 'planet')
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
            self.body_cache.mark_as_bad(body.name, 'planet')
            return 0
        else:
            self.client.user_logger.info( "We just sent an excavator to {} ({},{}).".format(body.name, body.x, body.y) )
            self.num_excavs -= 1
            return 1

class Point():
    def __init__( self, x, y ):
        self.x   = x
        self.y   = y

class Ring():   # by Josten's
    """ A ring of cells radiating out from a planet.

    Row and column numbers, as well as ring offsets, start at zero.  Cell 
    numbers start at 1.

    Attributes::

        cell_size           Integer size of the sides of the cells in the ring.
        cells_per_row       Number of cells per row (3 for a ring_offset of 1)
        cells_this_ring     Total number of cells in this ring only (8 for a 
                            ring_offset of 1)
        center_cell         Cell object; the cell in the middle.
        center_cell_number  The number of the center cell.  Numbering starts at 
                            1 in the ring's NW corner cell.
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
        self.planet                 = planet
        self.ring_offset            = ring_offset
        self.cells_this_ring        = int( 8 * self.ring_offset )
        self.cells_per_row          = int( (2 * self.ring_offset + 1) )
        self.total_cells            = int( self.cells_per_row ** 2 )
        self.center_cell_number     = int( (self.total_cells + 1) / 2 )
        self.next_cell_number       = 0
        self.cell_size              = 54
        self._set_center_location() 
        self._set_center_cell()

    def _set_center_location(self):
        self.center_cell_number     = int( (self.total_cells + 1) / 2 )
        self.center_col             = self.center_cell_number - 1 # cell numbers start at 1
        while( self.center_col > self.cells_per_row ):
            self.center_col -= self.cells_per_row
        self.center_row = self.center_col

    def _set_center_cell(self):
        self.center_cell = Cell( Point(self.planet.x, self.planet.y), self.cell_size )

    def _get_cell_location(self, num):
        """ Find a cell's location in the ring, given its number.

        Arguments:
            - num -- Integer number of the cell.  The NW-most cell is 1; 
              numbering is left-to-right, top-to-bottom.  So, for ring_offset of 
              1, the bottom-right cell's number will be 9.

        Returns a tuple:
            - column (numbering starts at 0)
            - row (numbering starts at 0)
            - Point object (the cell's centerpoint)
        """
        row  = 0
        col  = num - 1
        x    = 0
        y    = 0
        while( col >= self.cells_per_row ):
            row += 1
            col -= self.cells_per_row
        row_diff = row - self.center_row        # 0 for cell 4
        col_diff = col - self.center_col        # -1 for cell 4

        ### We have to reverse the signs if we're starting out negative.  ie 
        ### if our center point's x is negative, to go up in space we have to 
        ### subtract.
        if self.center_cell.center_point.x < 0:
            col_diff *= -1
        if self.center_cell.center_point.y < 0:
            row_diff *= -1

        x = self.center_cell.center_point.x + (col_diff * self.cell_size)
        y = self.center_cell.center_point.y + (row_diff * self.cell_size)
        return( col, row, Point(x, y) )

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
            col, row, point = self._get_cell_location( i )
            yield Cell( point, self.cell_size )

class Cell():
    """
    Attributes::

        bottom              Y coordinate of the bottom boundary of the cell
        center_point        Point object - the center of the cell.
        left                X coordinate of the left boundary of the cell
        cell_size           Size of the sides of the cell
        right               X coordinate of the right boundary of the cell
        top                 Y coordinate of the top boundary of the cell

    Constructor will raise Cell.OutOfBoundsError if the entire cell is out of 
    bounds, so be sure to create a new cell in a try block.

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

    class OutOfBoundsError(Exception):
        """ The entire cell is out of bounds """
        def __init__(self, value):
            self.value = value
        def __str__(self):
            return repr(self.value)

    def __init__( self, point:Point, cell_size ):
        self.center_point   = point
        self.cell_size      = cell_size
        self._set_bounding_points()

    def _set_bounding_points(self):
        self.left    = int( self.center_point.x - (self.cell_size / 2) )
        self.right   = int( self.center_point.x + (self.cell_size / 2) )
        self.top     = int( self.center_point.y + (self.cell_size / 2) )
        self.bottom  = int( self.center_point.y - (self.cell_size / 2) )

        if self.top < -1500 or self.bottom > 1500 or self.left > 1500 or self.right < -1500:
            ### The cell is completely out of bounds.  But we don't want to 
            ### stop iteration.  eg the top row of cells could be out of 
            ### bounds, leaving the other rows in bounds.  If we stopped 
            ### iteration, we'd never process the following in-bounds cells.  
            ### So for out-of-bounds cells, just return a single point that's 
            ### in bounds, but which won't contain any stars.  ie don't do 
            ### anything different.
            pass
        ### Limit any part of the cell that laps out of bounds to being just 
        ### barely in-bounds.  Making TLE Map module requests with 
        ### out-of-bounds coords is an error.
        self.top     =  1500 if self.top     > 1500 else self.top
        self.right   =  1500 if self.right  >  1500 else self.right
        self.bottom  = -1500 if self.bottom < -1500 else self.bottom
        self.left    = -1500 if self.left   < -1500 else self.left

