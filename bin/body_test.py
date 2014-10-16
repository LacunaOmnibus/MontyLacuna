
import os
import sys
import pprint
pp = pprint.PrettyPrinter( indent = 4 )
import re
import threading
import timeit

bindir = os.path.abspath(os.path.dirname(__file__))
libdir = bindir + "/../lib"
sys.path.append(libdir)

import lacuna as lac


glc = lac.users.Member(
    config_file = bindir + "/../etc/lacuna.cfg",
    config_section = 'my_sitter',
)

supp01 = glc.get_body(82651)



### Just a couple utility functions I found useful while creating this test 
### script.
def list_bodies(glc):
    for id, name in glc.empire.planets.items():
        if re.match('^\wASS', name):
            continue
        print( "{} has an id of {}".format(name, id) )

def list_buildings(body):
    pp.pprint( body.buildings_id )

#list_bodies(glc)
#quit()

#list_buildings(supp01)
#quit()




### Repair
#building_ids = []
#for i in supp01.buildings_name['Shield Against Weapons']:
#    building_ids.append( i['id'] )
#rv = supp01.repair_list( building_ids )
#pp.pprint( rv )


### Rearrange
### DevMin on support 01 ID is 4294596.
move_to = [{
    ### dev min, this move is legal.
    'id': 4294596,
    'x':  0,
    'y': 1
}]   
#### this is the DevMin's original loc.
move_back = [{
    'id': 4294596,
    'x':  -1,
    'y': 0
}]
### If you test this, running it with move_to, please remember to run it with 
### move_back afterwards.
#rv = supp01.rearrange_buildings( move_to )
#rv = supp01.rearrange_buildings( move_back )
#pp.pprint( rv['moved'] )


### Get buildable list
#rv = supp01.get_buildable( 0, 0 )                  # illegal - can't build on the center plot
#rv = supp01.get_buildable( 0, 1 )                  # legal, returns all
#rv = supp01.get_buildable( 0, 1, 'Water' )         # legal, returns all with the Water tag
#rv = supp01.get_buildable( 0, 1, 'Blargle' )       # legal, but returns nothing
#pp.pprint( rv['buildable'] )


### Rename
#rv = supp01.rename( 'bmots support 01' )
#rv = supp01.rename( 'bmots support 01111' )
#pp.pprint( rv )


### Abandon
### DO NOT TEST THIS UNLESS YOU'RE 100% SURE YOU'RE LOGGED IN WITH A TEST 
### ACCOUNT.
# test_planet_id = integer ID of planet you don't mind losing because you're testing.
#dumpme = glc.get_body( ID of a body you don't mind losing. )
#rv = dumpme.abandon()
#pp.pprint( rv )

