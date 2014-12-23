
import itertools, os, sys

bindir = os.path.abspath(os.path.dirname(sys.argv[0]))
libdir = bindir + "/../lib"
sys.path.append(libdir)
import lacuna as lac

guest = lac.clients.Guest()

client = lac.clients.Member(
    config_file = bindir + "/../etc/lacuna.cfg",
    config_section = 'sitter',
)

### Using a non-logged-in guest account
###
#for n in ['tmtowtdi', 'fake_name']:
#    if guest.is_name_available(n):
#        print(n, "is available for use.")
#    else:
#        print(n, "is taken, and is not available for use.")
###
### Almost everything else requires a logged-in account.


### View my own empire's profile.
### This only works if you're logged in with your real, not sitter, password.
###
#pro = client.empire.view_profile()
#print( "I am from {} in {}, and my player name is {}.  I have won {} medals."
#    .format(pro.city, pro.country, pro.player_name, len(pro.medals.keys()))
#)


### View 10 colonies, and then 10 stations, just to show that they're 
### separate.
###
#print( "10 of my colonies:" )
#for pid, pname in list( itertools.islice(client.empire.colonies.items(), 10) ):
#    print( "\t{} has ID {}.".format(pname, pid) )
#print( "10 of my stations:" )
#for pid, pname in list( itertools.islice(client.empire.stations.items(), 10) ):
#    print( "\t{} has ID {}.".format(pname, pid) )



### See how many RPCs you've used so far.
### This does not use any RPCs, so you can check it as often as you'd like.
###
#print( "Number of RPCs used today by {} is {}". format(client.empire.name, client.empire.rpc_count) )


### Find a list of empires by name
###
#empires = client.empire.find( "Inf" )
#for i in empires:
#    print( "I found", i.name )


### View some other empire's profile.
###
#jt = client.empire.find( "Jandor Trading" )[0]
#pro = client.empire.view_public_profile( jt.id )
#print( "{}'s player name is {}, and they last logged in on {}."
#    .format(pro.name, pro.player_name, pro.last_login)
#)


### Edit your profile
###
#mydict = { 'status_message': 'This was set by empire_test.py' }
#client.empire.edit_profile( mydict )


### Change your password
###
#client.empire.change_password( 'foobar', 'foobar' )


### See info on your species
###
#spec = client.empire.view_species_stats()
#print( "My species, {}, is described as {}, and can inhabit orbits {}-{}"
#    .format(spec.name, spec.description, spec.min_orbit, spec.max_orbit)
#)


### See what boosts you have turned on
###
#boosts = client.empire.view_boosts()
#print( "My building boost expires at {}.".format(boosts.building) )


### See the initial species templates
###
#tmpls = client.empire.get_species_templates()
#for i in tmpls:
#    print( "{} is described as {}" .format(i.name, i.description) )


### Redefine your species
### CAREFUL this is going to spend 100 E.  Make sure you're logged in using a 
### test account!
###
#new_species = {
#    'name':                     "My new name",
#    'description':              "My new description",
#    'min_orbit':                1,
#    'max_orbit':                7,
#    'manufacturing_affinity':   7,
#    'deception_affinity':       7,
#    'research_affinity':        1,
#    'management_affinity':      1,
#    'farming_affinity':         1,
#    'mining_affinity':          1,
#    'science_affinity':         7,
#    'environmental_affinity':   1,
#    'political_affinity':       4,
#    'trade_affinity':           1,
#    'growth_affinity':          7,
#}
#raise KeyError("This is really going to spend 100 E - make real sure you're on a test account!")
#client.empire.redefine_species( new_species )


### Redeem an essentia code
### 
#client.empire.redeem_essentia_code( '56cc359e-8ba7-4db7-b608-8cb861c65510' )


### 
### From a logged-in client, you have access to most other objects via get_*() methods:
### 
# alliance = client.get_alliance()                   # Generic Alliance object, NOT set to any specific alliance.
# body1 = client.get_body( integer body ID )         # Gotta go dig up the planet's ID.  Ugh.
# body2 = client.get_body_byname( Name of a body )   # Yay, I already know my planet's name.
# inbox = client.get_inbox()                         # My empire's mail inbox
# mymap = client.get_map()                           # Starmap
# mystats = client.get_stats()                       # Stats

#my_alliance = client.get_my_alliance()             # This one is set to my empire's alliance.
#if my_alliance:
#    print( "You are in the alliance named {}.".format(my_alliance.name) )
#else:
#    print( "You are not in an alliance." )


