
Build Ships
===========

Builds ships at multiple shipyards on a given planet.

The easiest way to run it will fill all of the available build queues on all 
of the shipyards on your planet::

    >>> python bin/build_ships.py Earth sweeper

To only build ships on shipyards of level 30::

    >>> python bin/build_ships.py --level 30 Earth sweeper

To only build 60 total ships on shipyards of level 30::

    >>> python bin/build_ships.py --num 60 --level 30 Earth sweeper

If you want to run this from a scheduled task, or a batch file/shell script, 
or any other situation where you don't want to see the script's running 
commentary, you can tell it to shut up::

    >>> python bin/build_ships.py --quiet --num 60 --level 30 Earth sweeper

For complete help, see the script's help documentation:

    >>> python bin/build_ships.py -h

