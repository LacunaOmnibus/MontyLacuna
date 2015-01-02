#!/usr/bin/python3

import os, sys
bindir = os.path.abspath(os.path.dirname(sys.argv[0]))
libdir = bindir + "/../lib"
sys.path.append(libdir)

import logging

import lacuna
import lacuna.binutils.libships_report as lib

sr  = lib.ShipsReport()
l   = sr.client.user_logger


### sr.planets will be a list, containing either just the planet name passed 
### in by the user, or all of the user's planet names if 'all' was passed in.
for pname in sr.planets:

    ### Set the current planet name as our 'working' planet
    sr.set_planet( pname )

    ### Get data on ships at this planet
    ### CHECK this should have caching turned on.
    l.info( "Gathering ship data on {}.".format(sr.planet.name) )
    sr.gather_ship_data()


sr.produce_report()


