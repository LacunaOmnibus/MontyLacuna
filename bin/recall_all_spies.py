#!/usr/bin/python3

import os, sys
bindir = os.path.abspath(os.path.dirname(sys.argv[0]))
libdir = bindir + "/../lib"
sys.path.append(libdir)

import logging
import lacuna
import binutils.librecall_all_spies as lib


recall  = lib.RecallAllSpies()
client  = recall.connect()
l       = client.user_logger

if not recall.args.quiet:
    client.user_log_stream_handler.setLevel(logging.INFO)

client.cache_on("my_planets", 3600)
planet = client.get_body_byname( recall.args.name )

client.cache_on("nothome_spies", 3600)

### Get IntMin
intmin = planet.get_buildings_bytype( 'intelligence', 1, 1 )[0]
l.debug("Got intmin")

### Get bodies where my spies who are out are located.  'id': 'name'
client.cache_off()
foreign_bodies = recall.find_nothome_spies( planet.id, intmin )
l.debug( "Got {} bodies containing my nothome spies.".format(len(foreign_bodies.keys())) )

### Get SpacePort
client.cache_on("buildings", 3600)
sp = planet.get_buildings_bytype( 'spaceport', 1, 1 )[0]
l.debug("Got spaceport")

### Do eet.
cnt = 0
for bid, name in foreign_bodies.items():
    cnt += 1
    l.info( "Recalling spies from {} (ID {}).".format(name, bid) )
    ### Turn the cache back off, or we'll try to use the same ship to pick up 
    ### spies on multiple planets.
    client.cache_off()
    ship, ids = sp.get_spies_back( bid )

l.info( "You had spies on {} foreign bodies.  They've all been recalled.".format(cnt) )

