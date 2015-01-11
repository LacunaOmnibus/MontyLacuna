
Recall All Spies
================

Recall all spies based on a given planet who are currently away from the 
planet.

If you have spies out at multiple different locations, this will go to each of 
those locations and get back all of your spies.  Uses the fastest ships you 
have available that can carry spies.

All you have to specify is the name of the planets to pull spies back to::

    >>> python bin/recall_all_spies.py Earth

Warning
-------
This script can behave a little oddly if you have lots of spies on a given 
target body and you're trying to retrieve them.

Imagine that you have a space station that you feared was under attack, so you 
send all of the spies from four different planets to that space station to 
defend it.  That's 360 total spies.

When we ask the TLE API to show us the spies on that planet, it will only ever 
show us 100 spies (of our 360).  

So each planet that sent spies knows its spies are there, but when we ask for 
them to be picked up, only 100 will be listed.

This means that this retrieval script will sometimes fail to recall spies that 
you know are definitely out and about.

The best way to fix this is to go run the :ref:`spies_report` script, using 
CSV formatting.  Use your favorite spreadsheet program (Excel or whatever) to 
view the produced file, and see which of your planets have spies at the 
troubled station.  Run this retrieval script for each of those planets.  Some 
runs will succeed in retrieving spies, and some will fail, resulting in 100 of 
your 360 spies being eventually picked up and returned home.

After the ships that are picking up your first batch of spies actually get to 
the space station and remove those 100 from the station, run this retrieval 
script again to pick up the next 100.

Full Documentation
------------------
For complete help, see the script's help documentation:

    >>> python bin/recall_all_spies.py -h

.. autoclass:: lacuna.binutils.librecall_all_spies.RecallAllSpies
   :members:
   :show-inheritance:

