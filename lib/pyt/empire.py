
import os, re, sys, unittest

rootdir = os.path.join( os.path.abspath(os.path.dirname(sys.argv[0])), ".." )
libdir  = os.path.join( rootdir, "lib" )
etcdir  = os.path.join( rootdir, "etc" )
sys.path.append(libdir)

import lacuna, lacuna.exceptions as err

class MyEmpire(unittest.TestCase):
    """ Test the lacuna.empire.MyEmpire class.
    """

    def __init__( self, test_method_name:str ):
        super().__init__(test_method_name)
        self.config_file = 'lacuna.cfg'
        self.sitter = lacuna.clients.Member(
            config_file     = os.path.join( etcdir, self.config_file ),
            config_section  = 'sitter'
        )
        self.real = lacuna.clients.Member(
            config_file     = os.path.join( etcdir, self.config_file ),
            config_section  = 'real'
        )

        ### We're going to be raising exceptions in here on purpose, and don't 
        ### want the logger to output any of those to the screen.
        self.sitter.request_log_stream_handler.setLevel('CRITICAL')
        self.real.request_log_stream_handler.setLevel('CRITICAL')

    def setUp(self):
        """ __init__() runs just once, while setUp() runs before each test (and 
        tearDown() runs after each test).  I don't need to re log in before each 
        test.
        """
        pass

    def test_id_numeric(self):
        self.assertTrue( re.match("^\d+$", self.sitter.empire.id) )

    def test_home_planet_id_numeric(self):
        self.assertTrue( re.match("^\d+$", self.sitter.empire.home_planet_id) )

    def test_rpc(self):
        start_rpc = self.sitter.empire.rpc_count
        self.sitter.empire.find("foo")
        end_rpc = self.sitter.empire.rpc_count
        ### assertEqual( start_rpc + 1, end_rpc) -- this isn't always going to 
        ### be true, as end_rpc may be more than one greater, depending on 
        ### what else is happening.  Asserting that end_rpc is greater than 
        ### start_rpc is really what we're going for anyway.
        self.assertTrue( start_rpc < end_rpc )

    def test_body_counts(self):
        station_ids = self.sitter.empire.stations.keys()
        colonie_ids = self.sitter.empire.colonies.keys()
        planet_ids  = self.sitter.empire.planets.keys()
        self.assertEqual( len(planet_ids), (len(station_ids) + len(colonie_ids)) )

    def test_find_empire(self):
        emps = self.sitter.empire.find( self.sitter.empire.name )
        found = False 
        for e in emps:
            if e.name == self.sitter.empire.name:
                found = True
        self.assertTrue( found )

    def test_get_invite_friend_url(self):
        url = self.sitter.empire.get_invite_friend_url()['referral_url']
        self.assertTrue( re.match("https?://(us1|pt)\.lacunaexpanse\.com/#referral=[\w-]{36}", url) )

    def test_get_species_templates(self):
        tmpls = self.sitter.empire.get_species_templates()
        ok = True
        for t in tmpls:
            ### No need to check each key in each template dict - it there's a 
            ### 'name' key we'll assume it's a full template.
            if not hasattr(t, 'name'):
                ok = False
        self.assertTrue( ok )

    def test_redefine_species_limits(self):
        limits = self.sitter.empire.redefine_species_limits()
        ok = True
        if not 'can' in limits: # See test_get_species_templates() comment
            ok = False
        self.assertTrue( ok )

    def test_view_boosts(self):
        boosts = self.sitter.empire.view_boosts()
        ok = True
        if not hasattr(boosts, 'food'): # See test_get_species_templates() comment
            ok = False
        self.assertTrue( ok )

    def test_view_profile_with_sitter(self):
        with self.assertRaises( err.ServerError ):
            profile = self.sitter.empire.view_profile()

    def test_view_profile_with_real(self):
        profile = self.real.empire.view_profile()   # real, not sitter.
        ok = True
        if not hasattr(profile, 'description'):     # See test_get_species_templates() comment
            ok = False
        self.assertTrue( ok )

    def test_view_species_stats(self):
        stats = self.sitter.empire.view_species_stats()
        ok = True
        if not hasattr(stats, 'name'): # See test_get_species_templates() comment
            ok = False
        self.assertTrue( ok )

if __name__ == '__main__':
    unittest.main()

