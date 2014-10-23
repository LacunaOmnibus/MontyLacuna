
import os, sys
bindir = os.path.abspath(os.path.dirname(__file__))
libdir = bindir + "/../../lib"
sys.path.append(libdir)

import lacuna as lac
from lacuna.exceptions import CaptchaResponseError

glc = lac.clients.Member(
    config_file = bindir + "/../../etc/lacuna.cfg",
    #config_section = 'my_sitter',
    config_section = 'play_test',
)
my_planet   = glc.get_body_byname( 'bmots rof 2.1' )
int         = my_planet.get_building_coords( -5, -2 )


### Show building status
### 
#rva = int.view()
#glc.pp.pprint( rva['spies'] )


### View spies' details, paginated
### 
#rvb = int.view_spies( 2 )       # look at spies on page 2
#glc.pp.pprint( rvb['spies'] )


### View all spies' details, non-paginated
### 
#rvc = int.view_all spies()
#glc.pp.pprint( rvc['spies'] )


### Burn a spy
### CAREFUL WITH THIS - will burn the last spy listed.
#rvd = int.view_all_spies()
#last_spy = rvd['spies'][-1]
#rvd = int.burn_spy( last_spy['id'] )
#print("Spy", last_spy['name'], "has been burned.")


### Train a new spy to replace the burned one
### 
#rve = int.train_spy( )
#del( rve['status'] )
#glc.pp.pprint( rve )


### Subsidize that training
### CAREFUL WITH THIS - it will spend 1 E per spy in the queue
#rvf = int.subsidize_training( )
#glc.pp.pprint( rvf )


### Rename the last spy in the list
### 
#rvg = int.view_all_spies()
#int.name_spy( rvg['spies'][-1]['id'], "FlurbleBlargle" )


### Assign a spy to a task
### Assigns to the last spy in the list.  He should be available if you 
### followed the rest of the tests in here; we just trained him and subsidized 
### his training.  Change the "-1" subscript as needed if your last spy is not 
### available.
#rvh = int.view_all_spies()
#rvi = int.assign_spy( rvh['spies'][-1]['id'], 'Counter Espionage'  )
#glc.pp.pprint( rvi['mission'] )

