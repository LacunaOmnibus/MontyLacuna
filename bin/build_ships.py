#!/usr/bin/python3

import os, sys
bindir = os.path.abspath(os.path.dirname(sys.argv[0]))
libdir = bindir + "/../lib"
sys.path.append(libdir)

import logging
import lacuna
import lacuna.exceptions as err
import lacuna.binutils.libbuild_ships as lib
import lacuna.exceptions as err

bs  = lib.BuildShips()
l   = bs.client.user_logger

### bs.planets will be a list, containing either just the planet name passed 
### in by the user, or all of the user's planet names if 'all' was passed in.
for pname in bs.planets:

    ### Set the current planet name as our 'working' planet
    bs.set_planet( pname )

    ### Get a list of shipyards that match the user's CLI args
    try:
        shipyards = bs.get_shipyards()
    except err.NoSuchBuildingError as e:
        l.info( "{} does not have any shipyards of the right level.  Skipping.".format(bs.planet.name) )
        continue;
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
        building_now, left_to_build = bs.build_at_yard( y, left_to_build )
        l.info( "I'm building {} ships at the sy at ({},{})." .format(building_now, y.x, y.y))
        if building_now > 25:
            l.info( "Shipyard build queues in game displays 25 ships max.  I am building {}.".format(building_now) )
        if left_to_build <= 0:
            break

    built = num_to_build
    if left_to_build != 0:
        l.info( "I wanted to build {} more ships, but the build queues were already working when I started.".format(left_to_build) )
        built = num_to_build - left_to_build

    l.info( "I am now building {:,} {} on {}.".format(built, bs.args.type, bs.planet.name) )


