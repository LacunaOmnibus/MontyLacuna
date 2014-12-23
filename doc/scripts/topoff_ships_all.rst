
.. _topoff_ships_all:

Topoff Ships on All Planets
===========================

Makes sure you have a minimum number of a certain type of ship at all of your 
planets.  

While this is most often used to ensure you have excavators lying around, you 
can use it for any ship type that you want to always have a minimum of in 
stock -- maybe you like having 2 supply pods, or 10 smugglers, or 30 scows, or 
whatever, on all of your planets.  This will do the job.

This actually calls :ref:`build_ships` with the --topoff argument, once for 
each of your planets.

To make sure each planet has at least 20 excavators in stock:

    >>> python bin/topoff_ships_all.py excavator 20 

To only build ships on shipyards of level 30::

    >>> python bin/topoff_ships_all.py --level 30 excavator 20

For complete help, see the script's help documentation:

    >>> python bin/topoff_ships_all.py -h

