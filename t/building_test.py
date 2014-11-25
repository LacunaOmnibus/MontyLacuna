
import pprint
pp = pprint.PrettyPrinter( indent = 4 )
import re
import threading
import timeit

import os, sys
bindir = os.path.abspath(os.path.dirname(__file__))
libdir = bindir + "/../lib"
sys.path.append(libdir)

import lacuna as lac

glc = lac.clients.Member(
    config_file = bindir + "/../etc/lacuna.cfg",
    config_section = 'play_test',
)
my_planet = glc.get_body_byname( 'bmots support 01' )



### Finding a building (the hard way)
#list_buildings(my_planet)  # I deleted this function; see body_test.py if you really want it back.
#quit()
### ...read the output, find the building you want, copy its ID, then:
#sp = my_planet.get_building_id( 'spaceport', <ID from copy above> )
#print( sp.image )


### Finding a building by coords (easy)
### 
#sp = my_planet.get_building_coords( 1, -3 )
#print( sp.image )


### Finding a building by building type (also easy)
### just remember this returns a list.
### 
sp = my_planet.get_buildings_bytype( 'spaceport', 0, 1 )[0]
print( sp.image )


### Build new
### Make sure to set the coords (args to build()) to an available plot.
###
#sp = my_planet.get_new_building( 'spaceport' )
#sp.build(5, -2)
#print( "My new spaceport started building on {} and will finish on {}, which will take {} seconds."
#    .format(sp.pending_build.start, sp.pending_build.end, sp.pending_build.seconds)
#)
### 
### This is a little wordy, but you've also got access to the start/end times 
### as datetime objects, and the build duration as a lacuna.bc.ElapsedTime 
### object:
#print( "My new spaceport will finish on {}-{}-{}.  That's {} days, {} hours, {} minutes, and {} seconds."
#    .format(
#        sp.pending_build.end_dt.year, 
#        sp.pending_build.end_dt.month, 
#        sp.pending_build.end_dt.day, 
#        sp.pending_build.seconds_el.days, 
#        sp.pending_build.seconds_el.hours, 
#        sp.pending_build.seconds_el.minutes, 
#        sp.pending_build.seconds_el.seconds, 
#    )
#)


### Demolish
### CAREFUL WITH UNCOMMENTING THIS
### Run the "Build new" block above first, then copy the building ID from its 
### output and paste it as the second arg to get_building_id() below.
#sp = my_planet.get_building_id( 'spaceport', 4734912 )
#print( "Before demo:", sp.id )
#sp.demolish()
### This would throw an AttributeError - the id no longer exists after 
### demolition (this is as it should be).
###     print( "After demo:", sp.id )

### Upgrade
### 
### This method had to be renamed to do_upgrade.  See the comments in 
### building.py - search for "do_" in there, and make sure to document this 
### behavior somewhere more reasonable.
###
### Otherwise, this works.
#sp = my_planet.get_building_coords( 1, -3 )
#sp.do_upgrade()


### Downgrade
###
### This method had to be renamed with the "^do_" the same way and for the 
### same reason as upgrade.  Again, go make with the documentation.
###
### Again, this otherwise works.  BE CAREFUL WITH TESTING THIS PLEASE
#sp = my_planet.get_building_coords( 2, -3 )
#sp.do_downgrade()

### Get stats for level
#sp = my_planet.get_building_coords( 2, -3 )
#rv = sp.get_stats_for_level(16)
#pp.pprint( rv['building'] )

### Repair
### To test this, I demoed the citadel on one of my planets on PT and then 
### snarked myself.  I also needed to copy buildings/spaceport.py and make a 
### new buildings module representing the buildings to fix, as well as add 
### that new building module to buildings/__init__.py (or the eval in 
### get_building_coords would blow up).
#test = lac.clients.Member(
#    config_file = bindir + "/../etc/lacuna.cfg",
#    config_section = 'play_test',
#)
#my_planet = test.get_body_byname( 'bmots support 01' )
#sp = my_planet.get_building_coords( -3, 0 )
#pp.pprint( sp.repair_costs )
#rv = sp.repair()

