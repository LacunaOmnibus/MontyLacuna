#!/usr/bin/python3

import os, subprocess, sys
bindir = os.path.abspath(os.path.dirname(sys.argv[0]))
libdir = bindir + "/../lib"
sys.path.append(libdir)

import logging

import lacuna
import lacuna.binutils.libtopoff_ships_all as lib

to      = lib.TopoffShips()
l       = to.client.user_logger
py      = sys.executable
build   = os.path.abspath(os.path.dirname(__file__)) + '/build_ships.py'

my_colonies = to.client.empire.colony_names.keys()
for i in my_colonies:
    command = [
        py, 
        build, 
        '--file',
        to.args.config_file,
        '--section',
        to.args.config_section,
        '--topoff', 
        '--level', 
        str(to.args.min_lvl), 
        '--num', 
        str(to.args.num), 
        i,
        to.args.type, 
    ]
    l.debug( "{}".format( ' '.join(command)) )
    subprocess.call( command )

