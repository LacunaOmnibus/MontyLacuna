#!/usr/bin/python3

import os, sys
bindir = os.path.abspath(os.path.dirname(sys.argv[0]))
libdir = bindir + "/../lib"
sys.path.append(libdir)

import logging
import lacuna, lacuna.exceptions
import lacuna.binutils.libtest_script as lib

test    = lib.TestScript()
l       = test.client.user_logger


print( test.client.config['sitter']['password'] )
quit()

l.info( "Following are some details about your empire." )
pro = test.client.empire.view_profile()
l.info( "You have {} messages in your inbox, and a total of {} colonies.  Your email is '{}'"
    .format(test.client.empire.has_new_messages, len(test.client.empire.colonies), pro.email)
)
l.info( "Congratulations!  You're all set." )

