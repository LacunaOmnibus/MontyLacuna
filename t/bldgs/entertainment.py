
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
#print( "There have been", ent.view()['ducks_quacked'], "ducks quacked." )
#for i in range(0,5):
#    print( ent.duck_quack() )
#    print("------------")
#print( "There have now been", ent.view()['ducks_quacked'], "ducks quacked." )



### Get lottery options (requires captcha)
### 

### You can get away with just this:
#options = ent.get_lottery_voting_options()
#for i in options:
#    print(i.name, "- -", i.url)

### ...however, if the user enters the captcha incorrectly, you'll get a 
### pretty ugly trace with three exceptions, so you're better off checking for 
### yourself:
try:
    options = ent.get_lottery_voting_options()
except CaptchaResponseError as e:
    print("Your captcha was incorrect.")
    quit()
for i in options:
    print(i.name, "- -", i.url)



### Force a logout so if we run this multiple times we'll get prompted for 
### captcha each time
glc.logout();

