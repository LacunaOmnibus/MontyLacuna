#!/usr/bin/python3


### BE SURE TO RUN THIS WITH -v -- IT'S OCCASIONALLY DOING SOMETHING I DON'T 
### UNDERSTAND YET AND WON'T WITHOUT -v.

import os, sys
bindir = os.path.abspath(os.path.dirname(sys.argv[0]))
libdir = bindir + "/../lib"
sys.path.append(libdir)

import logging

import lacuna
import lacuna.binutils.libbuild_ships as lib

bs  = lib.BuildShips()
l   = bs.client.user_logger


### bs.planets will be a list, containing either just the planet name passed 
### in by the user, or all of the user's planet names if 'all' was passed in.
for pname in bs.planets:

    ### Set the current planet name as our 'working' planet
    bs.set_planet( pname )

    ### Get a list of shipyards that match the user's CLI args
    shipyards = bs.get_shipyards()
    l.info( "{} has {} shipyards of the correct level.".format(bs.planet.name, len(shipyards)) )

    ### Ensure building the requested ship type is possible, and figure out 
    ### how many should be built.
    try:
        num_to_build = bs.determine_buildable( shipyards )
    except KeyError as e:
        l.warning( "Skipping {} because:".format(bs.planet.name) )
        l.warning( "\t{}:".format(e) )
        continue

    if num_to_build <= 0:
        continue
    requested = 'max' if bs.args.num == 0 else bs.args.num
    l.info( "You requested to build {} ships.  I'm going to try to build {:,} ships."
        .format(requested, num_to_build)
    )
    if requested != 'max' and not bs.args.topoff and int(num_to_build) < int(requested):
        l.info( "I'm building fewer than requested for a reason. You're probably low on spaceports." )

    ### Doo eet.
    left_to_build = num_to_build
    for y in shipyards:
        ships, building_now, cost = y.view_build_queue()
        num_to_build_here = y.level - building_now
        num_to_build_here = left_to_build if left_to_build < num_to_build_here else num_to_build_here
        left_to_build -= num_to_build_here
        l.debug( "About to try building {} ships." .format(num_to_build_here))
        if num_to_build_here > 0:
            y.build_ship( bs.shiptype, num_to_build_here )
        else:
            ### CHECK
            ### I'm not sure why this is hitting periodically.
            l.info( "Looks like we've added all to the queue that we can." )
        l.info( "I'm building {} ships at the sy at ({},{})." .format(num_to_build_here, y.x, y.y))
        if num_to_build_here > 25:
            l.info( "Remember that the Shipyard build queue in game will only ever display the first " )
            l.info( "Shipyard build queues in game displays 25 ships max.  I am building {}.".format(num_to_build_here) )
        elif left_to_build <= 0:
            break

    built = num_to_build
    if left_to_build != 0:
        l.info( "I wanted to build {} more ships, but the build queues were already working when I started.".format(left_to_build) )
        built = num_to_build - left_to_build

    l.info( "I am now building {:,} {} on {}.".format(built, bs.args.type, bs.planet.name) )


