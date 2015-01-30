MontyLacuna
===========

A Python Client for The Lacuna Expanse.


This is essentially a port of the Perl Games::Lacuna::Client module to Python.  

## bugsquish
The latest run of build_ships.py got me this (topping off 20 excavs per 
planet):

[2015-01-29 23:52:58] (USER) (INFO) - bmots rof 2.1 has 8 shipyards of the correct level.
Traceback (most recent call last):
  File "bin/build_ships.py", line 34, in <module>
    num_to_build = bs.determine_buildable( shipyards )
  File "/home/jon/work/MontyLacuna/bin/../lib/lacuna/binutils/libbuild_ships.py", line 84, in determine_buildable
    raise KeyError("You don't have any docks available to hold more ships.")
KeyError: "You don't have any docks available to hold more ships."


train_spies.py
    Have them do a complex sort on whatever the user asked for and level as the secondary 
    critera.

## TBD
- Test the log rotation on Windows.  jof had a failure that he said he solved by manually 
  clearing out his logfile, so it sounds like the rotation is broken.
- Ack through everything for "CHECK" and fix.
  - Even if you find no CHECK marks, leave this list item here.  I have a tendency to 
    re-add these marks.

