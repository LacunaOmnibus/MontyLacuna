#!/usr/bin/python3

import os, sys
bindir = os.path.abspath(os.path.dirname(sys.argv[0]))
libdir = bindir + "/../lib"
sys.path.append(libdir)

import logging, lacuna
import lacuna.exceptions as err
import lacuna.binutils.libabbrv as lib

sa = lib.ShowBodyAbbrv()

sa.abbrv.show( sa.args.name )

