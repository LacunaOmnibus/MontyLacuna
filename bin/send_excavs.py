#!/usr/bin/python3

import logging, os, sys
bindir = os.path.abspath(os.path.dirname(sys.argv[0]))
libdir = bindir + "/../lib"
sys.path.append(libdir)

import lacuna
import lacuna.binutils.libsend_excavs as lib

send = lib.SendExcavs()
l = send.client.user_logger

for pname in sorted(send.planets):
    send.set_planet( pname )

    ### Send 'em
    cnt = 0
    while send.num_excavs > 0:
        stars = send.get_map_square()
        if not stars:
            l.info( "No stars found in this map square." )
            continue
        cnt += send.send_excavs_to_bodies_orbiting( stars )
    l.info( "{} sent out {} excavators.".format(send.planet.name, cnt) )

