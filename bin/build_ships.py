#!/usr/bin/python3

import os, sys
bindir = os.path.abspath(os.path.dirname(sys.argv[0]))
libdir = bindir + "/../lib"
sys.path.append(libdir)

import lacuna
import binutils.libbuild_ships as lib


"""
>>> py bin/build_ships.py --num 10 --level 30 "bmots support 02" sweeper

Builds ships at all shipyards on the planet that are at --level or higher.

Right now, if any of those shipyards are already building, this counts how 
many queue slots are left.  The max_buildable count takes that into account.



Doesn't do any shipbuilding yet, but you can run it to get some output.

"""

bs      = lib.BuildShips()
client  = bs.connect()

client.cache_on("my_planets", 3600)
planet  = client.get_body_byname( bs.args.name )

### We're going to want to get at those shipyards a few times in here, but we 
### don't want to draw from the cache from a previous run of this script, 
### because we have to check for whether the shipyards are building anything 
### or not.
### So turn shipyard caching on, but clear its contents.
client.cache_on("shipyards_for_building", 3600)
client.cache_clear()
yards, max_buildable = bs.get_shipyards( planet )
print( "You have", len(yards), "shipyards of the correct level." )
print( "You can build up to", max_buildable, "ships at a time." )


