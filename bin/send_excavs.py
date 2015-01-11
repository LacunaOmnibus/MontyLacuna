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

### planets is a list.  Either it's just the planet name the user passed, or 
### it's a list of all of our planets if they passed in 'all'.
for pname in send.planets:
    ### Set the current planet name as our 'working' planet
    send.set_planet( pname )

    ### Send 'em
    cnt = 0
    while send.num_excavs > 0:
        stars = send.get_map_square()
        cnt += send.send_excavs_to_bodies_orbiting( stars )
    l.info( "{} sent out {} excavators.".format(send.planet.name, cnt) )


"""
All versions work.
    python bin/send_excavs.py -tp35 -v --max_ring 3 bmots01
    python bin/send_excavs.py -t p35 --max_ring 3 bmots01
    python bin/send_excavs.py --t p35 --max_ring 3 bmots01
"""

