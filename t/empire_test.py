
import os, sys

bindir = os.path.abspath(os.path.dirname(__file__))
libdir = bindir + "/../lib"
sys.path.append(libdir)
import lacuna as lac

guest = lac.clients.Guest()

tmt = lac.clients.Member(
    config_file = bindir + "/../etc/lacuna.cfg",
    #config_section = 'my_sitter',
    #config_section = 'my_real',
    config_section = 'play_test',
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
###

### View my own empire's profile.
### This only works if you're logged in with your real, not sitter, password.
###
pro = tmt.empire.view_profile()
print( "I am from {} in {}, and my player name is {}.  I have won {} medals."
    .format(pro.city, pro.country, pro.player_name, len(pro.medals.keys()))
)


### See how many RPCs you've used so far.
### This does not use any RPCs, so you can check it as often as you'd like.
###
#print( "Number of RPCs used today by {} is {}". format(tmt.empire.name, tmt.empire.rpc_count) )


### Find a list of empires by name
###
#empires = tmt.empire.find( "Inf" )
#for i in empires:
#    print( "I found", i.name )


### View some other empire's profile.
###
#jt = tmt.empire.find( "Jandor Trading" )[0]
#pro = tmt.empire.view_public_profile( jt.id )
#print( "{}'s player name is {}, and they last logged in on {}."
#    .format(pro.name, pro.player_name, pro.last_login)
#)


### Edit your profile
###
#mydict = { 'status_message': 'This was set by empire_test.py' }
#tmt.empire.edit_profile( mydict )


### Change your password
###
#tmt.empire.change_password( 'foobar', 'foobar' )


### See info on your species
###
#spec = tmt.empire.view_species_stats()
#print( "My species, {}, is described as {}, and can inhabit orbits {}-{}"
#    .format(spec.name, spec.description, spec.min_orbit, spec.max_orbit)
#)


### See what boosts you have turned on
###
#boosts = tmt.empire.view_boosts()
#print( "My building boost expires at {}.".format(boosts.building) )


### See the initial species templates
###
#tmpls = tmt.empire.get_species_templates()
#for i in tmpls:
#    print( "{} is described as {}" .format(i.name, i.description) )


### 
### From a logged-in client, you have access to most other objects via get_*() methods:
### 
# alliance = tmt.get_alliance()                   # Generic Alliance object, NOT set to any specific alliance.
# my_alliance = tmt.get_my_alliance()             # This one is set to my empire's alliance.
# body1 = tmt.get_body( integer body ID )         # Gotta go dig up the planet's ID.  Ugh.
# body2 = tmt.get_body_byname( Name of a body )   # Yay, I already know my planet's name.
# inbox = tmt.get_inbox()                         # My empire's mail inbox
# mymap = tmt.get_map()                           # Starmap
# mystats = tmt.get_stats()                       # Stats

