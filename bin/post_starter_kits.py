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
trade_id = sk.post_kit()

l.info( "Your kit was posted; the trade ID is {}.".format(trade_id) )

"""

All of the named kits have been tested:
    res
    stor
    mil
    ute
    beach
    deco
    full
    big

You can set the price with or without quotes - tested both of these:
    py bin/post_starter_kits.py bmots01 --price "2.2" beach
    py bin/post_starter_kits.py bmots01 --price 2.2 beach

"""

