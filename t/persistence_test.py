
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

my_planet   = glc.get_body_byname( 'bmots rof 2.4' )
ent         = my_planet.get_building_coords( -2, -5 )


"""

    This calls the get_lottery_voting_options() method on your Entertainment 
    District; this method requires a captcha.

    The first time you run this script, you should be prompted for a captcha.  
    If you enter it incorrectly, you'll be prompted again the next time you 
    run this.

    However, if you enter the captcha correctly, you should be able to run 
    this again as many times as you like (RPCs allowing) in the next 30 
    minutes without being re-prompted for a captcha.  After this happens, 
    you'll be able to see your session_id in the correct section in your 
    config file.

    
    Once you've confirmed that you can run this multiple times, only being 
    prompted for the captcha the first time, uncomment the call to logout() at 
    the bottom.  This will invalidate your session_id and remove it from your 
    config file.  The next time you run this after calling logout(), you will 
    be re-prompted for a captcha.


    PLEASE remember to leave this file with glc.logout() commented.

"""

        
try:
    rva = ent.get_lottery_voting_options()
    print("The get_lottery_voting_options() call worked.  I'm not going to bother showing any output.")
except CaptchaResponseError as e:
    print("Your captcha was incorrect.")


#glc.logout()



