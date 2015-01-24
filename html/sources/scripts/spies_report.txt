
.. _spies_report:

Spies Report
============

Produces a report on the spies homed from either a single planet or all of 
your planets.

An example report on just spies homed from Earth::

    >>> python bin/spies_report.py Earth

    Earth
    -------
      Assignments:
        Counter Espionage                                                30
        Idle                                                             60
      Locations:
        123456  (    0,    0) - Earth                                    90

``Locations`` shows the ID, (X, Y) coordinates, and name of the planet or 
planets where the spies are located, rather than where they're based from (all 
of the spies in the report above are based from Earth).  In the example above, 
all of the spies are at home.

Note that this style report only contains spy assignments, locations, and 
counts.  If you want a more complete report, see the section below on CSV 
format.

Running for all Planets
-----------------------

To see what all your spies are doing, use ``all`` as the planet name:

    >>> python bin/spies_report.py all

Force Fresh Data
----------------

When running a report, spy data gets cached so retrieving it on the next run 
will be quicker.  This way you can conveniently run a report multiple times 
without having to wait or waste your RPCs.  

However, if you run the report on a planet, then go build a bunch of new 
spies, or assign existing spies to different tasks or whatever, and then want 
to run the same report again, you won't want to look at data cached from the 
first run.  In that case, pass the ``--fresh`` option::

    >>> python bin/spies_report.py --fresh Earth

Produce CSV Output
------------------

By default, the report is delivered to the screen in a summarized, 
human-readable format.  However, you can instead create a spreadsheet, which 
will contain full data on each individual spy::

    >>> python bin/spies_report.py --format csv all

That will produce the output in CSV format, on the screen.  Since CSV format 
on the screen isn't really very helpful, you should redirect that into a 
file::

    >>> python bin/spies_report.py --format csv all > myfile.csv

Now, you can open ``myfile.csv`` using Excel or whatever spreadsheet software 
you like.

Full Documentation
------------------

For complete help, see the script's help documentation:

    >>> python bin/spies_report.py -h

.. autoclass:: lacuna.binutils.libspies_report.SpiesReport
   :members:
   :show-inheritance:

.. autoclass:: lacuna.binutils.libspies_report.PlanetSpyData
   :members:
   :show-inheritance:

