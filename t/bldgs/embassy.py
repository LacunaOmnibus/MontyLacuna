
import os, sys
bindir = os.path.abspath(os.path.dirname(__file__))
libdir = bindir + "/../../lib"
sys.path.append(libdir)

import lacuna as lac

glc = lac.clients.Member(
    config_file = bindir + "/../../etc/lacuna.cfg",
    config_section = 'play_test',
)
my_planet = glc.get_body_byname( 'bmots rof 1.4' )
emb = my_planet.get_building_coords( -4, -0 )


### Create new alliance
###
#rva = emb.create_alliance( 'My Test Alliance' )
#glc.pp.pprint( rva )


### Leave current alliance
###
#rvb = emb.leave_alliance( )
#glc.pp.pprint( rvb )


### Dissolve existing alliance
###
#rvc = emb.dissolve_alliance( )
#glc.pp.pprint( rvc )


### Get alliance status
###
#rvd = emb.get_alliance_status( )
#glc.pp.pprint( rvd )


### Send alliance invite
###
#rve = emb.send_invite( 2403, "Ignore this invite - I'm testing code." )    # IO
#glc.pp.pprint( rve )


### Get list of pending invites to your alliance
###
#rvf = emb.get_pending_invites()
#glc.pp.pprint( rvf['invites'] )
#print("------------")


### Withdraw an already-sent alliance invite
###
#rvg = emb.withdraw_invite( 5811, "Ignore this too - still testing" )    # IO
#glc.pp.pprint( rvg )
### Show pending invites again to show the withdrawn one is gone
#rvh = emb.get_pending_invites()
#glc.pp.pprint( rvh['invites'] )


### Get list of invitations sent to your empire from alliances you're not 
### currently a member of
###
#rvi = emb.get_my_invites()
#glc.pp.pprint( rvi['invites'] )


### Accept an invitation to an alliance
###
#rvj = emb.accept_invite( rvi['invites'][0]['id'] )
#glc.pp.pprint( rvj )


### Reject an invitation to an alliance
###
#rvk = emb.reject_invite( rvi['invites'][0]['id'] )
#glc.pp.pprint( rvk )


### Set a new alliance leader
###
#rvl = emb.assign_alliance_leader( some_integer_empire_ID )
#glc.pp.pprint( rvl )


### Update alliance settings
###
#ally_settings = {
#    'forum_uri': 'http://www.example.com',
#    'description': 'This is a public description',
#    'announcements': 'This is only visible to alliance members',
#}
#rvm = emb.update_alliance( ally_settings )
#glc.pp.pprint( rvm )


### View the contents of the alliance stash
###
#rvn = emb.view_stash()
#glc.pp.pprint( rvn['stash'] )


### Donate to the stash
#donation = { 'apple': 1, }
#rvo = emb.donate_to_stash(donation)
#glc.pp.pprint( rvo['stash'] )


### Exchange with the stash
###
#donation = { 'lapis': 20000, }
#request = {  'fungus': 20000 }
#rvp = emb.exchange_with_stash(donation, request)
#glc.pp.pprint( rvp['stash'] )



