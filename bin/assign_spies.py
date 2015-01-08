#!/usr/bin/python3


### 1.7 is getting "no usable spies" on a counter 20 topoff, but everybody is 
###   home.  Probably just need to tweak the message, but find out what's 
###   happening.
###
### 1.7 (3)
###
###
### Others with "no usable":
###     2.1, 2.2, 2.4, 2.6, 2.7 (1)

import os, sys
bindir = os.path.abspath(os.path.dirname(sys.argv[0]))
libdir = bindir + "/../lib"
sys.path.append(libdir)

import logging

import lacuna
import lacuna.exceptions as err
import lacuna.binutils.libassign_spies as lib

ass = lib.AssignSpies()             # tee-hee
l   = ass.client.user_logger

for p in ass.planets:
    ### Set the current planet
    ass.set_planet( p )
    l.info( "Working on {}.".format(ass.planet.name) )

    ### If we were asked to topoff to a specific number, either figure out how 
    ### many more we need to assign to reach that number, or bail on this 
    ### planet if we're over that number.
    l.debug( "Checking on how many spies are running {} on {}.".format(ass.args.task, ass.on) )
    try:
        ass.check_topoff()
    except err.TopoffError as e:
        l.info( "You already have {} spies on this task.  Skipping.".format(e.number) )
        continue

    ### Find the spies located on the requested planet
    l.debug( "Setting only spies located on {}.".format(ass.on) )
    try:
        ass.set_spies_on_target()
    except err.NoUsableSpiesError as e:
        l.info( "You have no spies located on {}.  Skipping.".format(ass.on) )
        continue

    ### Set only the spies who are able to run the requested target task
    l.debug( "Setting only spies who are able to run {}.".format(ass.args.task) )
    try:
        ass.set_able_spies()
    except err.NoUsableSpiesError as e:
        l.info( "You have no spies able to run {} on {}.  Skipping.".format(ass.args.task, ass.on) )
        continue

    ### Set only the spies who are currently doing the requested current task
    l.debug( "Setting only spies who are current performing the {} task.".format(ass.args.doing) )
    try:
        ass.set_spies_doing_correct_task()
    except err.NoUsableSpiesError as e:
        l.info( "You have no spies currently set to {} on {}.  Skipping.".format(ass.args.doing, ass.on) )
        continue

    ### We might still have more spies available than the user requested.  Set 
    ### only the spies with the best of whatever attribute was requested.
    l.debug( "Finding just the spies with the highest {}.".format(ass.args.top) )
    ass.set_best_spies()
    if not ass.spies:
        l.info( "4 You have no usable spies on {}.  Skipping.".format(ass.on) )
        continue

    ### Do eet.
    l.debug( "Assigning spies on {} to {}.".format(p, ass.args.task) )
    count = ass.assign_spies()
    l.info( "{} spies from {} have been assigned to {}.".format(count, p, ass.get_task(ass.args.task)) )

