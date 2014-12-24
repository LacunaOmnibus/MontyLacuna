
import os
import sys
import pprint, re

bindir = os.path.abspath(os.path.dirname(sys.argv[0]))
libdir = bindir + "/../lib"
sys.path.append(libdir)

import lacuna as lac
pp = pprint.PrettyPrinter( indent = 4 )

glc = lac.clients.Member(
    config_file = bindir + "/../etc/lacuna.cfg",
    config_section = 'sitter',
    #config_section = 'play_test',
)


mymap = glc.get_map();


### View the laws reported by a given star.
###
### (-5,-1) is the first star I found near (0,0) that was seized.  It's a 
### Culture-seized star, and the point of this test is to ensure that you can 
### view laws passed by another alliance.  So if you're in Culture, go find a 
### star that's been seized by some other alliance, and use its coords below 
### instead.
###
#star_dict = {
#    'left': -5, 'right': -5,
#    'top': -1, 'bottom': -1
#}
#star = mymap.get_star_map(star_dict)[0]
#if hasattr(star, 'station'):
#    laws = star.view_nonseizure_laws()
#    print( "Laws passed by {}".format(star.station.name) )
#    for l in laws:
#        print( l.name )


### View all stars in a chunk of space using named arguments.
### Since we're calling view_laws() on each returned star for this test, you 
### should use a small chunk of space in your star_dict.
###
#star_dict = {
#    'left': -5,
#    'right': -5,
#    'top': -1,
#    'bottom': -1
#}
#stars = mymap.get_star_map(star_dict)
#for s in stars[0:5]:
#    print( "{} ({}, {}) is {} and, as far as my probes can tell, is orbited by {} bodies."
#        .format(s.name, s.x, s.y, s.color, len(s.bodies))
#    )
#    if hasattr(s, 'station'):
#        print( "This star has been claimed by station {} (id {}).".format(s.station.name, s.station.id) )
#    ###
#    ### Any star not under control of a station will have the single law "Not 
#    ### controlled by a station".
#    ###
#    laws = s.view_nonseizure_laws()
#    for l in laws:
#        print( "Law '{}' is in effect.".format(l.name) )


### View all stars in a chunk of space using positional arguments
###
#stars = mymap.get_stars( -1500, -1470, -1470, -1500 )
#for s in stars[0:5]:
#    print( "{} ({}, {}) is {} and, as far as my probes can tell, is orbited by {} bodies."
#        .format(s.name, s.x, s.y, s.color, len(s.bodies))
#    )


### Check on whether you've got a probe headed towards a given star and, if 
### so, when it'll land.
###
#my_planet = glc.get_body_byname("bmots01")
#probe_inc = mymap.check_star_for_incoming_probe( my_planet.star_id )
#if probe_inc:
#    print( "My probe will land on {} at {}".format(my_planet.star_name, probe_inc) )
#else:
#    print( "I don't have a probe headed towards", my_planet.star_name )


### Get a star by ID
###
#my_planet = glc.get_body_byname("bmots01")
#star = mymap.get_star( my_planet.star_id )
#print( "Star {} is {}.".format(star.name, star.color) )


### Get a star by name
###
#star = mymap.get_star_by_name( 'Schu Ize' )
#print( "Star {} is {}.".format(star.name, star.color) )


### Get star by coords
###
#star = mymap.get_star_by_xy( -303, 127 )
#print( "Star {} is {}.".format(star.name, star.color) )


### Get a list of stars whose name matches a string
###
#stars = mymap.search_stars( "Schu" )
#for i in stars:
#    print( "Star {} is {}.".format(i.name, i.color) )


### Check if there are any fissures visible to you in a given zone
###
#zone = '-1|0'
#zone_dict = { 'zone': zone, }
#fissures = mymap.probe_summary_fissures( zone_dict )
#if not len(fissures):
#    print( "There are no fissures visible to me in", zone )
#else:
#    for i in fissures:
#        print( "{} ({}, {}) has a fissure on it.".format(i.name, i.x, i.y) )


### Get a body object for any planet orbiting any star, provided you can see 
### the planet in your starmap.
###
#planet = mymap.get_orbiting_planet( 'Cho Iarnowy Ipr', 'DIXIE 2' )
#print( "{} is located at ({}, {}) and is a type {} planet."
#    .format(planet.name, planet.x, planet.y, planet.surface_type) 
#)


