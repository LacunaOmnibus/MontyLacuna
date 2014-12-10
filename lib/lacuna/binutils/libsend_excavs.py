
import lacuna, lacuna.exceptions, lacuna.binutils.libbin
import argparse, os, sys

"""
python bin/send_excavs.py --t p23 --t p24 --t p25 --max_ring 3 Earth
    This doesn't build excavs; you have to manage that manually or with another script.

Current issues with this:
    - If you send an excav from Earth to Target_A, then run this for Mars, and 
      it also tries to send an excav to Target_A, the send from Mars will be 
      disallowed (because you already have an excav from your empire on the 
      way).  This will be mis-interpreted as being because of a MO Excavation 
      law.  The station that has seized Target_A will then be added to the 
      list of "bad_stations", and no more excavs will be sent to any planet 
      under that station's jurisdiction.  And that station may well be your 
      own station, so perfectly valid planets will be skipped.

Other than that, this seems to be working.  I'd like to return to it once the 
view_laws() thing is straightened out.

"""

class SendExcavs(lacuna.binutils.libbin.Script):
    """
    Attributes::

        arch            The Archaeology Ministry on self.planet.
        args            Command-line arguments; the result of
                        self.parser.parse_args()
        bad_stations    Dict of names ( {name: 1} ) of stations we've 
                        encountered that won't accept excavs (MO laws).
        cell_number     The cell we're working on.  Starts at 1.
        client          lacuna.clients.Member object
        excav_sites     A list of lacuna.ship.Excavator objects.  Starts
                        as an empty list, set to the correct value by 
                        get_excav_count().
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
            description = 'I SHOW UP ABOVE THE OPTIONS SECTION IN HELP',
            epilog      = 'I SHOW UP BELOW THE OPTIONS SECTION IN HELP',
        )
        parser.add_argument( 'name', 
            metavar     = '<planet>',
            action      = 'store',
            help        = 'All spies from this planet will be recalled.'
        )
        parser.add_argument( '--t', 
            dest        = 'ptypes',
            metavar     = '<ptype>',
            action      = 'append',
            choices     = [ 'p'+ str(i) for i in range(1,41) ],
            help        = 'All spies from this planet will be recalled.'
        )
        parser.add_argument( '--max_ring', 
            metavar     = '<max_ring>',
            action      = 'store',
            type        = int,
            default     = 2,
            help        = 'This might be tough to explain to the user'
        )
        parser.add_argument( '--quiet', 
            dest        = 'quiet',
            action      = 'store_true',
            help        = "Silence all output."
        )
        super().__init__(parser)

        if not self.args.quiet:
            ### CHECK
            self.client.user_log_stream_handler.setLevel('DEBUG')
            #self.client.user_log_stream_handler.setLevel('INFO')

        self.excav_sites    = []
        self.bad_stations   = {}
        self.client.user_logger.debug( "Getting star map." )
        self.map            = self.client.get_map()
        self.num_excavs     = 0
        self.client.user_logger.debug( "Getting planet " + self.args.name + "." )
        self.planet         = self.client.get_body_byname( self.args.name )
        self.ring           = Ring(self.planet, 0)
        self.travelling     = {}

        self.client.user_logger.debug( "Getting Arch Min." )
        self.arch   = self.planet.get_buildings_bytype( 'archaeology', 1, 1, 100 )[0]
        self.client.user_logger.debug( "Getting Space Port." )
        self.sp     = self.planet.get_buildings_bytype( 'spaceport', 1, 1, 100 )[0]


    def get_excav_count( self ):
        """ Get number of excavs this planet is able to send right now, and 
        locations of its existing excavs.

        "Able to send right now" means the lower of "how many available excav 
        slots are there in my Arch Min" and "how many excavators do I have built 
        and ready to go".

        Returns nothing, but sets ``self.num_excavs``.

        This does *not* take into account the destinations of excavs that are 
        currently in the air on the way to excavate a planet.
        """
        self.client.cache_off() # we need fresh data for this method

        excav_sites, excav_max, num_travelling = self.arch.view_excavators()
        ### Omit the first excav site; it's our current planet.
        self.excav_sites = excav_sites[1:]

        paging = {}
        filter = {'task': 'Travelling'}
        travelling_ships, travelling_count = self.sp.view_all_ships( paging, filter )
        for s in travelling_ships:
            if s.type == 'excavator':
                self.travelling[ s.to.id ] = 1

        filter = {'type': 'excavator'}
        ships, excavs = self.sp.view_all_ships( paging, filter )
        excavs_built = []
        for i in ships:
            if i.task == 'Docked':
                excavs_built.append(i)
        num_excavs_ready = len(excavs_built)

        ### At this point, num_excavs is the number of excavators we can send 
        ### out, according to the Arch Min's limits.
        self.num_excavs = (excav_max - (len(self.excav_sites) + num_travelling) )

        self.client.user_logger.debug( "Arch min has {} slots available.".format(self.num_excavs) )
        if self.num_excavs <= 0:
            return

        ### If we have fewer excavators ready to go than the Arch Min has 
        ### slots available, we'll shorten self.num_excavs - can't send what 
        ### we don't have.
        self.client.user_logger.debug( "Space port has {} excavators ready.".format(num_excavs_ready) )
        if num_excavs_ready < self.num_excavs:
            self.num_excavs = num_excavs_ready
        self.client.user_logger.info( "We're ready to send out {} more excavators.".format(self.num_excavs) )

    def get_map_square( self ):
        """ Gets a list of stars in the next map square.  

        Map squares start from the innermost ring.  When all squares (cells) in 
        a ring have been returned, we move to the NW cell, one ring out, and 
        then return all cells in that ring, etc.

        Which ring and cell we're on currently is maintained by ``self``, so no 
        arguments need to be passed in.

        Returns a list of lacuna.map.Star objects.

        See the Cell class for details on cells and rings.
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

        self.client.user_logger.debug( "Original planet is ({}, {})"
            .format(self.planet.x, self.planet.y) 
        )
        self.client.user_logger.debug( 
            "Requested cell {} offset {}, row {}, col {}, centerpoint is ({}, {})."
            .format(
                self.ring.this_cell_number, 
                self.ring.ring_offset, 
                req_cell.row, 
                req_cell.col, 
                req_cell.center_x, 
                req_cell.center_y
            )
        )
        self.client.user_logger.debug( "Requested cell top {}, bottom {}, left {}, right {}."
            .format(req_cell.top, req_cell.bottom, req_cell.left, req_cell.right)
        )

        star_list = self.map.get_star_map({
            'top':      req_cell.top,
            'right':    req_cell.right,
            'bottom':   req_cell.bottom,
            'left':     req_cell.left 
        })
        return star_list


    def star_seizure_forbids_excav( self, star, stations:dict, my_alliance = '' ):
        """ Lets you know if the laws affecting a star forbid you from sending 
        excavators to that star's planets.

        **NO WORKY WORKY**
            CHECK
            12/10/2014 - Norway just told me that view_laws() is now working 
            when called from the body on PT.  

            ...and he just realized that, in the case where a station is 
            controlled by another station, it's going to be confusing as to 
            which laws get returned.  He's now going to look at making 
            view_laws() a Star method -- it'll return the laws that currently 
            affect a given star, which should reduce confusion.

            This whole method assumes that you can call ``view_laws()`` on a 
            station your alliance doesn't own.  The docs say you can do that, 
            but you can't.

            So this in no way works.

            If the ``view_laws()`` thing ever gets fixed, this method should 
            be just about ready to go, so I'm leaving it here.

        Arguments:
            - star -- lacuna.map.Star object
            - stations -- Dict.  Keeps track of stations that have already had 
              their laws checked, so any given station only has to have its 
              ``view_laws()`` method called once.  This should start out as an 
              empty dict.
            - my_alliance -- Optional lacuna.alliance.MyAlliance object.  This 
              is only 'optional' in that, if the user is not a member of an 
              alliance, it can be omitted.  But if the user is a member of an 
              alliance, and this doesn't get passed in, any stations owned by 
              the user's alliance that have Members Only Excavation laws in 
              effect will be reported as not being excavate-able.

        Returns True if the star's laws forbids you from excavating its planets, 
        False otherwise.
        """

        ### return False unless star owned by a station
        if not hasattr( star, 'station' ):
            return False
        self.client.user_logger.debug( "{} is owned by an alliance.".format(star.name) )

        ### return False if that's my alliance
        if my_alliance:
            if star.station.id == my_alliance.id:
                self.client.user_logger.debug( "Good - it's my alliance." )
                return False
        self.client.user_logger.debug( "Maybe bad - it's not my alliance." )

        ### if station id is in stations dict, return the value
        if star.station.id in stations:
            self.client.user_logger.debug( "We've already checked out this station." )
            return stations[ star.station.id ]

        ### View laws on station.  Set stations dict and return.
        laws = star.station.view_laws()
        for i in laws:
            if i.name == 'Members Only Excavation':
                stations[ star.station.id ] = True
                self.client.user_logger.debug( "This foreign station forbids MO excavation." )
                return True

        self.client.user_logger.debug( "This foreign station allows MO excavation." )
        stations[ star.station.id ] = False
        return False


    def send_excavs(self):
        """ Sends excavators to the requested planet types in range.

        "requested planet types" and "in range" are both controlled by 
        command-line arguments.

        Returns the number of excavators sent.
        """
        cnt = 0
        while self.num_excavs > 0:
            stars = self.get_map_square()
            cnt += self.send_excavs_to_bodies_orbiting( stars )
        return cnt

    def send_excavs_to_bodies_orbiting(self, stars:list):
        """ Sends excavators to the bodies around each star in a list, provided 
        each body is of one of the requested types.

        Arguments:
            - stars -- list of lacuna.map.Star objects

        Called by ``send_excavs``, so this shouldn't need to be called in a 
        script.

        For each excavator sent, self.num_excavs is decremented.

        Returns the number of excavators sent.
        """
        cnt = 0
        for s in stars:
            if hasattr(s, 'station') and s.station.name in self.bad_stations:
                self.client.user_logger.debug("Station {} has MO Excav law on.  Skipping." .format(s.station.name) )
                continue
            ### This is where we'd call star_seizure_forbids_excav() if 
            ### view_laws() worked.
            cnt += self.send_excavs_to_bodies( s, s.bodies )
            if self.num_excavs <= 0:
                return cnt
        return cnt

    def send_excavs_to_bodies(self, star, bodies:list):
        """ Tries to send an excavator to each body in a list of bodies, 
        provided each body is of one of the requested types.

        Arguments:
            - bodies -- list of body.Body objects

        Called by ``send_excavs``, so this shouldn't need to be called in a 
        script.

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

        Called by ``send_excavs``, so this shouldn't need to be called in a 
        script.

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

        if body.type == 'habitable planet' and body.surface_type in self.args.ptypes:
            self.client.user_logger.debug("Planet {} ({},{}) is habitable, uninhabited, and the correct type." .format(body.name, body.x, body.y) )
        else:
            self.client.user_logger.debug("Planet {} is either not habitable or not the correct type." .format(body.name) )
            return 0

        for e in self.excav_sites:
            if e.body == body.name:
                self.client.user_logger.debug("We already have an excav at {}." .format(body.name) )
                return 0

        target  = { "body_name": body.name }
        excav = self.get_available_excav_for( target )
        if not excav:
            ### CHECK view_laws(), when put in place, should deal with this.
            ### The other reason we could get to here is if we've already got 
            ### an excavator headed to this body from one of our other 
            ### colonies.
            self.client.user_logger.debug("We can't send an excavator.  Probably MO Excav law.  Adding to bad stations dict.")
            if hasattr(star, 'station'):
                self.bad_stations[star.station.name] = 1
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
            ###
            ### CHECK
            ### If we get an exception that tells us we're limited because of 
            ### an MO Excavation law, we should record the station as bad.  I 
            ### expect a ServerError exception in that case, I just don't know 
            ### the code.  I'd guess 1010.
            ### 
            ### I think that, for most exceptions at this point (including the 
            ### case of a MO Excavation law, or the case where we've already 
            ### got an excav on the way), the target planet is bad, so we'd 
            ### just return 0, not mangle self.num_excavs, and get on with it.
            ###
            self.client.user_logger.debug("Encountered {}, ({}) trying to send excav to {} ({}, {})."
                .format(type(e), e, body.name, body.x, body.y)
            )
            return 0
        else:
            ### It probably sent.  If we already had an excav on the way to 
            ### this planet, no exception gets thrown, and it looks like we 
            ### sent one, but we really didn't.
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



class CellOrig():
    """
    CHECK
    After testing out Ring and Cell above, get rid of this.

    Most of this is dealing with zero-based offsets.
    ``ring_offset`` _is_ zero-based; the center 'ring' is offset 0.

    However, ``cell_number`` is NOT zero-based.  The upper-left cell is number 
    1.

    Max requested area allowed by ``lacuna.map.Map.get_star_map()`` is 3001.  
    The closest square to that is 54x54, giving an area of 2916, so length of 
    any dimension of any cell is hardcoded at 54.

    CHECK
        This object probably knows a bit too much about its surroundings.  In 
        a perfect world, there would be a Ring object that knows about cell 
        placement (col and row), where the center cell is, etc.

    Attributes
        ::

            area                length**2, or 2916.
            cell_number         Number of the current cell
            cells_per_row       Number of cells per row (3 for a ring_offset of 1)
            cells_this_ring     Total number of cells in this ring only (8 for a 
                                ring_offset of 1)
            center_cell_number  the cell_number of the center cell (1 for a 
                                ring_offset of 0, 5 for a ring_offset of 1, etc)
            center_col          The column occupied by the center cell.  0-based. 
            center_row          The row occupied by the center cell.  0-based. 
            col                 The column occupied by the current cell.  0-based.
            length              54
            planet              lacuna.body.MyBody object everything is relative to.
            ring_offset         Integer offset from the center (center is 0)
            row                 The row occupied by the current cell.  0-based.
            total_cells         Total number of cells in the square, including all 
                                rings (9 for a ring_offset of 1)

    **Rings and Cells**
        The diagram below shows ring offsets 0 and 1.

        The center cell contains the target planet in its center.  In the 
        example diagram, that center cell's count is either 1 (at 
        ``ring_offset`` 0) or 5 (at ``ring_offset``  1).  The other cells are 
        numbered assuming ``ring_offset``  1.

        Each increase in ``ring_offset``  will add another layer of cells 
        around the previous layer, just as ``ring_offset``  1 adds a full 
        layer of cells wrapped around the single cell at ``ring_offset``  0::

               <---- 54 ----> <---- 54 ----> <---- 54 ---->
            ^^ +------------+ +------------+ +------------+
            || |  offset 1  | |  offset 1  | |  offset 1  |
               |            | |            | |            |
            54 |            | |            | |            |
               |            | |            | |            |
            || |  count 1   | |  count 2   | |  count 3   |
            VV +------------+ +------------+ +------------+

            ^^ +------------+ +------------+ +------------+
            || |  offset 1  | | offset 0/1 | |  offset 1  |
               |            | |            | |            |
            54 |            | |     o      | |            |
               |            | |            | |            |
            || |  count 4   | | count 1/5  | |  count 6   |
            VV +------------+ +------------+ +------------+

            ^^ +------------+ +------------+ +------------+
            || |  offset 1  | |  offset 1  | |  offset 1  |
               |            | |            | |            |
            54 |            | |            | |            |
               |            | |            | |            |
            || |  count 7   | |  count 8   | |  count 9   |
            VV +------------+ +------------+ +------------+

    """

    def __init__( self, planet, ring_offset:int = 0, cell_number:int = 1 ):
        self.planet             = planet                            # The center planet everything is relative to.
        self.ring_offset        = ring_offset
        self.cell_number        = cell_number
        self.length             = 54                                # length of the sides of the cells
        self.area               = length**2
        self.cells_this_ring    = int( 8 * self.ring_offset )
        self.cells_per_row      = int( (2 * self.ring_offset + 1) )
        self.total_cells        = int( cells_per_row**2 )
        self.center_cell_number = int( (total_cells + 1) / 2 )      # number of the center cell (upper-left is 1)

        self.row, self.col                  = self._get_row_and_col( self.cell_number )
        self.center_row, self.center_col    = self._get_row_and_col( self.center_cell_number )
        self._set_center_point()
        self._set_bounding_points()

    def _get_row_and_col(self, number):
        row = 0
        col = number - 1 # cell numbers start at 1
        while( col > self.cells_per_row ):
            row += 1
            col -= self.cells_per_row

    def _set_center_point(self):
        self.center_x = 0
        self.center_y = 0
        if self.row < self.center_row:
            self.center_y = (self.planet.y - self.length) * (self.center_row - self.row)
        elif self.row > self.center_row:
            self.center_y = (self.planet.y + self.length) * (self.row - self.center_row)
        if req_col < self.center_col:
            self.center_x = (self.planet.x - self.length) * (self.center_col - req_col)
        elif req_col > self.center_col:
            self.center_x = (self.planet.x + self.length) * (req_col - self.center_col)

    def _set_bounding_points(self):
        self.left    = self.center_x - (self.length / 2)
        self.right   = self.center_x + (self.length / 2)
        self.top     = self.center_y + (self.length / 2)
        self.bottom  = self.center_y - (self.length / 2)

        if self.top < -1500 or self.bottom > 1500 or self.left > 1500 or self.right < -1500:
            ### CHECK this needs to do something more reasonable than bailing.
            self.client.user_logger.debug( "This cell is entirely out of bounds." )
            quit()

        ### At least part of the cell is in bounds.  But parts of it might lap 
        ### over the boundaries, and get_star_map doesn't accept any 
        ### out-of-bounds coords.
        self.top     =  1500 if self.top     > 1500 else self.top
        self.right   =  1500 if self.right  >  1500 else self.right
        self.bottom  = -1500 if self.bottom < -1500 else self.bottom
        self.left    = -1500 if self.left   < -1500 else self.left

