#!/usr/bin/python3

###
### There are some CHECK s to be dealt with in the lib.
### 

import logging, os, sys
bindir = os.path.abspath(os.path.dirname(sys.argv[0]))
libdir = bindir + "/../lib"
sys.path.append(libdir)

import lacuna
import lacuna.binutils.libsend_excavs as lib

### Get library class instance
send = lib.SendExcavs()

### Get logger
l = send.client.user_logger

### Figure out how many excavs we need to send
send.get_excav_count()

### Fire the BFG at Norway.
###
### No, just kidding.  This sends excavs!
send.send_excavs()

"""
python bin/send_excavs.py --t p35 --max_ring 3 bmots01
"""


