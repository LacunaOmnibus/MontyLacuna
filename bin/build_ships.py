#!/usr/bin/python3

import configparser, os, re, sys
bindir = os.path.abspath(os.path.dirname(__file__))
libdir = bindir + "/../lib"
sys.path.append(libdir)

import argparse, lacuna


"""
>>> py build_ships.py --name Earf --type sweeper --num 10 --level 30

Builds ships at all shipyards on the planet that are at --level or higher.

Right now, if any of those shipyards are already building, this counts how 
many queue slots are left.  The max_buildable count takes that into account.



Doesn't do any shipbuilding yet, but you can run it to get some output.


"""


def get_args():
    parser = argparse.ArgumentParser(
        description = 'Build ships in bulk.',
        epilog      = 'This shows at the end after help.',
    )
    ### https://docs.python.org/3.4/library/argparse.html#the-add-argument-method
    parser.add_argument( '--name', 
        metavar     = '<planet>',
        dest        = 'pname',
        action      = 'store',
        required    = True,
        help        = 'Name of planet on which to build ships.'
    )
    parser.add_argument( '--type', 
        metavar     = '<shiptype>',
        dest        = 'stype',
        action      = 'store',
        required    = True,
        help        = "Type of ship to build (eg 'scow_mega')."
    )
    parser.add_argument( '--num', 
        metavar     = '<count>',
        action      = 'store',
        type        = int,
        required    = True,
        help        = 'Number to build.'
    )
    parser.add_argument( '--level', 
        metavar     = '<lvl>',
        dest        = 'min_sy_lvl',
        action      = 'store',
        type        = int,
        default     = 1,
        help        = 'Minimum shipyard level to use for building'
    )
    return parser.parse_args()

def connect():
    return lacuna.clients.Member(
        config_file = bindir + "/../etc/lacuna.cfg",
        config_section = 'play_test',
    )

def get_shipyards():
    mymax = 0
    yards = planet.get_buildings_bytype( 'shipyard', args.min_sy_lvl )
    if not yards:
        raise RuntimeError("You don't have any shipyards of the required level.")
    for y in yards:
        if hasattr(y, 'work'):
            ships, num, cost = y.view_build_queue()
            mymax += (int(y.level) - num)                    # SHIT y.level is a string.
        else:
            mymax += int(y.level)
    return( yards, mymax )



args    = get_args()
client  = connect()

client.cache_on("my_planets", 3600)
planet  = client.get_body_byname( args.pname )

### We're going to want to get at those shipyards a few times in here, but we 
### don't want to draw from the cache from a previous run of this script, 
### because we have to check for whether the shipyards are building anything 
### or not.
### So turn shipyard caching on, but clear its contents.
client.cache_on("shipyards_for_building", 3600)
client.cache_clear()
yards, max_buildable = get_shipyards()
print( "You have", len(yards), "shipyards of the correct level." )
print( "You can build up to", max_buildable, "ships at a time." )


