

.. sidebar:: Jump to

    - :ref:`abbrvs`
    - :ref:`setting_abbrvs`
    - :ref:`displaying_abbrvs`
    - :ref:`deleting_abbrvs`
    - :ref:`using_abbrvs`

.. _abbrvs:

Body Abbreviations
==================
Planet and Space Station names both tend to get pretty long, and having to 
type out the entire name at the command line when running scripts can get 
tedious.

To help with that, MontyLacuna has a body name abbreviation system.  It allows 
you to set abbreviations for your planets with longer names, display those 
abbreviations, and delete them when you're not using them any more.

All MontyLacuna scripts that accept a planet name argument will also accept 
any abbreviation you've set up.

.. _setting_abbrvs:

Setting Abbreviations
---------------------
To set the abbreviation for the planet "My Fantastic Planet Number 01" to just 
"fan01"::

    >> py bin/abbrv_set.py "My Fantastic Planet Number 01" fan01
    My Fantastic Planet Number 01 can now be abbreviated as 'fan01'

You can set abbreviations for both planets and space stations.  So to set up 
abbreviations for a small empire in a small alliance::

    >> py bin/abbrv_set.py "My Fantastic Planet Number 01" fan01
    >> py bin/abbrv_set.py "My Fantastic Planet Number 02" fan02
    >> py bin/abbrv_set.py "My Fantastic Planet Number 03" fan03
    >> py bin/abbrv_set.py "My Fantastic Planet Number 04" fan04
    >> py bin/abbrv_set.py "Station GreatStation 01" ss01
    >> py bin/abbrv_set.py "Station GreatStation 02" ss02
    >> py bin/abbrv_set.py "Station GreatStation 03" ss03

.. _displaying_abbrvs:

Displaying Set Abbreviations
----------------------------
You can check the abbreviation for any single planet with::

    >> py bin/abbrv_show.py "My Fantastic Planet Number 01"
    My Fantastic Planet Number 01 is abbreviated as fan01

But you still had to type out the full planet name for that, and it only shows 
you a single abbreviation.  More likely, what you're going to want is to see 
all of your abbreviations at one time::

    >> py bin/abbrv_show.py all

    FULL NAME                                          ABBREVIATION
    My Fantastic Planet Number 01                      fan01
    My Fantastic Planet Number 02                      fan02
    My Fantastic Planet Number 03                      fan03
    My Fantastic Planet Number 04                      fan04
    Station GreatStation 01                            ss01
    Station GreatStation 02                            ss02
    Station GreatStation 03                            ss03
    
.. _deleting_abbrvs:

Deleting An Abbreviation
------------------------
If you decide you're no longer using a given abbreviation and want to get it 
out of the list::

    >> py bin/abbrv_del.py "My Fantastic Planet Number 01"

    >> py bin/abbrv_show.py all
    FULL NAME                                          ABBREVIATION
    My Fantastic Planet Number 02                      fan02    # Note that 01 is gone.
    My Fantastic Planet Number 03                      fan03
    My Fantastic Planet Number 04                      fan04
    Station GreatStation 01                            ss01
    Station GreatStation 02                            ss02
    Station GreatStation 03                            ss03
    
.. _using_abbrvs:
    
Using Abbreviations
-------------------
Once your abbreviations are set up, you can use them as the body name 
arguments for any MontyLacuna scripts that need a body name::

    >> py bin/build_ships.py fan02 sweeper
    >> py bin/scuttle_ships.py --num 10 fan03 scow
    >> py bin/recall_all_ships.py fan04

...etc.

