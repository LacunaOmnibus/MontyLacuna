
import os, re, sys, time, unittest

rootdir = os.path.join( os.path.abspath(os.path.dirname(__file__)), "..", "..", ".." )
libdir  = os.path.join( rootdir, "lib" )
sys.path.append(libdir)

import lacuna, lacuna.exceptions as err, lacuna.binutils.libsend_excavs as lib
import lacuna.test.connector as conn

class TestBodyCache(unittest.TestCase):
    """ Test the :class:`lacuna.binutils.libsend_excavs.BodyCache` class.
    """
    def test_bad(self):
        bc = lib.BodyCache()
        bc.mark_as_bad( "bad_star", "star" )
        bc.mark_as_bad( "bad_station", "station" )
        bc.mark_as_bad( "bad_planet_1", "planet" )
        bc.mark_as_bad( "bad_planet_2" )
        ### When not specifying a type, we default to 'planet'?
        self.assertTrue( bc.planets["bad_planet_2"] )
        ### Everything got marked bad?
        self.assertTrue( bc.is_bad("bad_star") )
        self.assertTrue( bc.is_bad("bad_station") )
        self.assertTrue( bc.is_bad("bad_planet_1") )
        self.assertTrue( bc.is_bad("bad_planet_2") )

class TestPoint(unittest.TestCase):
    """ Test the :class:`lacuna.binutils.libsend_excavs.Point` class.
    """
    def test(self):
        p = lib.Point( 10, 20 )
        self.assertEqual( p.x, 10 )
        self.assertEqual( p.y, 20 )

class TestCell(unittest.TestCase):
    """ Test the :class:`lacuna.binutils.libsend_excavs.Cell` class.
    """
    def test(self):
        p = lib.Point( 0, 0 )
        c = lib.Cell( p, 54 )
        self.assertEqual( c.right, 27 )
        self.assertEqual( c.left, -27 )
        self.assertEqual( c.top, 27 )
        self.assertEqual( c.bottom, -27 )
        self.assertEqual( c.center_point.x, 0 )
        self.assertEqual( c.center_point.y, 0 )
        self.assertEqual( c.cell_size, 54 )

        p = lib.Point( -100, -100 )
        c = lib.Cell( p, 54 )
        self.assertEqual( c.right, -73 )
        self.assertEqual( c.left, -127 )
        self.assertEqual( c.top, -73 )
        self.assertEqual( c.bottom, -127 )
        self.assertEqual( c.center_point.x, -100 )
        self.assertEqual( c.center_point.y, -100 )
        self.assertEqual( c.cell_size, 54 )

#@unittest.skip("skipping Send Excavs")
class TestSendExcavs(unittest.TestCase, conn.Connector):
    """ Test the :class:`lacuna.binutils.libsend_excavs.SendExcavs` class.

    Requirements:

    - test_sitter config section must contain the following

      - test_planet: <name of a planet with an archmin>.  'all' is also acceptable, provided all of your planets have arch mins on them.
      - send_excavs_ptypes: A single planet type, eg "p35"
      - send_excavs_max_ring: How far out to extend from the center cell, eg "1"
      - send_excavs_max_send: How many excavs to send, eg "1"

    - The empire you're connecting as must be a member of an alliance

      - A single member alliance that just contains your own empire is fine.

    """
    @classmethod
    def setUpClass(self):
        self.tle_connect(self)

        args = {
            'client': self.sitter,
            'name': self.sitter.test_planet,
            'ptypes': self.sitter.send_excavs_ptypes,
            'max_ring': self.sitter.send_excavs_max_ring,
            'max_send': self.sitter.send_excavs_max_send,
            'fresh': True,
        }
        self.se = lib.SendExcavs( testargs = args )

    #@unittest.skip("skipping")
    def test_planets(self):
        planets = 0
        for p in self.se.planets:
            self.se.set_planet( p )
            self.assertEqual( type(self.se.planet), lacuna.body.MyBody )
            planets += 1
        self.assertTrue( planets > 0 )

    #@unittest.skip("skipping")
    def test_planet(self):
        self.se.set_planet( self.se.planets[0] )
        self.assertEqual( type(self.se.ring), lib.Ring )
        self.assertEqual( type(self.se.body_cache), lib.BodyCache )
        self.assertEqual( type(self.se.excav_sites), list )
        self.assertEqual( self.se.num_excavs, 0 )
        self.assertEqual( type(self.se.travelling), dict )

    #@unittest.skip("skipping")
    def test_ring(self):
        self.se.set_planet( self.se.planets[0] )
        self.assertEqual( self.se.ring.cell_size, 54 )
        self.assertEqual( self.se.ring.ring_offset, 0 )
        self.assertEqual( self.se.ring.cells_per_row, 1 )
        self.assertEqual( self.se.ring.cells_this_ring, 1 )
        self.assertEqual( self.se.ring.center_cell_number, 1 )
        self.assertEqual( self.se.ring.center_col, 0 )
        self.assertEqual( self.se.ring.center_row, 0 )
        self.assertEqual( self.se.ring.planet, self.se.planet )
        self.assertEqual( self.se.ring.total_cells, 1 )

        square = self.se.get_map_square()   # advance us out to the next ring
        ### No need to test cell_size again.  It's hard-coded.
        self.assertEqual( self.se.ring.ring_offset, 1 )
        self.assertEqual( self.se.ring.cells_per_row, 3 )
        self.assertEqual( self.se.ring.cells_this_ring, 8 )
        self.assertEqual( self.se.ring.center_cell_number, 5 )
        self.assertEqual( self.se.ring.center_col, 1 )
        self.assertEqual( self.se.ring.center_row, 1 )
        self.assertEqual( self.se.ring.planet, self.se.planet )
        self.assertEqual( self.se.ring.total_cells, 9 )

    #@unittest.skip("skipping")
    def test_alliance(self):
        self.assertEqual( type(self.se.ally), lacuna.alliance.MyAlliance )

    #@unittest.skip("skipping")
    def test_alliance_members(self):
        self.assertEqual( type(self.se.ally_members), list )
        gotme = False
        for m in self.se.ally_members:
            if m == self.sitter.empire.name:
                gotme = True
        self.assertTrue( gotme )

    #@unittest.skip("skipping")
    def test_ready_excavs(self):
        self.se.set_planet( self.se.planets[0] )
        self.assertEqual( type(self.se.get_ready_excavators()), int )

    #@unittest.skip("skipping")
    def test_get_map_square(self):
        self.se.set_planet( self.se.planets[0] )
        square = self.se.get_map_square()
        self.assertEqual( type(square), list )
        for s in square:
            self.assertEqual( type(s), lacuna.map.Star )



    """
    FAKE TESTS
    These tests would require more setup than is reasonable to expect, since 
    we're not in control of the server.
    We can check that these methods are callable and return the correct types, 
    but can't really check that they're doing what they're supposed to be.
    """
    #@unittest.skip("skipping")
    def test_note_travelling_excavators(self):
        self.se.set_planet( self.se.planets[0] )
        self.assertEqual( self.se.note_travelling_excavators(), None )

    #@unittest.skip("skipping")
    def test_star_seizure_forbids_excav(self):
        self.se.set_planet( self.se.planets[0] )
        star = self.sitter.get_map().get_star( self.se.planet.star_id )
        self.assertEqual( type(self.se.star_seizure_forbids_excav(star)), bool )

    #@unittest.skip("skipping")
    def test_send_excavs_to_bodies_orbiting(self):
        self.se.set_planet( self.se.planets[0] )
        stars = self.se.get_map_square()[0:1]
        cnt = self.se.send_excavs_to_bodies_orbiting( stars )
        self.assertEqual( type(cnt), int )

    #@unittest.skip("skipping")
    def test_system_contains_hostiles(self):
        self.se.set_planet( self.se.planets[0] )
        star = self.sitter.get_map().get_star( self.se.planet.star_id )
        self.assertEqual( type(self.se.system_contains_hostiles(star)), bool )

    #@unittest.skip("skipping")
    def test_send_excavs_to_bodies(self):
        self.se.set_planet( self.se.planets[0] )
        star = self.sitter.get_map().get_star( self.se.planet.star_id )
        self.assertEqual( type(self.se.send_excavs_to_bodies(star, [self.se.planet])), int )

    #@unittest.skip("skipping")
    def test_get_available_excav_for(self):
        self.se.set_planet( self.se.planets[0] )
        rslt = self.se.get_available_excav_for({ 'body_id': self.se.planet.id })
        if rslt:
            self.assertEqual( type(rslt), lacuna.ship.ExistingShip )
        else:
            self.assertEqual( type(rslt), bool )

    #@unittest.skip("skipping")
    def test_send_excav_to_matching_body(self):
        self.se.set_planet( self.se.planets[0] )
        star = self.sitter.get_map().get_star( self.se.planet.star_id )
        self.assertEqual( type(self.se.send_excav_to_matching_body(star, self.se.planet)), int )

if __name__ == '__main__':
    unittest.main()

