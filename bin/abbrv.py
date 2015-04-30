#!/usr/bin/python3


### At this point, this works, but it's still pretty rudimentary.  See the 
### comments in the library.
###
###     $ py bin/abbrv.py --do set --abbrv '1.1' "bmots rof 1.1"
###
###     $ py bin/abbrv.py --do delete "bmots rof 1.1"
###     $ py bin/abbrv.py --do delete all
###
###     $ py bin/abbrv.py --do show "bmots rof 1.1"
###     $ py bin/abbrv.py --do show all

import os, sys
bindir = os.path.abspath(os.path.dirname(sys.argv[0]))
libdir = bindir + "/../lib"
sys.path.append(libdir)

import logging, lacuna
import lacuna.exceptions as err
import lacuna.binutils.libabbrv as lib

sa = lib.SetBodyAbbrv()
l  = sa.client.user_logger






#l.info( "{} spies from {} have been tk to {}.".format(count, p, tk.task) )

