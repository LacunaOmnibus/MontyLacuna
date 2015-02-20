
.. _send_excavs:

Send excavs
===========
Sends out excavators from one or all of your colonies to the nearby planets of 
whatever type or types you want to excavate.

This does not build excavators for you; you have to have those ready to go 
before running this; see :ref:`build_ships` if you haven't got excavators 
ready to go yet.

To send all excavators possible from Earth to the nearest p33 and/or p35 
planets available::

    >>> python bin/send_excavs.py -tp33 -t p35 Earth

To send excavators from all of your colonies, instead of just one::

    >>> python bin/send_excavs.py -tp33 -t p35 all

Note that both formats, *-tp33* and *-t p35*, will work fine.

If you're trying to split up your excavators between p11 and p12 planets, and 
you've got 20 excavators to send, you'd run ``send_excavs.py`` twice::

    >>> python bin/send_excavs.py --max_send 10 -t p11 Earth
    >>> python bin/send_excavs.py --max_send 10 -t p12 Earth

If Earth has already sent out its maximum number of excavators, 
``send_excavs.py`` will let you know, so there's no harm in accidentally 
running this for a planet that's already set, excavator-wise.

What's being sent where?
------------------------
We're able to check on all of the stars in a given 54x54 box with a single 
server check.  So to start, this gets such a box with your planet at the 
center::

                        +---------+
                        |         |
                        |    o    |
                        |         |
                        +---------+

If the script can't find enough of the right planets inside that first box, it 
draws a "ring" around that center box.  I use the word "ring", but it's really 
a larger square.  This "ring" is made up of 8 more 54x54 unit boxes::

            +---------+ +---------+ +---------+
            |         | |         | |         |
            | ring 1  | | ring 1  | | ring 1  |
            |         | |         | |         |
            +---------+ +---------+ +---------+
            +---------+ +---------+ +---------+
            |         | |         | |         |
            | ring 1  | |    o    | | ring 1  |
            |         | |         | |         |
            +---------+ +---------+ +---------+
            +---------+ +---------+ +---------+
            |         | |         | |         |
            | ring 1  | | ring 1  | | ring 1  |
            |         | |         | |         |
            +---------+ +---------+ +---------+

If the script still hasn't found enough of the right kinds of planets inside 
that first ring, it draws another ring around the first ring.  This second 
ring consists of 16 more 54x54 boxes.  

By default, the script will go as far out as three rings around the initial 
box around your planet.  After that, it will give up, even if it hasn't sent 
out all of your excavs.  If that happens, you can increase how far the script 
will go by increasing the ``--max_ring`` argument::

    >>> python bin/send_excavs.py -tp33 -t p35 --max_ring 5 Earth

Full documentation
------------------
For complete help, see the script's help documentation:

    >>> python bin/send_excavs.py -h

.. autoclass:: lacuna.binutils.libsend_excavs.SendExcavs
   :members:
   :show-inheritance:

.. autoclass:: lacuna.binutils.libsend_excavs.BodyCache
   :members:
   :show-inheritance:

.. autoclass:: lacuna.binutils.libsend_excavs.Cell
   :members:
   :show-inheritance:

.. autoclass:: lacuna.binutils.libsend_excavs.Ring
   :members:
   :show-inheritance:

