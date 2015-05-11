#!/usr/bin/python3

import os, sys
bindir = os.path.abspath(os.path.dirname(sys.argv[0]))
libdir = bindir + "/../lib"
sys.path.append(libdir)

import logging, lacuna
import lacuna.exceptions as err
import lacuna.binutils.libabbrv as lib

sa = lib.SetBodyAbbrv()

sa.abbrv.save( sa.args.name, sa.args.abbrv )
print( "{} can now be abbreviated as '{}'.".format(sa.args.name, sa.args.abbrv) )

