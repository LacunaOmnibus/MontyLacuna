#!/usr/bin/python3

import os, sys
bindir = os.path.abspath(os.path.dirname(sys.argv[0]))
libdir = bindir + "/../lib"
sys.path.append(libdir)

import logging
import lacuna, lacuna.exceptions
import binutils.libtest_script as lib


test    = lib.TestScript()
client  = test.connect()
l       = client.user_logger
client.user_log_stream_handler.setLevel(logging.INFO)


l.info( "Following are some details about your empire." )
pro = client.empire.view_profile()
l.info( "You are from {} in {}, and your player name is {}."
    .format(pro.city, pro.country, pro.player_name)
)
l.info( "Congratulations!  You're all set." )

