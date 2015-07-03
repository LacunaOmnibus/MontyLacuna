
.. _ss_lab:

SS Lab
======
Builds plans at a Space Station lab.  If you request multiple plans, it will 
build one at a time and go to sleep for however long the build takes, then 
wake back up again to build more.

You can also chose to subsidize the builds with Essentia if you like.

To build a single level one Art Museum plan on Earth::

    >>> python bin/ss_lab.py Earth art

To build ten level one Art Museum plans on Earth::

    >>> python bin/ss_lab.py --num 10 Earth art

To build a single level 15 Art Museum plan on Earth::

    >>> python bin/ss_lab.py --level 15 Earth art

To build ten level 15 Art Museum plan on Earth::

    >>> python bin/ss_lab.py --num 10 --level 15 Earth art

To build ten level 15 Art Museum plan on Earth and subsidize all of them, which will cost a total of 20 E::

    >>> python bin/ss_lab.py --num 10 --level 15 --sub Earth art

Plan Names
----------
You do have to provide the plan name exactly as the server expects to see it.

    ==================  =================================
    ARGUMENT            IN-GAME NAME YOU'RE FAMILIAR WITH
    ==================  =================================
    art                 Art Museum
    command             Station Command Center
    food                Culinary Institute
    ibs                 Interstellar Broadcast System
    opera               Opera House
    parliament          Parliament
    policestation       Police Station
    warehouse           Warehouse
    ==================  =================================

For complete help, see the script's help documentation::

    >>> python bin/ss_lab.py -h

.. autoclass:: lacuna.binutils.libss_lab.SSLab
   :members:
   :show-inheritance:

