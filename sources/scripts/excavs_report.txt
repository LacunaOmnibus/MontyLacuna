
.. _excavs_report:

Excavators Report
=================
Reports on the excavators you've sent out at one or all of your planets, 
including the distance from your colony to the excavated planet.

Being able to see the distance is especially helpful if you've ever moved your 
colony around with a BHG.  Excavated planets that are too far away will be 
less efficient, as replacement excavators will have to spend an inordinate 
amount of time travelling between your colony and the excavated planet.

An example report::

    >>> python bin/excavs_report Earth
                         Earth
                         =====
    EXCAVATED COLONY                DISTANCE     TYPE
    Earth                               0.00     p11
    Mars                               16.55     p12
    Jupiter                            18.97     p12
    Saturn                             22.20     p35
    Uranus                             23.09     p33
    Neptune                            23.77     p35
    Pluto                            1234.85     p35

Remember that the colony hosting the archaeology ministry is, itself, being 
excavated, and at the rate of two regular planets.  So since Earth is a p11 
planet, we've got two regular excavators out at p12 planets, which are the 
resource complement to the p11.

Pluto is very far away compared to the other planets.  After seeing this 
report, you'd most likely want to delete the excavator on Pluto and send out 
another one to a much closer planet.  Poor Pluto can't catch a break.

Report on all planets
---------------------
As with several other MontyLacuna scripts, you can pass ``all`` as the planet 
name to view reports on all of your planets::

    >>> python bin/excavs_report.py all

This report can get pretty long, and might scroll off the screen so far that 
you can't see the whole thing.  So you can just redirect the output to a 
file::

    >>> python bin/excavs_report.py all > excavs.txt

...then open up ``excavs.txt`` in your favorite text editor.

Force fresh data
----------------

Data get cached so retrieving it on the next run will be quicker.  This way 
you can conveniently run a report multiple times, or even run different 
reports, without having to wait or waste your RPCs.  

However, if you run a report once, then update something (eg you send out a 
new excavator) and want to run the same report again to see your new resource 
situation, you won't want to look at data cached from the previous run.  In 
that case, pass the ``--fresh`` option::

    >>> python bin/excavs_report.py --fresh Earth

Full documentation
------------------

For complete help, see the script's help documentation::

    >>> python bin/excavs_report.py -h

.. autoclass:: lacuna.binutils.libexcavs_report.ExcavsReport
   :members:
   :show-inheritance:

