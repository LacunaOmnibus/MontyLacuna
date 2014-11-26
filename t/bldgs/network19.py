
import os, re, sys
bindir = os.path.abspath(os.path.dirname(sys.argv[0]))
libdir = bindir + "/../../lib"
sys.path.append(libdir)

import lacuna as lac

glc = lac.clients.Member(
    config_file = bindir + "/../../etc/lacuna.cfg",
    config_section = 'my_sitter',
    #config_section = 'play_test',
)
my_planet   = glc.get_body_byname( 'bmots rof 1.4' )
net19       = my_planet.get_building_coords( 1, -2 )


### Check if we're restricting coverage or not.  Restrict if we're not, open 
### if we are.
###
#view = net19.view()
#print( "At first, restrict coverage was", view['restrict_coverage'] )
#if view['restrict_coverage'] == '1':
#    net19.restrict_coverage( 0 )
#else:
#    net19.restrict_coverage( 1 )
#view = net19.view()
#print( "After toggling, restrict coverage is", view['restrict_coverage'] )



### View news.
#stories, feeds = net19.view_news()
#for s in stories[0:3]:
#    print( "Headline '{}' -- dateline {}".format(s.headline, s.date) )
#
#print( "This Network 19 can view the following feeds:" )
#for z in feeds[0:3]:
#    print( "In zone {} -- {}".format(z.zone, z.url) )

