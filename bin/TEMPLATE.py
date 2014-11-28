#!/usr/bin/python3

import os, sys
bindir = os.path.abspath(os.path.dirname(sys.argv[0]))
libdir = bindir + "/../lib"
sys.path.append(libdir)

import logging

import lacuna
### This is the binutils lib to import
import binutils.librecall_all_spies as lib

client  = bs.connect()
l       = client.user_logger

if not bs.args.quiet:
    client.user_log_stream_handler.setLevel(logging.INFO)

client.cache_on("my_planets", 3600)
planet = client.get_body_byname( bs.args.name )

### This is the name of the class in the binutils/lib* you're importing
recall  = lib.RecallAllSpies()

