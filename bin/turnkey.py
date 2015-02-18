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

#l.info( "{} spies from {} have been tk to {}.".format(count, p, tk.task) )

