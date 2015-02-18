
.. _post_starter_kit:

Post Starter Kit
================

Posts a specific named starter/noob kit to either the TM or SST for you.  The 
easiest and most common way of running this will be to chose from one of 
several :ref:`pre-set named kits <named_kits>` and post that.

Post a Resources kit from Earth::

    >>> python bin/post_starter_kit.py --kit resources Earth

If you want to post 5 resources kits, just run the above command five times.  
Your terminal should automatically repeat the previous command when you press 
the Up arrow key.  So just type the command above once, hit enter, then, after 
it's finished running, hit the Up arrow and hit enter again, etc.

By default, all posted kits cost 0.1 E, but you can charge whatever you like::

    >>> python bin/post_starter_kit.py --kit res --price 0.5 Earth

The named kits all contain level 1+0 plans.  You can change the extra build 
level to offer 1+1 or 1+2 or whatever extra level you like, as long as you 
have the plans on hand, by using the ``--ebl`` (Extra Build Level) argument.  
This example would offer the Resources Kit with all plans at 1+2:: 

    >>> python bin/post_starter_kit.py --kit res --price 10.3 --ebl 2 Earth

SST
---
Kits are normally posted to the Trade Ministry, but sometimes you're out of 
range of that desperate new player and you're willing to spend the 1E at the 
SST just to get him to stop begging ;)

To post a regular Resources kit to the SST::

    >>> python bin/post_starter_kit.py --sst --kit res --price 1.5 Earth

    ***
    Be aware that using this option will automatically charge you the 1E SST 
    fee, so set your asking price accordingly.
    ***

.. _named_kits:

Named Kits
----------

To make posting a little easier, kits with longer names have aliases, which  
are shown in parentheses below.  So to add (eg) a Resources Kit at the default 
price of 0.1 E, you can do any of the following::

    >>> python bin/post_starter_kit.py --kit resources Earth
    >>> python bin/post_starter_kit.py --kit resource Earth
    >>> python bin/post_starter_kit.py --kit res Earth

If you don't want to use any of these pre-rolled kits, see the 
:ref:`custom_kits` section below.

- **Resources Kit** ('resources', resource', 'res')

  - Algae Pond
  - Amalgus Meadow
  - Beeldeban Nest
  - Denton Brambles
  - Geo Thermal Vent
  - Lapis Forest
  - Malcud Field
  - Natural Spring
  - Volcano

- **Storage Kit** ('storage', 'store', 'stor')

  - Interdimensional Rift
  - Ravine

- **Military Kit** ('military', 'mil')

  - Citadel of Knope
  - Crashed Ship Site
  - Gratch's Gauntlet
  - Kalavian Ruins

- **Utility Kit** ('utility', 'util', 'ute')

  - Black Hole Generator
  - Library of Jith
  - Oracle of Anid
  - Pantheon of Hagness
  - Temple of the Drajilites

- **Halls 10 Kit** ('halls10', 'hall10', 'h10')
- **Halls 100 Kit** ('halls100', 'hall100', 'h100')

  - These contain 10 and 100 halls, respectively.
  - Yes, I'm well aware that you're dying to post 11 or 99 halls, and are just 
    about to send off an email to me asking me to enable that.  No.  These are 
    meant to be bulk-posted starter kits, and choices of 10 or 100 are fine.

    - If you really really want some other quantity, see the section below on 
      "Creating A Customized Kit".

- **Beach Kit** ('beach')

  - All 13 Beach plans

- **Decoration Kit** ('decoration', deco')

  - Crater
  - Grove of Trees
  - Lagoon
  - Lake
  - Patch of Sand
  - Rocky Outcropping

- **Pretty Kit** ('pretty')

  - Combines all plans from the Beach and Decoration kits above.

- **Full Basic Kit** ('fullbasic', 'full_basic', 'full')

  - Combines all plans from the Resources and Storage kits above.

- **Big Kit** ('big')

  - Combines all plans from the Resources, Storage, Military, and Utility kits 
    above.

.. _custom_kits:

Creating A Customized Kit
-------------------------
You may want to post some slightly different combination of plans that's not 
listed above.  To create your own custom kit, you'll need to edit the 
``post_starter_kit.py`` script, but doing so is not hard.

Open the script in an editor, and find the section near the top that looks 
like::

    ###
    ### Define any custom kits here
    ###

Right under that, define your customized kit or kits.  For example, here are 
two custom kit definitions::

    ### Modify a standard ResKit for orbit 1 - remove the food buildings that
    ### won't work in that orbit.
    orb1kit = lib.CustomKit( sk.client, lib.ResKit(sk.client) )
    orb1kit.del_plan( 'Amalgus Meadow' )
    orb1kit.del_plan( 'Beeldeban Nest' )
    orb1kit.del_plan( 'Denton Brambles' )
    orb1kit.del_plan( 'Lapis Forest' )
    ### Since we're not specifying price, it'll default to 0.1 E.

    ### Start with a completely empty kit, and just add a few plans.
    happykit = lib.CustomKit( sk.client )
    happykit.add_plan( 'Kalavian Ruins', 3)             # include a 1+3 Ruins
    happykit.add_plan( 'Halls of Vrbansk', 0, 5)        # include 5 Halls (with 0 extra build levels)
    happykit.price = 1.5

You can define as many custom kits as you want, calling ``del_plan()`` and/or 
``add_plan()`` as often as needed to define what you want your kit to contain.  
When you create a new custom kit, there's no need to delete any of your old 
kits - might as well leave the old kits' definitions there in case you want to 
use them in the future.

To specify which of your custom kits you want to use, just include this line 
after your kit definitions::

    sk.kit = happykit

...And that's it.  When you run the kit poster script, it'll post your 
``happykit`` for 1.5 E::

    >>> python bin/post_starter_kit.py Earth

Full Documentation
------------------

For complete help, see the script's help documentation:

    >>> python bin/post_starter_kit.py -h

.. autoclass:: lacuna.binutils.libpost_starter_kit.PostStarterKit
   :members:
   :show-inheritance:

.. autoclass:: lacuna.binutils.libpost_starter_kit.StarterKit
   :members:
   :show-inheritance:

.. autoclass:: lacuna.binutils.libpost_starter_kit.CustomKit
   :members:
   :show-inheritance:

