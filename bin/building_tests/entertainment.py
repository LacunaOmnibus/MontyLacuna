
import os, sys
bindir = os.path.abspath(os.path.dirname(__file__))
libdir = bindir + "/../../lib"
sys.path.append(libdir)

import lacuna as lac
from lacuna.exceptions import CaptchaResponseError

glc = lac.clients.Member(
    config_file = bindir + "/../../etc/lacuna.cfg",
    config_section = 'my_sitter',
)
my_planet   = glc.get_body_byname( 'bmots rof 2.4' )
ent         = my_planet.get_building_coords( -2, -5 )


### Quack!
###
print( "There have been", ent.view()['ducks_quacked'], "ducks quacked." )
for i in range(0,5):
    print( ent.duck_quack() )
    print("------------")
print( "There have now been", ent.view()['ducks_quacked'], "ducks quacked." )



### Get lottery options (requires captcha)
### 

### You can get away with just this:
#rva = ent.get_lottery_voting_options()
#glc.pp.pprint( rva['options'] )

### ...however, if the user enters the captcha incorrectly, you'll get a 
### pretty ugly trace with three exceptions, so you're better off checking for 
### yourself:
try:
    rva = ent.get_lottery_voting_options()
except CaptchaResponseError as e:
    print("Your captcha was incorrect.")
    quit()
for mydict in rva['options']:
    print( "Name:", mydict['name'] )
    print( "URL:", mydict['url'] )
    print("------------")






