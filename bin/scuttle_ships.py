#!/usr/bin/python3

import os, sys
bindir = os.path.abspath(os.path.dirname(sys.argv[0]))
libdir = bindir + "/../lib"
sys.path.append(libdir)

import logging

import lacuna
import lacuna.binutils.libscuttle_ships as lib

ss  = lib.ScuttleShips()
l   = ss.client.user_logger

### Not much for us to do here except call scuttle().
cnt = ss.scuttle()
s = 'ship' if cnt == 1 else 'ships'
l.info( "I just scuttled {:,} {}.".format(cnt, s) )

