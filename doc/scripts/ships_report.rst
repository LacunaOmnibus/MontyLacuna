
.. _ships_report:

Ships Report
============

Produces a report on the ships located on either a single planet or all of 
your planets.

An example report on just warships on Earth::

    >>> python bin/ships_report.py --tag War Earth

    There are 2,123 total ships on Earth.
            Excavator                          23
            Scow Mega                         100
            Snark                             500
            Sweeper                         1,500

To report on both trade- and war- ships on a single planet::

    >>> python bin/ships_report.py --tag War --tag Trade Earth

To report on all ships on a single planet, just skip the ``--tag`` argument 
altogether::

    >>> python bin/ships_report.py Earth

Any of those combinations of tags can be used to report on all of the ships 
across your empire::

    >>> python bin/ships_report.py all

When running a report, ship data get cached so retrieving it on the next run 
will be quicker.  This way you can conveniently run a report multiple times 
without having to wait or waste your RPCs.  

However, if you, for example, run the report on a planet, then go build a 
bunch of ships and want to run the same report again to see your new ships, 
you won't want to look data cached from the first run (before you built the 
ships).  In that case, pass the ``--fresh`` option:

    >>> python bin/ships_report.py --fresh Earth

For complete help, see the script's help documentation:

    >>> python bin/ships_report.py -h


.. autoclass:: lacuna.binutils.libships_report.ShipsReport
   :members:
   :show-inheritance:

.. autoclass:: lacuna.binutils.libships_report.PlanetShipData
   :members:
   :show-inheritance:

