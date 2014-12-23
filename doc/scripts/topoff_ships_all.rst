
.. _topoff_ships_all:

Topoff Ships on All Planets
===========================

Makes sure you have a minimum number of a certain type of ship at all of your 
planets.  Most often used to ensure you have excavators lying around.

This actually calls :ref:`build_ships` with the --topoff argument, once for 
each of your planets.

To make sure each planet has at least 20 excavators in stock:

    >>> python bin/topoff_ships_all.py excavator 20 

To only build ships on shipyards of level 30::

    >>> python bin/topoff_ships_all.py --level 30 excavator 20

For complete help, see the script's help documentation:

    >>> python bin/topoff_ships_all.py -h

