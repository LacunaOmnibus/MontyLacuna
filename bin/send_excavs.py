#!/usr/bin/python3

###
### There are some CHECK s to be dealt with both here and in the lib.
### 
### The code in the lib worked up to the point of getting the list of stars 
### (so the whole Cell/Ring thing was working).
### 
### At that point, I realized that I needed a Cell class, so I made one.  It 
### basically contains the code that had already been working, but of course 
### that's been sliced and moved.  It should work, but you know how that goes.
###
### Test everything.
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

### Turn on caching
send.client.cache_on("my_planets", 3600)

### Get planet
#planet = send.client.get_body_byname( send.args.name )

### Figure out how many excavs we need to send
send.get_excav_count( planet )

### Fire the BFG at Norway.
###
### No, just kidding.  This sends excavs!
send.send_excavs()



                    



### While number of excavs to send > 0:
###
###     - Iterate stars in that area of space
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

