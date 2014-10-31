
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
#view = int.view()
#print( "We have {} of a max {} spies, and {} are in training, which takes {} seconds."
#    .format(view.current, view.maximum, view.in_training, view.training_costs['time'])
#)


### View spies' details, paginated
### 
#spies = int.view_spies( 2 )       # look at spies on page 2
#spy = spies[0]
#print( "Your first spy is based from {}, assigned to {}, and is doing task {}."
#    .format( spy.based_from.name, spy.assigned_to.name, spy.assignment)
#)


### View all spies' details, non-paginated
### 
#spies = int.view_all_spies()
#spy = spies[0]
#print( "Your first spy is based from {}, assigned to {}, and is doing task {}."
#    .format( spy.based_from.name, spy.assigned_to.name, spy.assignment)
#)


### Burn a spy
### 
#spies = int.view_all_spies()
#last_spy = spies[-1]
#int.burn_spy( last_spy.id )
#print("Spy", last_spy.name, "has been burned.")


### Train a new spy to replace the burned one
### 
#rv = int.train_spy( )
#print( rv['trained'], "new spies are being trained." )


### Subsidize that training
### 
#int.subsidize_training( )
#print( "Spy training has been subsidized" )


### Rename the last spy in the list
### 
#spies = int.view_all_spies()
#int.name_spy( spies[-1].id, "FlurbleBlargle" )


### Assign a spy to a task
### Assigns to the last spy in the list.  He should be available if you 
### followed the rest of the tests in here; we just trained him and subsidized 
### his training.  Change the "-1" subscript as needed if your last spy is not 
### available.
#spies = int.view_all_spies()
#spy, result = int.assign_spy( spies[-1].id, 'Counter Espionage'  )
#print( "The result of assigning spy {} to mission {} was {} because {}."
#    .format(spy.name, spy.assignment, result.result, result.reason )
#)


### So we can see all prompts for captchas on subsequent runs.
glc.logout()
