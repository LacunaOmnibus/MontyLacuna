#!/usr/bin/python3

import os, sys
bindir = os.path.abspath(os.path.dirname(sys.argv[0]))
libdir = bindir + "/../lib"
sys.path.append(libdir)

import logging

import lacuna
import lacuna.exceptions as err
import lacuna.binutils.libexcavs_report as lib

er  = lib.ExcavsReport()
l   = er.client.user_logger

for pname in er.planets:
    try:
        er.set_planet( pname )
    except err.NoSuchBuildingError as e:
        l.info( "{} does not have a working Archaeology Ministry.  Skipping.".format(er.planet.name) )
        continue

    l.info( "Gathering excavator data on {}.".format(er.planet.name) )
    er.gather_excavator_data()

er.show_report()


