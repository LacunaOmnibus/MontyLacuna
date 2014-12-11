
.. _send_excavs:

Send Excavs
===========

Sends out excavators from a planet to the nearby planets of whatever type or 
types you want to excavate.  This does not build excavators for you; you have 
to have those ready to go before running this; see :ref:`build_ships` if you 
haven't got excavators ready to go yet.

    >>> python bin/send_excavs.py -tp33 -t p35 Earth

This mostly works, but still needs a little love.  If you want to run this for 
a single one of your planets, or for two planets that are separated by a lot 
of space, it'll work fine.  But don't try running it for multiple nearby 
planets.  It won't break anything, but it'll end up sending excavators out 
farther away than needed.

Current issues with this:
    - If you send an excav from Earth to Target_A, then run this for Mars, and 
      it also tries to send an excav to Target_A, the send from Mars will be 
      disallowed (because you already have an excav from your empire on the 
      way).  This will be mis-interpreted as being because of a MO Excavation 
      law.  The station that has seized Target_A will then be added to the 
      list of "bad_stations", and no more excavs will be sent to any planet 
      under that station's jurisdiction.  And that station may well be your 
      own station, so perfectly valid planets will be skipped.

      - Right now, it's only possible to view the laws set by a space station 
        owned by your own alliance.  However, the ability for any player to 
        check on the laws of any station is currently being added (it should 
        be on PT already).  Once we're able to check laws on any station, this 
        problem should get fixed.

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

