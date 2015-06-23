#!/usr/bin/python3

import os, sys
bindir = os.path.abspath(os.path.dirname(sys.argv[0]))
libdir = bindir + "/../lib"
sys.path.append(libdir)

import logging

import lacuna
import lacuna.binutils.liballow_friendly_bhg as lib
import lacuna.exceptions as err

af  = lib.AllowFriendlyBHG()
l   = af.client.user_logger

### Set station and parl based on the command-line station name
try:
    af.set_station()
except err.NoSuchBuildingError as e:
    l.error( "This station doesn't have a working Parliament at level 28 or higher." )
    quit()

### Get ally id based on the command-line friendly alliance name
friendly_ally_id = af.get_ally_id()
if not friendly_ally_id:
    l.info( "We either found no alliances or more than one alliance matching the requested name." )
    quit()

### Let 'em through.
af.allow_bhg_usage( friendly_ally_id )

l.info("The proposition has been issued.  It will become a law after it gets voted through.")

