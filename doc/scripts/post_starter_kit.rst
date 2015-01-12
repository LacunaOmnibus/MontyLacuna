
.. _post_starter_kit:

Post Starter Kit
================

Posts a specific named starter/noob kit to either the TM or SST for you.  See 
below for a list of all available named kits.

Post a Resources kit from Earth::

    >>> python bin/post_starter_kit.py Earth resources

If you want to post 5 resources kits, just run the above command five times.  
Your terminal should automatically repeat the previous command when you press 
the Up arrow key.  So just type the command above once, hit enter, then, after 
it's finished running, hit the Up arrow and hit enter again, etc.

By default, all posted kits cost 0.1 E.  However, you can charge whatever you 
like::

    >>> python bin/post_starter_kit.py --price 0.5 Earth resources

The named kits all contain level 1+0 plans.  You can change the extra build 
level to offer 1+1 or 1+2 or whatever extra level you like, as long as you 
have the plans on hand, by using the ``--ebl`` (Extra Build Level) argument.  
This example would offer the Resources Kit with all plans at 1+2:: 

    >>> python bin/post_starter_kit.py --price 10.3 --ebl 2 Earth resources

You cannot change the default level from 1.  Most players who would benefit 
from starter kits are not yet going to understand that a level 5 plan does not 
build a level 5 building from scratch, so changing the primary level is not 
allowed in the context of posting starter kits.

SST
---
Kits are normally posted to the Trade Ministry, but sometimes you're out of 
range of that desperate new player and you're willing to spend the 1E at the 
SST just to get him to stop begging ;)

To post a regular Resources kit to the SST::

    >>> python bin/post_starter_kit.py --sst --price 1.5 Earth resources

    ***
    Be aware that using this option will automatically charge you the 1E SST 
    fee, so set your asking price accordingly.
    ***

Named Kits
----------

When offering a kit for trade, the following named kits are available.  To 
make posting a little easier, kits with longer names have had aliases added.  
These aliases are shown in parentheses below.  So to add (eg) a Resources Kit 
at the default price of 0.1 E, you can do any of the following::

    >>> python bin/post_starter_kit.py Earth resources
    >>> python bin/post_starter_kit.py Earth resource
    >>> python bin/post_starter_kit.py Earth res

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

- Halls 10 Kit ('halls10', 'hall10', 'h10')
- Halls 100 Kit ('halls100', 'hall100', 'h100')

  - These contain 10 and 100 halls, respectively.
  - Yes, I'm well aware that you're dying to post 11 or 99 halls, and are just 
    about to send off an email to me asking me to enable that.  No.  These are 
    meant to be bulk-posted starter kits, and choices of 10 or 100 are fine.

    - If you really really want some other quantity, see the section below on 
      "Creating A Customized Kit".

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

Creating A Customized Kit
-------------------------
The named kits above are just my guess at what kinds of packs most people will 
generally want to be able to post.  I'm aware that you may want to post some 
slightly different combination of plans that's not listed above.

For now, creating your own kit is going to require that you edit some code.  I 
may come up with some more reasonable facility for creating custom kits in the 
future, but until that happens, code editing is it.

You'll need to edit the script's library file, 
``lib/lacuna/binutils/libpoststarter_kit.py``:
    - See the existing kit classes, starting with ResKit about line 22.  Copy 
      one of those existing kit classes, and edit it so it contains the plans 
      you want in your custom kit.  Be sure to change the name of your custom 
      kit to something unique that you recognize (eg "MyCustomKit").
    - Around line 141 is the list of valid choices that the user can pass in 
      as the name of the kit.  Add a name to represent your custom kit, along 
      with any aliases you want (just follow the existing examples).
    - In _set_kit(), around line 193 (this is going to be the hardest part), 
      you'll need to create a new regex (see the exising ``re.compile`` lines 
      as examples), and then you'll need to add a new ``elif`` block down 
      below.  Your ``elif`` block will be two lines of code, just as you can 
      see in the existing examples.

Yes, I'm aware the above is a bit more technical than some folks are 
comfortable dealing with.  Yes, I'm OK with that, at least for now.  If you 
can't figure out how to add your own custom kit, you're stuck with using one 
of the existing named kits.


Full Documentation
------------------

For complete help, see the script's help documentation:

    >>> python bin/post_starter_kit.py -h

.. autoclass:: lacuna.binutils.libpost_starter_kit.PostStarterKit
   :members:
   :show-inheritance:

