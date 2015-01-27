#!/usr/bin/python3

import os, sys
bindir = os.path.abspath(os.path.dirname(sys.argv[0]))
libdir = bindir + "/../lib"
sys.path.append(libdir)

import logging

import lacuna
import lacuna.exceptions as err
import lacuna.binutils.libtrain_spies as lib

ts = lib.TrainSpies()
l  = ts.client.user_logger

for p in ts.planets:
    ### Set the current planet
    ts.set_planet( p )
    l.info( "Working on {}.".format(ts.planet.name) )

    ### Get that planet's Int Min.  Skip to the next planet if there's no int 
    ### min.
    l.info( "Finding Int Min and locating spies on {}.".format(ts.planet.name) )
    try:
        ts.set_intmin()
        l.debug( "Got an int min on {}.".format(ts.planet.name) )
    except err.NoSuchBuildingError as e:
        l.info( "You don't have an Intelligence Ministry on {}.  Skipping.".format(ts.planet.name) )
        continue

    ### Do eet.
    for pname, loc in ts.locations.items():
        if loc:
            ts.train_spies_at( pname, loc )
        else:
            l.info( "Any training buildings you have on {} are currently full.".format(pname) )

