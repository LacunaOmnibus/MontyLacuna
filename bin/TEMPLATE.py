#!/usr/bin/python3

import logging, os, sys
bindir = os.path.abspath(os.path.dirname(sys.argv[0]))
libdir = bindir + "/../lib"
sys.path.append(libdir)

import lacuna


Fix all instances of "CHECK" below (and delete this line).


### This is the binutils lib to import.
import binutils.CHECK as lib



### The 'CHECK' below is the name of the class in the binutils/lib* you're 
### importing.  Change that, and change OBJECT to something more reasonable.  
### You have to change OBJECT several times.
OBJECT  = lib.CHECK()



client  = OBJECT.connect()
l       = client.user_logger

if not OBJECT.args.quiet:
    client.user_log_stream_handler.setLevel(logging.INFO)

client.cache_on("my_planets", 3600)
planet = client.get_body_byname( OBJECT.args.name )

