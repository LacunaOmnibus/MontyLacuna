
import binutils.libbin
import argparse, lacuna, os, sys


"""

python bin/send_excavs.py --t p23 --t p24 --t p25 --max_ring 3 Earth
    This doesn't build excavs; you have to manage that manually or with another script.


Rings
I'm using rings of squares, rather than an increasing circle using SQL, because 
I can select all of the stars in a square with a single TLE request.

    +------------+ +------------+ +------------+
    |  offset 1  | |  offset 1  | |  offset 1  |
    |            | |            | |            |
    |            | |            | |            |
    |            | |            | |            |
    |  count 1   | |  count 2   | |  count 3   |
    +------------+ +------------+ +------------+

    +------------+ +------------+ +------------+
    |  offset 1  | |  offset 0  | |  offset 1  |
    |            | |            | |            |
    |            | |      o     | |            |
    |            | |            | |            |
    |  count 4   | |  count 1   | |  count 5   |
    +------------+ +------------+ +------------+

    +------------+ +------------+ +------------+
    |  offset 1  | |  offset 1  | |  offset 1  |
    |            | |            | |            |
    |            | |            | |            |
    |            | |            | |            |
    |  count 6   | |  count 7   | |  count 8   |
    +------------+ +------------+ +------------+


- ring_offset 0 contains my planet at the center
- ring_offset 1 starts at the NW corner of ring_offset 0, ring_offset 2 starts 
  in the NW corner of ring_offset 1, etc.
- Each ring_offset has (8 * ring_offset) cells

8 in offset 1
    8 squares in this ring (8 * offset)
    3 squares per row (offset + offset + 1)
                . . .
                4 5 .
                . . .

in offset 2
    16 squares in this ring (8 * offset)
    5 squares per row (offset + offset + 1)
              . . . . 5
              . 7 . .10
              . .13 .15
              . . . .20
              . . . .25

offset 3
    24 squares in this ring (8 * offset)
    7 squares per row (offset + offset + 1)
            . . . . . . 7
            . . . . . .14
            . . . . . .21
            . . .25 . .28
            . . . . . .35
            . . . . . .42
            . . . . . .49

"""



class SendExcavs(binutils.libbin.Script):

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
            dest        = 'ptype',
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

    def get_excav_count( self, planet ):
        available_num = 0

        planet.client.user_logger.debug("Getting arch min")
        arch = planet.get_buildings_bytype( 'archaeology', efficiency = 100 )[0]
        out, max, trav = arch.view_excavators()
        available_num = (max - (len(out) + trav) )
        planet.client.user_logger.debug( "Arch min has {} slots available.".format(available_num) )
        if available_num <= 0:
            return available_num

        planet.client.user_logger.debug("Getting space port")
        sp = planet.get_buildings_bytype( 'spaceport', efficiency = 100, limit = 1 )[0]
        paging = {}
        filter = {'type': 'excavator'}
        excavs, count = sp.view_all_ships( paging, filter )

        planet.client.user_logger.debug( "Space port has {} excavators ready.".format(count) )
        if count < available_num:
            available_num = count

        planet.client.user_logger.debug( "So we're ready to send out {} more excavators.".format(available_num) )
        return available_num

    def get_map_square( self, map, planet, offset:int, cell:int ):
        """
            Most of this is dealing with zero-based offsets.
            'offset' _is_ zero-based; the center square is 0.
            'cell' is NOT zero-based.  Upper-left cell number is number 1.

            Max requested area is 3001.  
            The closest square I can get to that is 54x54 (54 / 2 is 27)
            54*54 is 2916, half of which is 1458
        """

        length          = 54                                # length of any side of the cells
        area            = length**2
        cells_this_ring = int( 8 * offset )
        cells_per_row   = int( (2 * offset + 1) )
        total_cells     = int( cells_per_row**2 )
        center_cell     = int( (total_cells + 1) / 2 )      # number of the center cell, if upper-left is 1

        ### Get row and column of the requested cell
        req_row = 0
        req_col = cell - 1                  # since cell counts start at 1
        while( req_col > cells_per_row ):
            req_row += 1
            req_col -= cells_per_row

        ### Get row and column of the center cell
        center_row = 0
        center_col = center_cell - 1        # since cell counts start at 1
        while( center_col > cells_per_row ):
            center_row += 1
            center_col -= cells_per_row

        ### Get centerpoint of requested cell
        req_center_x = 0
        req_center_y = 0
        if req_row < center_row:
            req_center_y = (planet.y - length) * (center_row - req_row)
        elif req_row > center_row:
            req_center_y = (planet.y + length) * (req_row - center_row)
        if req_col < center_col:
            req_center_x = (planet.x - length) * (center_col - req_col)
        elif req_col > center_col:
            req_center_x = (planet.x + length) * (req_col - center_col)

        planet.client.user_logger.debug( "Original planet (cell {}) is ({}, {})".format(center_cell, planet.x, planet.y) )
        planet.client.user_logger.debug( "Requested cell {} (row {}, col {}) centerpoint is ({}, {})"
            .format(cell, req_row, req_col, req_center_x, req_center_y)
        )

        ### Derive bounding points of requested cell
        left    = req_center_x - (length / 2)
        right   = req_center_x + (length / 2)
        top     = req_center_y + (length / 2)
        bottom  = req_center_y - (length / 2)

        planet.client.user_logger.debug( "Cell {} in ring {} from ({}, {}).  Top {}, bottom {}, left {}, right {}."
            .format(cell, offset, planet.x, planet.y, top, bottom, left, right)
        )

        if top < -1500 or bottom > 1500 or left > 1500 or right < -1500:
            ### CHECK this needs to do something more reasonable than bailing.
            planet.client.user_logger.debug( "This cell is entirely out of bounds." )
            quit()

        ### At least part of the cell is in bounds.  But parts of it might lap 
        ### over the boundaries, and get_star_map doesn't accept any 
        ### out-of-bounds coords.
        top     =  1500 if top     > 1500 else top
        right   =  1500 if right  >  1500 else right
        bottom  = -1500 if bottom < -1500 else bottom
        left    = -1500 if left   < -1500 else left

        star_list = map.get_star_map({ 'top': top, 'right':right, 'bottom':bottom, 'left': left })
        return star_list

