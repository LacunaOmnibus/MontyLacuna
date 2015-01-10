
.. _post_starter_kit:

Post Starter Kit
================

Posts a starter (noob) kit to either the TM or SST for you.

Post a Resources kit from Earth::

    >>> python bin/post_starter_kit.py Earth resources

By default, all posted kits cost 0.1 E.  However, you can charge whatever you 
like::

    >>> python bin/post_starter_kit.py --price 2.4 Earth resources

Named Kits
----------

- Resources Kit ('resources', resource', 'res')

  - Algae Pond
  - Amalgus Meadow
  - Beeldeban Nest
  - Denton Brambles
  - Geo Thermal Vent
  - Lapis Forest
  - Malcud Field
  - Natural Spring
  - Volcano

- Storage Kit ('storage', 'store', 'stor')

  - Interdimensional Rift
  - Ravine

- Military Kit ('military', 'mil')

  - Citadel of Knope
  - Crashed Ship Site
  - Gratch's Gauntlet
  - Kalavian Ruins

- Utility Kit ('utility', 'util', 'ute')

  - Black Hole Generator
  - Library of Jith
  - Oracle of Anid
  - Pantheon of Hagness
  - Temple of the Drajilites

- Beach Kit ('beach')

  - All 13 Beach plans

- Decoration ('decoration', deco')

  - Crater
  - Grove of Trees
  - Lagoon
  - Lake
  - Patch of Sand
  - Rocky Outcropping

- Full Basic Kit ('fullbasic', 'full_basic', 'full')

  - Combines all plans from the Resources and Storage kits above.

- Big Kit ('big')

  - Combines all plans from the Resources, Storage, Military, and Utility kits 
    above.

Full Documentation
------------------

For complete help, see the script's help documentation:

    >>> python bin/post_starter_kit.py -h

.. autoclass:: lacuna.binutils.libpost_starter_kit.PostStarterKit
   :members:
   :show-inheritance:

