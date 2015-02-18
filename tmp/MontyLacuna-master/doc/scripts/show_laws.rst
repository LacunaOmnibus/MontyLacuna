
.. _show_laws:

Show Laws
=========

Displays the laws controlling a given star::

    >>> python bin/show_laws.py Sol

    Members Only Colonization      Only members of {Alliance 00 SomeAll}...
    Members Only Colonization      Only members of {Alliance 00 SomeAll}...
    Members Only Mining Rights     Only members of {Alliance 00 SomeAll}...
    Members Only Colonization      Only members of {Alliance 00 SomeAll}...
    Members Only Colonization      Only members of {Alliance 00 SomeAll}...
    Members Only Mining Rights     Only members of {Alliance 00 SomeAll}...
    Members Only Excavation        Only members of {Alliance 00 SomeAll}...
    BHG Neutralized                All Black Hole Generators will cease ...

    The seizing station, International Space Station, has seized 100 stars.
    That station is owned by SomeAlliance.

Most stations have lots of star seizure laws passed.  Displaying them all will 
cause the report to scroll off your screen.  It's noisy, and you normally 
don't care about seeing all of those seizures, so they're not included in a 
normal report.

However, if you do want to see all those seizure laws as well::

    >>> python bin/show_laws.py --all Sol

    Seize Some Planet 1            Seize Some Planet 1
    Seize Some Planet 2            Seize Some Planet 2
    Seize Some Planet 3            Seize Some Planet 3
    Seize Some Planet 4            Seize Some Planet 4
    Seize Some Planet 5            Seize Some Planet 5
    Seize Some Planet 6            Seize Some Planet 6
    .... You get the idea at this point ...
    Members Only Colonization      Only members of {Alliance 00 SomeAlli...
    Members Only Colonization      Only members of {Alliance 00 SomeAlli...
    Members Only Mining Rights     Only members of {Alliance 00 SomeAlli...
    Members Only Colonization      Only members of {Alliance 00 SomeAlli...
    Members Only Colonization      Only members of {Alliance 00 SomeAlli...
    Members Only Mining Rights     Only members of {Alliance 00 SomeAlli...
    Members Only Excavation        Only members of {Alliance 00 SomeAlli...
    BHG Neutralized                All Black Hole Generators will cease ...

    The seizing station, International Space Station, has seized 100 stars.
    That station is owned by SomeAlliance.

Alliance Names
--------------
Some laws include the name of the alliance that passed the law in the 
description of the law itself.  However, not all of them do.  If it's possible 
to display the name of the station's owning alliance, it will be displayed, 
but it's simply not always possible.

Force Fresh Data
----------------

When running a report, star data gets cached so retrieving it on the next run 
will be quicker.  This way you can conveniently run a report multiple times 
without having to wait or waste your RPCs.  

To clear the cache, pass the ``--fresh`` option::

    >>> python bin/show_laws.py --fresh Sol

Full Documentation
------------------

For complete help, see the script's help documentation:

    >>> python bin/show_laws.py -h

.. autoclass:: lacuna.binutils.libshow_laws.ShowLaws
   :members:
   :show-inheritance:

