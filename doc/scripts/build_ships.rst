
.. _build_ships:

Build Ships
===========

Builds ships at multiple shipyards on a given planet.

When passing the name of a ship, you must use the ship's "system" name.  A 
complete list can be found here: :ref:`ships_list`

The easiest way to run it will fill all of the available build queues on all 
of the shipyards on your planet::

    >>> python bin/build_ships.py Earth sweeper

To only build ships on shipyards of level 30::

    >>> python bin/build_ships.py --level 30 Earth sweeper

To only build 60 total ships on shipyards of level 30::

    >>> python bin/build_ships.py --num 60 --level 30 Earth sweeper

You can also just top off your ships, to make sure you've always got a certain 
number in stock.  The following will build however many excavators it takes to 
get to a total of 20, and will just quit if you've already got 20 or more::

    >>> python bin/build_ships.py --num 20 --level 30 --topoff Earth excavator

If you want to run this from a scheduled task, or a batch file/shell script, 
or any other situation where you don't want to see the script's running 
commentary, you can tell it to shut up::

    >>> python bin/build_ships.py --quiet --num 60 --level 30 Earth sweeper

For complete help, see the script's help documentation:

    >>> python bin/build_ships.py -h

.. autoclass:: lacuna.binutils.libbuild_ships.BuildShips
   :members:
   :show-inheritance:

