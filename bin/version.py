#!/usr/bin/python3

import os, sys, zipfile
libdir  = os.path.abspath(os.path.dirname(sys.argv[0])) + "/../lib"
sys.path.append(libdir)

import lacuna
print( "You are using MontyLacuna version {}.".format(lacuna.version) )
