
import binutils.libbin
import argparse, lacuna, os, sys

"""
python bin/send_excavs.py --t p23 --t p24 --t p25 --max_ring 3 Earth
    This doesn't build excavs; you have to manage that manually or with another script.
"""

class SendExcavs(binutils.libbin.Script):
    """
    Attributes::

        arch            The Archaeology Ministry on self.planet.
        args            Command-line arguments; the result of
                        self.parser.parse_args()
        cell_number     The cell we're working on.  Starts at 1.
        client          lacuna.clients.Member object
        excav_sites     A list of sites currently being excavated.  Starts
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

        self.ring_offset    = 1
        self.cell_number    = 1
        self.num_excavs     = 0
        self.excav_sites    = []
        self.map            = self.client.get_map()
        self.planet         = self.client.get_body_byname( self.args.name )

        self.arch   = self.planet.get_buildings_bytype( 'archaeology', efficiency = 100 )[0]
        self.sp     = self.planet.get_buildings_bytype( 'space port', efficiency = 100 )[0]

        if not self.args.quiet:
            ### CHECK
            self.client.user_log_stream_handler.setLevel('DEBUG')
            #self.client.user_log_stream_handler.setLevel('INFO')

    def get_excav_count( self ):
        """ Get number of excavs this planet is able to send right now, and 
        locations of its existing excavs.

        Arguments:
            - planet -- lacuna.body.MyBody object

        This does _not_ take into account the destinations of excavs that are 
        currently in the air on the way to excavate a planet.
        """
        self.out, max, trav = self.arch.view_excavators()
        self.num_excavs = (max - (len(out) + trav) )
        self.client.user_logger.debug( "Arch min has {} slots available.".format(self.num_excavs) )
        if self.num_excavs <= 0:
            return

        paging = {}
        filter = {'type': 'excavator'}
        self.excav_sites, count = self.sp.view_all_ships( paging, filter )

        self.client.user_logger.debug( "Space port has {} excavators ready.".format(count) )
        if count < self.num_excavs:
            self.num_excavs = count
        self.client.user_logger.debug( "So we're ready to send out {} more excavators.".format(self.num_excavs) )

        return

    def get_map_square( self ):
        """ Gets a list of stars in the next map square.  """

        center_cell = Cell( self.planet, 0, 1 )
        req_cell    = Cell( self.planet, self.ring_offset, self.cell_number )

        self.client.user_logger.debug( "Original planet (cell {}) is ({}, {})"
            .format(center_cell.cell_number, self.planet.x, self.planet.y) 
        )
        self.client.user_logger.debug( "Requested cell {} (offset {}) (row {}, col {}) centerpoint is ({}, {})"
            .format(req_cell.cell_number, req_cell.ring_offset, req_cell.row, req_cell.col, req_cell.center_x, req_cell.center_y)
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

        ### Advance to the next cell.  If at max cell, advance to the next 
        ### ring.  If at max ring, there are no more excavs to send.
        self.cell_number += 1
        if self.cell_number > cells_this_ring:
            self.cell_number = 1
            self.ring_offset += 1
            if self.ring_offset > self.args.max_ring:
                self.num_excavs = 0

        return star_list


    def star_seizure_forbids_excav( self, star, stations:dict, my_alliance = '' ):
        """ Lets you know if the laws affecting a star forbid you from sending 
        excavators to that star's planets.

        **NO WORKY WORKY**
        This whole method assumes that you can call view_laws() on a station 
        your alliance doesn't own.  The docs say you can do that, but you can't.

        So this in no way works.

        If the view_laws() thing ever gets fixed, this method should be just 
        about ready to go, so I'm leaving it in.
        **NO WORKY WORKY**

        Arguments:
            - star -- lacuna.map.Star object
            - stations -- Dict.  Keeps track of stations that have already had 
              their laws checked, so any given station only has to have its 
              view_laws() method called once.  This should start out as an empty 
              dict.
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


    def send_excavs(self, num:int, excavs:list):
        while self.num_excavs > 0:
            stars = self.get_map_square()
            self.send_excavs_to_bodies_orbiting( stars )

    def send_excavs_to_bodies_orbiting(self, stars:list):
        """ Sends excavators to the valid bodies around a list of stars.

        For each excavator sent, self.num_excavs is decremented.

        Returns the number of excavators sent.
        """
        cnt = 0
        for s in stars:
            ### This is where we'd call star_seizure_forbids_excav() if 
            ### view_laws() worked.
            cnt += self.send_excavs_to_bodies( s.bodies )
        return cnt

    def send_excavs_to_bodies(self, bodies:list):
        """ Tries to send an excavator to each body in a list of bodies.

        Returns the integer count of excavators sent.
        """
        cnt = 0
        for b in s.bodies:
            cnt += self.send_excav_to_body(b)
            if self.num_excavs <= 0:
                return cnt
        return cnt

    def send_excav_to_body(self, body):
        """ Tries to send an excavator to a body.

        For each excavator sent, self.num_excavs is decremented.

        Returns 1 if sent, 0 if not.
        """
        if body.type == 'habitable planet' and body.surface_type in self.args.ptypes:
            self.client.user_logger.debug("Planet {} is habitable and the correct type." .format(body.name) )
        for e in self.excav_sites:
            if e.body == body.name:
                self.client.user_logger.debug("We already have an excav at {}." .format(body.name) )
                return 0
        try:
            target  = { "body_name": body.name, "quantity": 1 }
            types   = [{ "type": "excavator" }]
            self.sp.send_my_ship_types( target, types )
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
            self.client.user_logger.debug("Encountered {} trying to send excav to {}."
                .format(type(e), body.name)
            )
            return 0
        else:
            ### Yay it sent.
            self.num_excavs -= 1
            return 1

class Cell():
    """
    Most of this is dealing with zero-based offsets.
    'ring_offset' _is_ zero-based; the center 'ring' is offset 0.

    However, 'cell_number' is NOT zero-based.  The upper-left cell is number 1.

    Max requested area allowed by get_star_map() is 3001.  The closest square 
    I can get to that is 54x54, giving an area of 2916, so length of a cell 
    (that's the length of any dimension) is hardcoded at 54.

    Attributes:
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

    Rings and Cells
    ---------------
    The diagram below shows ring offsets 0 and 1.

    The center cell contains the target planet in its center.  That center 
    cell's count is either 1 (at ring_offset 0) or 5 (at ring_offset 1).  The 
    other cells are numbered assuming ring_offset 1.

    Each increase in ring_offset will add another layer of cells around the 
    previous layer, just as ring_offset 1 adds a full layer of cells wrapped 
    around the single cell at ring_offset 0.


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

