#!/usr/bin/python3

import os, sys
bindir = os.path.abspath(os.path.dirname(sys.argv[0]))
libdir = bindir + "/../lib"
sys.path.append(libdir)

import logging, lacuna
import lacuna.exceptions as err
import lacuna.binutils.libabbrv as lib

da  = lib.DelBodyAbbrv()
ute = lacuna.utils.Utils()

ute.mytry( da.abbrv.delete, da.args.name )
print( "The abbreviation for {} has been removed.".format(da.args.name) )

