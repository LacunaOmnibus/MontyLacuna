
.. _send_excavs:

Send Excavs
===========

Sends out excavators from one of your colonies to the nearby planets of 
whatever type or types you want to excavate.

This does not build excavators for you; you have to have those ready to go 
before running this; see :ref:`build_ships` if you haven't got excavators 
ready to go yet.

To send all excavators possible from Earth to the nearest p33 and/or p35 
planets available::

    >>> python bin/send_excavs.py -tp33 -t p35 Earth

Note that both formats, *-tp33* and *-t p35*, will work fine.

If you're trying to split up your excavators between p11 and p12 planets, and 
you've got 20 excavators to send, you'd run ``send_excavs.py`` twice::

    >>> python bin/send_excavs.py --max_send 10 -t p11 Earth
    >>> python bin/send_excavs.py --max_send 10 -t p12 Earth


If Earth has already sent out its maximum number of excavators, 
``send_excavs.py`` will let you know, so there's no harm in accidentally 
running this for a planet that's already set, excavator-wise.

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

