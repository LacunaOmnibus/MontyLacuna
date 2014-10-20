
import os
import sys
import pprint, re

bindir = os.path.abspath(os.path.dirname(__file__))
libdir = bindir + "/../lib"
sys.path.append(libdir)

import lacuna as lac
pp = pprint.PrettyPrinter( indent = 4 )

glc = lac.clients.Member(
    config_file = bindir + "/../etc/lacuna.cfg",
    config_section = 'my_sitter',
)

mail = glc.get_inbox();

msgs = mail.view_inbox( {"tags": "excavator"} )
pp.pprint( msgs['message_count'] )
pp.pprint( msgs['messages'][0:3] )


### Work as expected.  Make sure trash and archived have some parl messages 
### for this to work as-is.
#msgs = mail.view_archived( {"tags": "parliament"} )
#msgs = mail.view_trashed( {"tags": "parliament"} )
#msgs = mail.view_sent( {"tags": "parliament"} )
#pp.pprint( msgs['message_count'] )


### Works, but the sample message ID won't exist anymore.  Grab one at random 
### out of the output of view_inbox() above.
#msg = mail.read_message( 68029602 )
#pp.pprint( msg['message'] )


### Same as before - this works, but you'll need new message IDs to test in 
### the future.
### The before/after displays of message_count show that the number of inbox 
### messages has dropped.
#msgs = mail.view_inbox( {"tags": "parliament"} )
#pp.pprint( msgs['message_count'] )
#msg = mail.archive_messages( [68029602, 68029554, 68029504] )
#msgs = mail.view_inbox( {"tags": "parliament"} )
#pp.pprint( msgs['message_count'] )


### Works.
#rv = mail.send_message(
#    'tmtowtdi,tmt_testing,no_such_player',
#    'python test',
#    'This is a test of the python message system.'
#)
#pp.pprint( rv['message'] )
#

