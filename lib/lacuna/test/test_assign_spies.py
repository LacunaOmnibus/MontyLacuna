
import os, re, sys, time, unittest

rootdir = os.path.join( os.path.abspath(os.path.dirname(__file__)), "..", "..", ".." )
libdir  = os.path.join( rootdir, "lib" )
sys.path.append(libdir)

import lacuna, lacuna.exceptions as err, lacuna.binutils.libassign_spies as lib
import lacuna.test.connector as conn

#@unittest.skip("skipping")
class TestAssignSpies(unittest.TestCase, conn.Connector):
    """ Test the lacuna.binutils.libassign_spies.AssignSpies class.

    Requirements
        - test_sitter config section must contain the following
          - test_planet: <name of a planet>
          - This planet must have at least one Idle spy who will be assigned to 
            run counter espionage.

    Running this test is going to produce a captcha that must be solved, so it's 
    not something you can run unattended.
    """
    @classmethod
    def setUpClass(self):
        self.tle_connect(self)

        args = {
            'client': self.sitter,
            'name': self.sitter.test_planet,
            'task':  'counter',
            'num':  1,
            'doing':  'Idle',
            'topoff':  False,
            'on':  None,
            'top':  'level',
            'fresh': True,
        }
        self.lib = lib.AssignSpies( testargs = args )

    #@unittest.skip("skipping")
    def test_planet(self):
        self.lib.set_planet( self.lib.planets[0] )
        self.assertEqual( type(self.lib.intmin), lacuna.buildings.callable.intelligence.intelligence )
        self.assertEqual( type(self.lib.all_spies), list )
        self.assertEqual( type(self.lib.spies), list )
        self.assertEqual( type(self.lib.max), int )

    #@unittest.skip("skipping")
    def test_all_spies(self):
        self.lib.set_planet( self.lib.planets[0] )
        for s in self.lib.all_spies:
            self.assertEqual( type(s), lacuna.spy.Spy )

    #@unittest.skip("skipping")
    def test_check_topoff(self):
        self.lib.set_planet( self.lib.planets[0] )
        self.lib.args.topoff = True
        origmax = self.lib.max
        try:
            self.lib.check_topoff()
        except err.TopoffError:
            self.assertTrue( True )
            return
        self.assertTrue( origmax >= self.lib.max )
        self.lib.args.topoff = False

    #@unittest.skip("skipping")
    def test_set_spies_on_target(self):
        self.lib.set_planet( self.lib.planets[0] )
        try:
            self.lib.set_spies_on_target()
        except err.NoUsableSpiesError:
            self.assertTrue( True )
            return
        self.assertTrue( len(self.lib.all_spies) >= len(self.lib.spies) )

    #@unittest.skip("skipping")
    def test_set_able_spies(self):
        self.lib.set_planet( self.lib.planets[0] )
        try:
            self.lib.set_able_spies()
        except err.NoUsableSpiesError:
            self.assertTrue( True )
            return
        self.assertTrue( len(self.lib.all_spies) >= len(self.lib.spies) )

    #@unittest.skip("skipping")
    def test_set_spies_doing_correct_task(self):
        self.lib.set_planet( self.lib.planets[0] )
        try:
            self.lib.set_spies_doing_correct_task()
        except err.NoUsableSpiesError:
            self.assertTrue( True )
            return
        self.assertTrue( len(self.lib.all_spies) >= len(self.lib.spies) )

    #@unittest.skip("skipping")
    def test_best_spies(self):
        self.lib.set_planet( self.lib.planets[0] )
        old_list = self.lib.spies
        self.lib.set_best_spies()
        self.assertTrue( len(self.lib.spies) <= len(old_list) )

    #@unittest.skip("skipping")
    def test_assign_spies(self):
        self.lib.set_planet( self.lib.planets[0] )
        self.lib.set_spies_on_target()
        self.lib.set_able_spies()
        self.lib.set_spies_doing_correct_task()
        self.lib.max = 1    # Make sure we're only assigning one spy
        num = self.lib.assign_spies()
        self.assertEqual( type(num), int )

if __name__ == '__main__':
    unittest.main()

