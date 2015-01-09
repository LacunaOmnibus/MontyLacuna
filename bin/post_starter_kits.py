#!/usr/bin/python3

import os, sys
bindir = os.path.abspath(os.path.dirname(sys.argv[0]))
libdir = bindir + "/../lib"
sys.path.append(libdir)

import logging

import lacuna
import lacuna.exceptions as err
import lacuna.binutils.libpost_starter_kits as lib

sk  = lib.PostStarterKit()
l   = sk.client.user_logger

### Pick one, or make your own combination.
###
### Trying to come up with command-line options for every possible combination 
### of kits people might want to post is going to make both of us unhappy, so 
### the user will need to edit this script (unless I can come up with some 
### more satisfactory solution).
kit_to_post = lib.ResKit()
kit_to_post = lib.StorageKit()
kit_to_post = lib.MilitaryKit()
kit_to_post = lib.UtilityKit()
kit_to_post = lib.DecoKit()
kit_to_post = lib.ComboKit( [lib.ResKit(), lib.UtilityKit()] )
kit_to_post = lib.ComboKit( [lib.ResKit(), lib.StorageKit(), lib.UtilityKit()], 0.5 )


"""

This doesn't work yet, but it's what I'm working towards.


    - Edit this script, chose what kit_to_post you want.

    >>> py bin/post_starter_kit.py --level 2 --num 5 --price 0.3 Earth

        Post 5 instances of kit_to_post from the TM on Earth. 
        All plans contained in each kit at level 2.  
        Charge 0.3 E for each trade.

    >>> py bin/post_starter_kit.py --level 5 --sst --num 2 --price 5 Earth

        Post 2 instances of kit_to_post from the SST on Earth. 
        All plans contained in each kit at level 5.  
        Charge 5.0 E for each trade.

etc


sk.post_kits()
    - Check that we actually have enough kits of the requested levels onhand or raise exception.
    - Post the kits

"""






### this remains so we have a convenient log call lying around.
l.info( "Gathering spy data on {}.".format(sk.planet.name) )



