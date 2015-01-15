
.. _build_ships:

Build Ships
===========

Builds or tops off ships at multiple shipyards on a given planet, or on all of 
your planets at once.

The name of the ship to be built must be translatable by 
:meth:`lacuna.types.Translator.translate_shiptype`.  This means that most 
common names will work.

When passing the name of a planet, remember to use double quotes around the 
name if there are any space in it.  And if you want to build the same number 
of ships on all of your planets, you can pass in the special planet name 
'all'.  (If you have a planet actually named 'all', you chose poorly.  Go 
rename it, or accept that this won't work properly for that planet.)

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

When topping off excavators, you may well want to just top them off at all of 
your planets in one shot::

    >>> python bin/build_ships.py --num 20 --level 30 --topoff all excavator

If you want to run this from a scheduled task, or a batch file/shell script, 
or any other situation where you don't want to see the script's running 
commentary, you can tell it to shut up::

    >>> python bin/build_ships.py --quiet --num 60 --level 30 Earth sweeper

For complete help, see the script's help documentation:

    >>> python bin/build_ships.py -h

.. autoclass:: lacuna.binutils.libbuild_ships.BuildShips
   :members:
   :show-inheritance:

