#!/usr/bin/python3

import os, sys
bindir = os.path.abspath(os.path.dirname(sys.argv[0]))
libdir = bindir + "/../lib"
sys.path.append(libdir)

import logging

import lacuna
import lacuna.binutils.libassign_spies as lib

ass = lib.AssignSpies()             # tee-hee
l   = ass.client.user_logger


### Find the spies assigned to the requested planet
ass.set_spies_on_target()

### Filter to get only the spies who are able to run the requested target task
ass.set_able_spies()

### Filter to get only the spies who are currently doing the requested current 
### task
ass.set_spies_doing_correct_task()

### We might still have more spies available than the user requested.  Filter 
### to get only the spies with the best of whatever attribute was requested.
ass.set_best_spies()

### Do eet.
count = ass.assign_spies()
l.info( "{} spies have been assigned to the {} task.".format(count, ass.args.task) )

