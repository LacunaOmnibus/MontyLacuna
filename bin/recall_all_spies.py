#!/usr/bin/python3

import os, sys
bindir = os.path.abspath(os.path.dirname(sys.argv[0]))
libdir = bindir + "/../lib"
sys.path.append(libdir)

import lacuna
import lacuna.exceptions as err
import lacuna.binutils.librecall_all_spies as lib


recall  = lib.RecallAllSpies()
l       = recall.client.user_logger

### Turn on caching, get planet
recall.client.cache_on("recall_spies", 3600)
planet = recall.client.get_body_byname( recall.args.name )
recall.client.cache_off()

### Get IntMin
intmin = planet.get_buildings_bytype( 'intelligence', 1, 1 )[0]
l.debug("Got intmin")

### Get bodies where my spies who are out are located.  'id': 'name'
foreign_bodies = recall.find_nothome_spies( planet.id, intmin )
l.debug( "Got {} bodies containing my nothome spies.".format(len(foreign_bodies.keys())) )

### Get SpacePort
recall.client.cache_on("recall_spies", 3600)
sp = planet.get_buildings_bytype( 'spaceport', 1, 1 )[0]
recall.client.cache_off()
l.debug("Got spaceport")

### Do eet.
cnt = 0
failure = 0
for bid, name in foreign_bodies.items():
    cnt += 1
    l.info( "Recalling spies from {} (ID {}).".format(name, bid) )
    ### Turn the cache back off, or we'll try to use the same ship to pick up 
    ### spies on multiple planets.
    recall.client.cache_off()
    try:
        ship, ids = sp.get_spies_back( bid )
    except err.MissingResourceError as e:
        l.warning("No spies could be found on {}".format(name))
        failure += 1
        continue

l.info( "You had spies on {} foreign bodies.".format(cnt) )
if failure:
    l.error("No spies could be found on {} foreign bodies, even though I'm pretty sure they're there.  Only 100 spies get returned from a check, and the spies from {} likely just appear after 100 in the list.  You'll need to remove spies from other planets first."
        .format(failure, recall.args.name)
    )
if cnt - failure:
    l.info("We picked up spies from {} of those bodies.".format(cnt - failure) )

