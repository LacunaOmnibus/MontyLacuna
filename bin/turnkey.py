#!/usr/bin/python3


import os, sys
bindir = os.path.abspath(os.path.dirname(sys.argv[0]))
libdir = bindir + "/../lib"
sys.path.append(libdir)

import logging

import lacuna
import lacuna.exceptions as err
import lacuna.binutils.libturnkey as lib

tk = lib.Turnkey()
l  = tk.client.user_logger

tk.perform_chosen_task()
quit()

### Do eet.
l.debug( "Assigning spies on {} to {}.".format(p, tk.args.task) )
count = tk.tk()
l.info( "{} spies from {} have been tk to {}.".format(count, p, tk.task) )

