#!/usr/bin/python3

import os, sys
bindir = os.path.abspath(os.path.dirname(sys.argv[0]))
libdir = bindir + "/../lib"
sys.path.append(libdir)

import logging

import lacuna
import lacuna.binutils.libbuild_ships as lib

bs  = lib.BuildShips()
l   = bs.client.user_logger

bs.client.cache_on("shipyards_for_building", 30)
bs.client.cache_clear( "shipyards_for_building" )

### Get a list of shipyards that match the user's CLI args
shipyards = bs.get_shipyards()
l.info( "You have {} shipyards of the correct level.".format(len(shipyards)) )

### Ensure building the requested ship type is possible, and figure out how 
### many should be built.
num_to_build = bs.determine_buildable( shipyards )
requested = 'max' if bs.args.num == 0 else bs.args.num
l.info( "You requested to build {} ships.  I'm going to try to build {:,} ships."
    .format(requested, num_to_build)
)

### Doo eet.
left_to_build = num_to_build
for y in shipyards:
    ships, building_now, cost = y.view_build_queue()
    num_to_build_here = y.level - building_now
    num_to_build_here = left_to_build if left_to_build < num_to_build_here else num_to_build_here
    left_to_build -= num_to_build_here
    y.build_ship( bs.args.type, num_to_build_here )
    l.info( "I'm building {} ships at the sy at ({},{})." .format(num_to_build_here, y.x, y.y))
    if num_to_build_here > 25:
        l.info( "Remember that the Shipyard build queue in game will only ever display the first " )
        l.info( "25 ships being built.  I'm definitely building {}.".format(num_to_build_here) )
    elif left_to_build <= 0:
        break

built = num_to_build
if left_to_build != 0:
    l.info( "I wanted to build {} more ships, but the build queues were already working when I started.".format(left_to_build) )
    built = num_to_build - left_to_build

l.info( "I am now building {:,} {} in various shipyards on {}.".format(built, bs.args.type, bs.planet.name) )

