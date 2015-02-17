#!/usr/bin/python3

import os, sys
bindir = os.path.abspath(os.path.dirname(sys.argv[0]))
libdir = bindir + "/../lib"
sys.path.append(libdir)

import logging

import lacuna
import lacuna.binutils.libstations_report as lib

sr  = lib.StationsReport()
l   = sr.client.user_logger

### sr.planets will be a list, containing either just the planet name passed 
### in by the user, or all of the user's planet names if 'all' was passed in.
for sname in sorted(sr.stations):

    ### Set the current planet name as our 'working' planet
    sr.set_station( sname )

    ### Display reports on stations with low resource income.  Stations with 
    ### all 4 resources in positive hourly produce no output at all.
    #sr.show_low_res( )

    sr.show_all( )


