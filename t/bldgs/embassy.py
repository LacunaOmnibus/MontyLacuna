
import os, sys
bindir = os.path.abspath(os.path.dirname(__file__))
libdir = bindir + "/../../lib"
sys.path.append(libdir)

import lacuna as lac


###
### This creates two clients.  One must be the leader of an alliance, and the 
### other should be un-allied.
###


### guild leader
leader_client = lac.clients.Member(
    config_file = bindir + "/../../etc/lacuna.cfg",
    config_section = 'play_test',
)
leader_planet   = leader_client.get_body_byname( 'bmots rof 1.4' )
leader_emb      = leader_planet.get_building_coords( -4, 0 )

### guild invitee
invitee_client = lac.clients.Member(
    config_file = bindir + "/../../etc/lacuna.cfg",
    config_section = 'play_test_two',
)
invitee_planet   = invitee_client.get_body_byname( 'Evolme' )
invitee_emb      = invitee_planet.get_building_coords( 5, 0 )


stats = leader_client.get_stats()

### Create new alliance
###
#ally = leader_emb.create_alliance( 'TestTwo Alliance' )
#print( "I created a new alliance named {}.  The leader's ID is {}, and it was created on {}."
#    .format(ally.name, ally.leader_id, ally.date_created)
#)


### Leave current alliance
###
#invitee_emb.leave_alliance( )


### Dissolve existing alliance
### Note this is using the invitee's embassy.  I suggest you have your invitee 
### whip up a quick alliance and dissolve that, instead of dissolving your 
### leader's alliance.
###
#invitee_emb.dissolve_alliance()


### Get alliance status
###
#ally = leader_emb.get_alliance_status( )
#print( "My alliance is named {}.  The leader's ID is {}, and it was created on {}."
#    .format(ally.name, ally.leader_id, ally.date_created)
#)


### Send alliance invite
###
#player = stats.find_empire_rank( '', 'tmtowtdi_test' )[0]
#print( "{} has ID {}.".format(player.empire_name, player.empire_id) )
#leader_emb.send_invite( player.empire_id, "Come join my alliance!" )


### Get list of invites your alliance has sent out to potential members, but 
### which have not been accepted or rejected yet.
###
#invites = leader_emb.get_pending_invites()
#for i in invites:
#    print( "Invite ID {} has been sent out to empire {}, whose ID is {}."
#        .format(i.id, i.name, i.empire_id)
#    )


### Withdraw an already-sent alliance invite
###
#invites = leader_emb.get_pending_invites()
#leader_emb.withdraw_invite( invites[0].id, "Your invite is being withdrawn." )


### Get list of invitations sent to your empire from alliances you're not 
### currently a member of
###
#invites = invitee_emb.get_my_invites()
#for i in invites:
#    print( "I have been invited to join {} (ID {}).  The invite ID is {}."
#        .format(i.name, i.alliance_id, i.id)
#    )


### Accept an invitation to an alliance
###
#invites = invitee_emb.get_my_invites()
#ally = invitee_emb.accept_invite( invites[0].id )
#print( "I accepted an invite to {}.  The leader's ID is {}, and it was created on {}."
#    .format(ally.name, ally.leader_id, ally.date_created)
#)


### Reject an invitation to an alliance
###
#invites = invitee_emb.get_my_invites()
#invitee_emb.reject_invite( invites[0].id )


### Set a new alliance leader
###
#my_ally = leader_client.get_my_alliance()
#print( "{}'s current leader's ID is {}.".format(my_ally.name, my_ally.leader_id) )
#new_leader = ''
#for i in my_ally.members:
#    if i.id != my_ally.leader_id:
#        print( "My new leader will be {} (ID {}).".format(i.name, i.id) )
#        new_leader = i
#if not new_leader:
#    raise KeyError("I was unable to find a new leader.")
#my_ally_now = leader_emb.assign_alliance_leader( new_leader.id )
#print( "The new leader of {} has an ID of {}."
#    .format(my_ally_now.name, my_ally_now.leader_id)
#)


###
### At this point, your invitee is the leader of the alliance.  Go reassign 
### leadership to the original leader again.
###


### Update alliance settings
###
#ally_settings = {
#    'forum_uri': 'http://www.example.com',
#    'description': 'This is a new shiny public description',
#    'announcements': 'This is only visible to alliance members but it was definitely set by our test script.  Blarg.',
#}
#ally = leader_emb.update_alliance( ally_settings )
#print( "After update, our forum is at {}, our description is {}, and our announcements are {}."
#    .format(ally.forum_uri, ally.description, ally.announcements)
#)


### View the contents of the alliance stash
###
#ally_stash = invitee_emb.view_stash()
#print( "I can exchange {} more times today, up to {} units per exchange."
#    .format(ally_stash.exchanges_remaining_today, ally_stash.max_exchange_size)
#)
#print( "Some items already in the stash:" )
#cnt = 0
#for i in ally_stash.stash:
#    cnt += 1
#    if cnt > 3:
#        break
#    print( "\tThere are {:,} of {} in the stash.".format(int(ally_stash.stash[i]), i) )
#print( "Some items I have stored that I can exchange with the stash:" )
#cnt = 0
#for i in ally_stash.stored:
#    cnt += 1
#    if cnt > 3:
#        break
#    print( "\tI have {:,} of {} that can be added to the stash.".format(int(ally_stash.stored[i]), i) )


### Donate to the stash
### It's likely your leader's alliance's stash is already full, and you can't 
### donate to a full stash.  Have your invitee drop ally, then create his own 
### brand new alliance to test this.
###
#donation = { 'apple': 1, }
#ally_stash = invitee_emb.donate_to_stash(donation)
#print( "Currently in the stash:" )
#for i in ally_stash.stash:
#    print( "\tThere are {:,} of {} in the stash.".format(int(ally_stash.stash[i]), i) )


### Exchange with the stash
###
#donation = { 'fungus': 1, }
#request = {  'apple': 1 }
#ally_stash = invitee_emb.exchange_with_stash(donation, request)
#print( "Currently in the stash:" )
#for i in ally_stash.stash:
#    print( "\tThere are {:,} of {} in the stash.".format(int(ally_stash.stash[i]), i) )



