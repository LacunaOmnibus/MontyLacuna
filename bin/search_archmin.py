#!/usr/bin/python3

import os, sys
bindir = os.path.abspath(os.path.dirname(sys.argv[0]))
libdir = bindir + "/../lib"
sys.path.append(libdir)

import logging

import lacuna
import lacuna.binutils.libsearch_archmin as lib
import lacuna.exceptions as err

sa  = lib.SearchArchmin()
l   = sa.client.user_logger

for pname in sa.planets:

    ### Set the current planet name as our 'working' planet.  Grab the ArchMin 
    ### and PCC while we're at it.
    l.info( "Setting {} as the working planet.".format(pname) )
    try:
        sa.set_planet( pname )
    except(  err.NoSuchBuildingError, err.WorkingError ) as e:
        l.warning( e )
        continue

    l.info( "Making sure we have enough ore to perform a search on {}.".format(pname) )
    try:
        sa.validate_ore()
    except err.InsufficientResourceError as e:
        l.warning( e )
        continue

    ### Doo eet.
    l.info( "Starting a search for {} on {}.".format(sa.ore_to_search, pname) )
    sa.search_for_glyph()


