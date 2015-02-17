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

num = 0
for sname in sorted(sr.stations):
    sr.set_station( sname )
    num += sr.run_report()
print( "Reported on {} total stations.".format(num) )

