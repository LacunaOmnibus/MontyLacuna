
import os, sys
import pprint, re

bindir = os.path.abspath(os.path.dirname(sys.argv[0]))
libdir = bindir + "/../lib"
sys.path.append(libdir)

import lacuna as lac
pp = pprint.PrettyPrinter( indent = 4 )



### Set up a config section named 'my_guest' with a username but no password.
guest = lac.clients.Guest(
    config_file = bindir + "/../etc/lacuna.cfg",
    config_section = 'my_guest',
)
client = lac.clients.Member(
    config_file = bindir + "/../etc/lacuna.cfg",
    config_section = 'sitter',
)
stats = client.get_stats()


### credits() works fine from a guest account.
###
#guest_stats = guest.get_stats()
#guest_cred = guest_stats.credits()
#print( "TLE Play Testers:" )
#for i in guest_cred['Play Testers']:
#    print( "\t", i )


### Look at alliance stats by page
###
#ranks, num, page = stats.alliance_rank()
#print( "There are {:,} total alliances.".format(num) )
#print( "Names of alliances on page number {}:".format(page) )
#for i in ranks:
#    print( "\t", i.alliance_name )


### Look at alliance stats for a specific alliance
###
#ranks = stats.find_alliance_rank('influence', 'S.M.A')
#for i in ranks:
#    print( "{} appears on page {}.".format(i.alliance_name, i.page_number) )


### Get info on a single player empire
###
#player = stats.find_empire_rank( 'empire_size_rank', 'The United' )[0]
#print( "{} has ID {}.".format(player.empire_name, player.empire_id) )


### Get info on empire ranks
###
#empires, emp_cnt, page = stats.empire_rank( 'blargle' )
#print( "There are {} total empires.  We're looking at page {}.".format(emp_cnt, page) )
#for i in empires:
#    print( "{} is in the alliance {}, and has an off. success rate of {} and a def. success rate of {}."
#        .format(i.empire_name, i.alliance_name, i.offense_success_rate, i.defense_success_rate) 
#    )


### Get info on colony ranks
###
#colonies = stats.colony_rank( 'blargle' )
#for i in colonies:
#    print( "{} is owned by {}.".format(i.planet_name, i.empire_name) )


### Get info on spy ranks
###
#spies = stats.spy_rank()
#for i in spies:
#    print( "{}, level {}, with a success rate of {} and a dirty score of {}, is owned by {}."
#        .format(i.spy_name, i.level, i.success_rate, i.dirtiest, i.empire_name)
#    )


### Get weekly medal winners
###
#winners = stats.weekly_medal_winners()
#for i in winners:
#    print( "{} won the {} medal {} times.  This should display the '{}' image."
#        .format(i.empire_name, i.medal_name, i.times_earned, i.medal_image)
#    )

