
.. _send_excavs:

Send Excavs
===========

**Not quite ready for prime time yet.**

This script needs the ability to check what laws have been passed by foreign 
space stations, and while that ability currently works on PT, it's not yet 
working on US1.  So attempting to run this script on US1 will likely explode 
spectacularly.  The law-checking ability should be coming to US1 soon, at 
which point this will work there.

Sends out excavators from one of your colonies to the nearby planets of 
whatever type or types you want to excavate.  This does not build excavators 
for you; you have to have those ready to go before running this; see 
:ref:`build_ships` if you haven't got excavators ready to go yet.

    >>> python bin/send_excavs.py -tp33 -t p35 Earth

For complete help, see the script's help documentation:

    >>> python bin/send_excavs.py -h


.. autoclass:: lacuna.binutils.libsend_excavs.SendExcavs
   :members:
   :show-inheritance:

.. autoclass:: lacuna.binutils.libsend_excavs.Cell
   :members:
   :show-inheritance:

.. autoclass:: lacuna.binutils.libsend_excavs.Ring
   :members:
   :show-inheritance:

