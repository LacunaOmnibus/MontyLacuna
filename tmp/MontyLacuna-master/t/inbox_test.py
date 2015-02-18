
import os
import sys
import pprint, re

bindir = os.path.abspath(os.path.dirname(sys.argv[0]))
libdir = bindir + "/../lib"
sys.path.append(libdir)

import lacuna as lac
pp = pprint.PrettyPrinter( indent = 4 )

glc = lac.clients.Member(
    config_file = bindir + "/../etc/lacuna.cfg",
    config_section = 'sitter',
)

mail = glc.get_inbox();


### See messages in your inbox
###
#glc.debugging_method = 'view_inbox'
#msgs, ttl = mail.view_inbox( {"tags": ["excavator", "correspondence"]} )
#print( "There are {:,} excavator/correspondence messages in my inbox.  Here are the first few:"
#    .format(ttl)
#)
#for i in msgs[0:3]:
#    print( "{} from {} (preview: {})".format(i.subject, i.from_name, i.body_preview) )
#    print( "The full body of the message follows:" )
#    print( mail.read_message( i.id ).body )
#    print( "----------------------" )


### See messages in one of the mailbox's sub-tabs
### 
#msgs, ttl = mail.view_trashed()
#msgs, ttl = mail.view_sent()
#msgs, ttl = mail.view_archived()
#print( "There are", ttl, "messages in this tab.  Here are the first few:")
#for i in msgs[0:3]:
#    print( "\t{} from {} (preview: {})".format(i.subject, i.from_name, i.body_preview) )


### Archive the first two excavator messages in your inbox.
### 
#msgs, ttl = mail.view_inbox( {"tags": ["excavator"]} )
#msg = mail.archive_messages([ msgs[0].id, msgs[1].id ])


### Trash the next two excavator messages in your inbox.
### 
#msgs, ttl = mail.view_inbox( {"tags": ["excavator"]} )
#msg = mail.trash_messages([ msgs[0].id, msgs[1].id ])


### Send mail to one or more players.
###
#mail.send_message(
#    'tmtowtdi,no_such_player',
#    'python test',
#    'This is a test of the python message system.',
#)
