#!/usr/bin/python3

import logging, os, sys
bindir = os.path.abspath(os.path.dirname(sys.argv[0]))
libdir = bindir + "/../lib"
sys.path.append(libdir)

import lacuna
import lacuna.binutils.libshow_laws as lib

### Get library class instance
sl = lib.ShowLaws()

### Display the report
sl.show_laws_report()

