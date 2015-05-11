#!/usr/bin/python3

import logging, os, sys
bindir = os.path.abspath(os.path.dirname(sys.argv[0]))
libdir = bindir + "/../lib"
sys.path.append(libdir)

import lacuna
import lacuna.binutils.librecall_all_ships as lib

### Get library class instance
recall = lib.RecallShips()

### Get planet
recall.client.cache_on("my_planets", 3600)
planet = recall.client.get_body_byname( recall.bodyname )

### Get any spaceport
sp = planet.get_buildings_bytype( 'spaceport', 1, 1 )[0]

### Recall our ships
ships = sp.recall_all()

### Produce report on what we just did unless the user included --quiet
recall.show_report(ships)

