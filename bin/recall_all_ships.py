#!/usr/bin/python3

import logging, os, sys
bindir = os.path.abspath(os.path.dirname(sys.argv[0]))
libdir = bindir + "/../lib"
sys.path.append(libdir)

import lacuna


### This is the binutils lib to import.
import binutils.librecall_all_ships as lib

recall  = lib.RecallShips()
client  = recall.connect()
l       = client.user_logger

if not recall.args.quiet:
    client.user_log_stream_handler.setLevel(logging.INFO)

l.info("foobar")
quit()

client.cache_on("my_planets", 3600)
planet = client.get_body_byname( recall.args.name )

