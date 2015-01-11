
import os
import sys
import pprint
pp = pprint.PrettyPrinter( indent = 4 )
import re

bindir = os.path.abspath(os.path.dirname(sys.argv[0]))
libdir = bindir + "/../lib"
sys.path.append(libdir)

import lacuna as lac
from lacuna.exceptions import CaptchaResponseError


glc = lac.clients.Member(
    config_file = bindir + "/../etc/lacuna.cfg",
    config_section = 'my_sitter',
)


### You don't normally need to do this - if a method requires a captcha, it'll 
### prompt you when it gets called.
###
### However, if you're doing something where timing matters, you might want to 
### run something like this beforehand.  It'll prompt you for a captcha, which 
### you can solve, and then your current session will be marked as having 
### solved a captcha.  You then have 30 minutes to run your time-sensitive 
### script without it having to prompt you for a captcha.


cap = glc.get_captcha()

p = cap.fetch()
print( "Puzzle is located at {}.  Guid is {}.".format(p.url, p.guid) )

quit()



### Display the captcha in a browser
###
cap.showit()

### Prompt the user for their response
###
cap.prompt_user()

### Send the response to the server and see if it was correct or not
###
try:
    cap.solveit()
    print("Yay your solution was correct!")
except CaptchaResponseError as e:
    print("Boo you messed something up - captcha no good.")
    

