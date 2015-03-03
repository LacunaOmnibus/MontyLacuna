
import os, re, sys, time, unittest

### __file__, not sys.argv[0].  When run using nose, sys.argv[0] will be nose 
### itself, not this module.
rootdir = os.path.join( os.path.abspath(os.path.dirname(__file__)), "..", "..", ".." )
libdir  = os.path.join( rootdir, "lib" )
sys.path.append(libdir)

import lacuna, lacuna.exceptions as err, lacuna.binutils.libexcavs_report as lib
import lacuna.test.connector as conn

#@unittest.skip("skipping Excavs Report")
class TestExcavsReport(unittest.TestCase, conn.Connector):
    """ Test the lacuna.binutils.libexcavs_report.ExcavsReport class.

    Requirements:
        test_sitter must contain
            planet: <name of a planet with an archmin>.  'all' is also 
            acceptable, provided all of your planets have arch mins on them.

    """
    @classmethod
    def setUpClass(self):
        self.tle_connect(self)

        args = {
            'client': self.sitter,
            'name': self.sitter.planet,
            'fresh': True,
        }
        self.er = lib.ExcavsReport( testargs = args )

    #@unittest.skip("skipping")
    def test_planets(self):
        planets = 0
        for p in self.er.planets:
            self.er.set_planet( p )
            self.assertEqual( type(self.er.planet), lacuna.body.MyBody )
            planets += 1
        self.assertTrue( planets > 0 )

    #@unittest.skip("skipping")
    def test_archmin(self):
        for p in self.er.planets:
            self.er.set_planet( p )
            self.assertEqual( type(self.er.archmin), lacuna.buildings.callable.archaeology.archaeology )

    #@unittest.skip("skipping")
    def test_excavator_data(self):
        for p in self.er.planets:
            self.er.set_planet( p )
            self.er.gather_excavator_data()
            for pname, bodies in self.er.excavator_data.items():
                for b in bodies:
                    self.assertTrue( type(b.distance) is float )
                    self.assertEqual( type(b), lacuna.body.Body )

if __name__ == '__main__':
    unittest.main()

