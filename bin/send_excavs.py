#!/usr/bin/python3

import logging, os, sys
bindir = os.path.abspath(os.path.dirname(sys.argv[0]))
libdir = bindir + "/../lib"
sys.path.append(libdir)

import lacuna
import binutils.libsend_excavs as lib

### Get library class instance
send = lib.SendExcavs()

### Get logger
l = send.client.user_logger

### Turn on caching
send.client.cache_on("my_planets", 3600)

### Get planet
planet = send.client.get_body_byname( send.args.name )

### Figure out how many excavs we need to send
###     The lowest of
###         How many available slots are there in the arch min
###         How many do we have built
###
###     Bail if either of those numbers is zero.
excavs_to_send = send.get_excav_count( planet )

### Get starmap
map = send.client.get_map()

### Get my alliance
my_alliance = send.client.get_my_alliance()




ring_offset = 1
cell = 1
while excavs_to_send > 0:
    stars = send.get_map_square(map, planet, ring_offset, cell )
    for s in stars:
        print( "Bodies orbiting {}:".format(s.name) )
        for b in s.bodies:
            if b.type == 'habitable planet':
                l.debug( "{} has surface type {}.".format(b.name, b.surface_type) )
    quit()



### AFAICT, we're working to here.  See libsend_excavs for graphical 
### explanation of ring_offset and cell.




### While number of excavs to send > 0:
###     - Get square of space
###         - first one is special.  Usually, we'll have (ring_offset * 8) 
###           cells, but if ring_offset is 0, we do need to get that one 
###           center cell.
###
###     - Iterate stars in that area of space
###         - Check if owned by an SS
###             - If so, check the laws on that SS.  If members only excav is 
###               on, and if the SS is not owned by my alliance, Record this 
###               SS in a "no good" dict and skip to next star
###         - Iterate planets around the star
###             - If planet is uninhabited, habitable, correct type and has no 
###               excavators from us, save planet ID in list.  Decrement count 
###               of excavs to send.  If <= 0, bail star iteration loop.
###
###     - If count of excavs to be sent is <= 0
###         - break while loop
###
###     - cell += 1
###         - if cell > (8 * ring_offset)
###             - ring_offset += 1
###             - cell = 1

