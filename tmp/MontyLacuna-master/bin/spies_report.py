#!/usr/bin/python3

import os, sys
bindir = os.path.abspath(os.path.dirname(sys.argv[0]))
libdir = bindir + "/../lib"
sys.path.append(libdir)

import logging

import lacuna
import lacuna.exceptions as err
import lacuna.binutils.libspies_report as lib

sr  = lib.SpiesReport()
l   = sr.client.user_logger

### sr.planets will be a list, containing either just the planet name passed 
### in by the user, or all of the user's planet names if 'all' was passed in.
for pname in sr.planets:

    ### Set the current planet name as our 'working' planet
    try:
        sr.set_planet( pname )
    except err.NoSuchBuildingError as e:
        l.info( "{} does not have a working Intelligence Ministry.  Skipping.".format(sr.planet.name) )
        continue

    ### Get data on spies at this planet
    l.info( "Gathering spy data on {}.".format(sr.planet.name) )
    sr.gather_spy_data()

sr.display_full_report()


