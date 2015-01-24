
.. _scuttle_ships:

Scuttle Ships
=============
Scuttles extra ships at a specific planet.

To scuttle a single smuggler ship on Earth::

    >>> python bin/scuttle_ships.py Earth smug

To scuttle 20 sweepers on Earth::

    >>> python bin/scuttle_ships.py --num 20 Earth sweeper

Scuttle By Worst Attribute
--------------------------
When we scuttle ships, we first sort them by speed and scuttle from slowest to 
fastest, so the above command would scuttle the 20 slowest sweepers.  That's 
usually fine; the 20 slowest sweepers are most likely going to also have the 
worst combat scores (which is the score you're probably most interested in 
when it comes to sweepers).

However, if you're in a situation where you really want to ensure that the 
sweepers you scuttle are the lowest combat rated::

    >>> python bin/scuttle_ships.py --num 20 --low combat Earth sweeper

        The valid choices for "--low" are:
            - combat
            - hold_size
            - max_occupants
            - speed
            - stealth

Ship Names
----------
There are a number of :ref:`ship_translations` you can use when scuttling, so 
you don't have to type out ``short_range_colony_ship`` (that'll give you a 
blister), or remember how the system refers to a Supply Pod V.

CLI Help
--------
For complete help, see the script's help documentation::

    >>> python bin/scuttle_ships.py -h

Class Documentation
-------------------
.. autoclass:: lacuna.binutils.libscuttle_ships.ScuttleShips
   :members:
   :show-inheritance:

