
.. _turnkey:

Turnkey (Prisoner Management)
=============================
Displays, releases, or executes foreign spies in either a Security Ministry 
(on a colony) or a Police Station (on a space station).

Viewing Spies and Prisoners
---------------------------
View the prisoners in a Security Ministry's prison::

    >>> python bin/turnkey.py Earth view_prisoners

It works the same way on a Police Station's prison::

    >>> python bin/turnkey.py ISS view_prisoners

The script will figure out that ``Earth`` is a colony and that ``ISS`` is a 
space station, so you don't have to specify whether you're dealing with a 
Security Ministry or Police Station.

Viewing foreign spies works the same way to display all free foreign spies 
whose level is lower than the Security Ministry's or Police Station's level::

    >>> python bin/turnkey.py ISS view_spies

Each of the above will show you the prisoners or spies on page one, with a 
maximum of 25 prisoners/spies per page.  If you want to look at page 3::

    >>> python bin/turnkey.py --page 3 ISS view_spies

...or, if you want to look at all pages (this will take some time and is 
likely to scroll off your screen)::

    >>> python bin/turnkey.py --page 0 Earth view_prisoners

Executing and Releasing
-----------------------
You can't release or execute foreign spies until they're in prison.  So if 
``view_spies`` showed that there are Bad Dudes around, you'll need to run 
security sweeps to catch them so that they become prisoners.  See 
:ref:`assign_spies` for that.

To release all of the prisoners on the first page of results::

    >>> python bin/turnkey.py Earth release
    Page 1 is the default, so there's no need to pass the '--page' argument 
    here.

To execute all of the prisoners on the third page of results::

    >>> python bin/turnkey.py --page 3 Earth execute

To execute everybody (you monster!)::

    >>> python bin/turnkey.py --page 0 Earth execute

When releasing or executing prisoners, each individual prisoner must be 
released or executed separately.  This means that if you have 100 prisoners, 
the process will use 100 RPCs and take 100 seconds.  Time your actions 
accordingly.

Full Documentation
------------------
For complete help, see the script's help documentation:

    >>> python bin/build_ships.py -h

.. autoclass:: lacuna.binutils.libturnkey.Turnkey
   :members:
   :show-inheritance:

