
Send Excavs
===========

Recall all spies based on a given planet who are currently away from the 
planet.

If you have spies out at multiple different locations, this will go to each of 
those locations and get back all of your spies.  Uses the fastest ships you 
have available that can carry spies.

All you have to specify is the name of the planets to pull spies back to::

    >>> python bin/recall_all_spies.py Earth

For complete help, see the script's help documentation:

    >>> python bin/recall_all_spies.py -h


.. autoclass:: lacuna.binutils.libsend_excavs.SendExcavs
   :members:
   :show-inheritance:

.. autoclass:: lacuna.binutils.libsend_excavs.Cell
   :members:
   :show-inheritance:

