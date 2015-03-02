
import os, re, sys, time, unittest

### __file__, not sys.argv[0].  When run using nose, sys.argv[0] will be nose 
### itself, not this module.
rootdir = os.path.join( os.path.abspath(os.path.dirname(__file__)), "..", "..", ".." )
libdir  = os.path.join( rootdir, "lib" )
etcdir  = os.path.join( rootdir, "etc" )
sys.path.append(libdir)

import lacuna, lacuna.test.connector as conn, lacuna.exceptions as err

@unittest.skip("skipping generic subclass")
class GenericSubclass(unittest.TestCase, conn.Connector):
    """ Should be used to test out all of the various classes that just inherit 
    from bc.  These don't have any of their own methods.
    """
    @classmethod
    def setUpClass(self):
        self.tle_connect(self)

    def test_boost(self):
        expected_attribs = ( 'food', 'ore', 'energy', 'water',
            'happiness', 'storage', 'building', 'spy_training' )
        mydict = { x: "foo" for x in expected_attribs }
        b = lacuna.empire.Boosts( self.sitter, mydict )
        for i in expected_attribs:
            self.assertTrue( hasattr(b, i) )

    def test_found_empire(self):
        expected_attribs = ( 'id', 'name' )
        mydict = { x: "foo" for x in expected_attribs }
        b = lacuna.empire.FoundEmpire( self.sitter, mydict )
        for i in expected_attribs:
            self.assertTrue( hasattr(b, i) )

    def test_owning_empire(self):
        expected_attribs = ( 'id', 'name', 'alignment', 'is_isolationist' )
        mydict = { x: "foo" for x in expected_attribs }
        b = lacuna.empire.OwningEmpire( self.sitter, mydict )
        for i in expected_attribs:
            self.assertTrue( hasattr(b, i) )

    def test_species(self):
        expected_attribs = (
            'name', 'description', 'min_orbit', 'max_orbit', 'manufacturing_affinity',
            'deception_affinity', 'research_affinity', 'management_affinity', 'farming_affinity',
            'mining_affinity', 'science_affinity', 'environmental_affinity', 'political_affinity',
            'trade_affinity', 'growth_affinity',
        )
        mydict = { x: "foo" for x in expected_attribs }
        b = lacuna.empire.Species( self.sitter, mydict )
        for i in expected_attribs:
            self.assertTrue( hasattr(b, i) )

    def test_species_template(self):
        expected_attribs = (
            'name', 'description', 'min_orbit', 'max_orbit', 'manufacturing_affinity',
            'deception_affinity', 'research_affinity', 'management_affinity', 'farming_affinity',
            'mining_affinity', 'science_affinity', 'environmental_affinity', 'political_affinity',
            'trade_affinity', 'growth_affinity',
        )
        mydict = { x: "foo" for x in expected_attribs }
        b = lacuna.empire.SpeciesTemplate( self.sitter, mydict )
        for i in expected_attribs:
            self.assertTrue( hasattr(b, i) )

#@unittest.skip("skipping Empire")
class Empire(unittest.TestCase, Connector):
    @classmethod
    def setUpClass(self):
        self.tle_connect(self)
    def test_fetch_captcha(self):
        rv = self.sitter.empire.fetch_captcha()
        self.assertTrue( rv['guid'] and rv['url'] )

@unittest.skip("skipping MyEmpire")
class MyEmpire(unittest.TestCase, Connector):
    """ Test the lacuna.empire.MyEmpire class.
    """
    @classmethod
    def setUpClass(self):
        self.tle_connect(self)

    @unittest.skip("skipping")
    def test_boosts(self):
        ### CHECK
        ### If this is being run against an empire that's never had boosts on, 
        ### the test might fail.  Once a boost has been turned on, ever, its 
        ### expiration date is what shows up in the view_boosts() retval, even 
        ### if that date is long in the past.  But if the boost has never been 
        ### turned on, I don't know what value gets returned.  I'm attempting 
        ### to deal with a false return in that case, but since I don't have 
        ### any empires in this situation, I don't know what'll happen.
        sb = self.sitter.empire.view_boosts()
        self.sitter.empire.boost_building()
        self.sitter.empire.boost_energy()
        self.sitter.empire.boost_food()
        self.sitter.empire.boost_happiness()
        self.sitter.empire.boost_ore()
        self.sitter.empire.boost_storage()
        self.sitter.empire.boost_water()
        self.sitter.empire.boost_spy_training()
        eb = self.sitter.empire.view_boosts()
        for attr in[ 'building', 'energy', 'food', 'happiness', 'ore', 'storage', 'water', 'spy_training' ]:
            old = time.strptime( getattr(sb, attr), "%d %m %Y %H:%M:%S +0000" ) if getattr(sb, attr) else 0
            new = time.strptime( getattr(eb, attr), "%d %m %Y %H:%M:%S +0000" )
            self.assertTrue( old < new )

    @unittest.skip("skipping")
    def test_change_password(self):
        oldpw   = self.real.password
        candpw  = oldpw + "1"
        self.real.empire.change_password( candpw, candpw )
        newpw   = self.real.password
        self.assertTrue( oldpw != newpw )
        self.assertEqual( newpw, candpw )

    @unittest.skip("skipping")
    def test_id_numeric(self):
        self.assertTrue( re.match("^\d+$", str(self.sitter.empire.id)) )

    @unittest.skip("skipping")
    def test_home_planet_id_numeric(self):
        self.assertTrue( re.match("^\d+$", str(self.sitter.empire.home_planet_id)) )

    #@unittest.skip("skipping")
    def test_rpc(self):
        start_rpc = self.sitter.empire.rpc_count
        self.sitter.empire.find("foo")
        end_rpc = self.sitter.empire.rpc_count
        ### assertEqual( start_rpc + 1, end_rpc) -- this isn't always going to 
        ### be true, as end_rpc may be more than one greater, depending on 
        ### what else is happening.  Asserting that end_rpc is greater than 
        ### start_rpc is really what we're going for anyway.
        self.assertTrue( start_rpc < end_rpc )

    @unittest.skip("skipping")
    def test_body_counts(self):
        station_ids = self.sitter.empire.stations.keys()
        colonie_ids = self.sitter.empire.colonies.keys()
        planet_ids  = self.sitter.empire.planets.keys()
        self.assertEqual( len(planet_ids), (len(station_ids) + len(colonie_ids)) )

    @unittest.skip("skipping")
    def test_edit_profile(self):
        old_pro = self.real.empire.view_profile()
        cand_desc = old_pro.description + "1"
        self.real.empire.edit_profile({ 'description': cand_desc })
        new_pro = self.real.empire.view_profile()
        self.assertTrue( old_pro.description != new_pro.description )
        self.assertEqual( cand_desc, new_pro.description )

    @unittest.skip("skipping")
    def test_find_empire(self):
        emps = self.sitter.empire.find( self.sitter.empire.name )
        found = False 
        for e in emps:
            if e.name == self.sitter.empire.name:
                found = True
        self.assertTrue( found )

    @unittest.skip("skipping")
    def test_get_invite_friend_url(self):
        url = self.sitter.empire.get_invite_friend_url()['referral_url']
        self.assertTrue( re.match("https?://(us1|pt)\.lacunaexpanse\.com/#referral=[\w-]{36}", url) )

    @unittest.skip("skipping")
    def test_get_species_templates(self):
        tmpls = self.sitter.empire.get_species_templates()
        ok = True
        for t in tmpls:
            ### No need to check each key in each template dict - it there's a 
            ### 'name' key we'll assume it's a full template.
            if not hasattr(t, 'name'):
                ok = False
        self.assertTrue( ok )

    @unittest.skip("skipping")
    def test_invite_friend(self):
        self.sitter.empire.invite_friend("flurble123456@mailinator.com", "Come join me TEST")
        self.assertTrue( True )

    @unittest.skip("skipping")
    def test_redeem_essentia_code(self):
        with self.assertRaises( err.ServerError ):
            self.sitter.empire.redeem_essentia_code("56cc359e-8ba7-4db7-b608-8cb861c65510")

    @unittest.skip("skipping")
    def test_redefine_species_limits(self):
        limits = self.sitter.empire.redefine_species_limits()
        ok = True
        if not 'can' in limits: # See test_get_species_templates() comment
            ok = False
        self.assertTrue( ok )

    @unittest.skip("skipping")
    def test_redefine_species(self):
        old_stats = self.sitter.empire.view_species_stats()
        cand_desc = old_stats.description + "1"
        stats_dict = old_stats.to_dict()
        stats_dict['description'] = cand_desc
        self.sitter.empire.redefine_species( stats_dict )
        new_stats = self.sitter.empire.view_species_stats()
        self.assertTrue( old_stats.description != new_stats.description )
        self.assertEqual( cand_desc, new_stats.description )

    @unittest.skip("skipping")
    def test_set_status_message(self):
        old_msg = self.sitter.empire.status_message
        cand_msg = old_msg + "1"
        self.sitter.empire.set_status_message( cand_msg )
        new_msg = self.sitter.empire.status_message
        self.assertTrue( old_msg != new_msg )
        self.assertEqual( cand_msg, new_msg )

    @unittest.skip("skipping")
    def test_view_public_profile(self):
        pro = self.sitter.empire.view_public_profile( self.sitter.empire.id )
        self.assertEqual( pro.id, self.sitter.empire.id )

    @unittest.skip("skipping")
    def test_view_boosts(self):
        boosts = self.sitter.empire.view_boosts()
        ok = True
        if not hasattr(boosts, 'food'): # See test_get_species_templates() comment
            ok = False
        self.assertTrue( ok )

    @unittest.skip("skipping")
    def test_view_profile_with_sitter(self):
        with self.assertRaises( err.ServerError ):
            profile = self.sitter.empire.view_profile()

    @unittest.skip("skipping")
    def test_view_profile_with_real(self):
        profile = self.real.empire.view_profile()
        ok = True
        if not hasattr(profile, 'description'):     # See test_get_species_templates() comment
            ok = False
        self.assertTrue( ok )

    @unittest.skip("skipping")
    def test_view_species_stats(self):
        stats = self.sitter.empire.view_species_stats()
        ok = True
        if not hasattr(stats, 'name'): # See test_get_species_templates() comment
            ok = False
        self.assertTrue( ok )

if __name__ == '__main__':
    unittest.main()

