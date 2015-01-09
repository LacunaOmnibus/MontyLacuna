#!/usr/bin/python3

import os, sys
bindir = os.path.abspath(os.path.dirname(sys.argv[0]))
libdir = bindir + "/../lib"
sys.path.append(libdir)

import lacuna
import lacuna.binutils.libpost_starter_kits as lib

sk  = lib.PostStarterKit()
l   = sk.client.user_logger

### Make sure the user has in stock the plans required by the selected kit.
l.info( "Making sure you have the plans needed for the {} kit in stock on {}.".format(sk.args.kit, sk.planet.name) )
sk.validate_plans()

### Post the kit to whichever trade building the user requested.
l.info( "Posting your kit to your {}.".format(sk.trade.name) )
sk.post_kit()

"""

This doesn't work yet, but it's what I'm working towards.

    >>> py bin/post_starter_kit.py --kit res --level 2 --num 5 --price 0.3 Earth

        Post 5 instances of ResKit from the TM on Earth. 
        All plans contained in each kit at level 2.  
        Charge 0.3 E for each trade.

    >>> py bin/post_starter_kit.py --kit storage --level 5 --sst --num 2 --price 5 Earth

        Post 2 instances of StorageKit from the SST on Earth. 
        All plans contained in each kit at level 5.  
        Charge 5.0 E for each trade.

etc
"""

