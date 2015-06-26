
.. _allow_friendly_bhg:

Allow Friendly BHG
==================
The Neutralize BHG law stops anybody who's not in your alliance but is in the 
jurisdiction of your space station from using their BHGs for anything.

If you have an alliance that's friendly, this script will allow the members of 
that alliance to use their BHGs, even if you have that restriction turned on.

You must have a non-damaged Parliament of at least level 28 on your station to 
enact this law.

This script is going to issue a proposition, so you'll need to be logged in 
using your real password, not your sitter::

    >>> python bin/allow_friendly_bhg.py --section real "My Station Name" "Friendly Ally Name"

Station and Alliance Names
--------------------------
When you type the name of your space station, you can use :ref:`abbrvs` if 
you've got one set up.  Otherwise you'll need to type the full name of the 
space station.

For the friendly alliance name, you only need to type the beginning of the 
alliance name, using at least three letters.  That will search for all 
alliances whose names match from the beginning.  If more than one alliance is 
found that matches, you'll be presented with a list::

    >>> python bin/allow_friendly_bhg.py "My Station Name" "The"
        Multiple alliances were found that match 'The':
                01: The Understanding
                02: The Star Union
                03: The Road
                04: The Invisible Kingdom
                05: The Lazorblade Consortium
                06: the_bear_pride
                07: The Orion Confederation
                08: The Old Republic
                09: The Dark Ones
                10: The Navigators
                11: The Unitement of Stars
                12: The Singularity Guild
                13: The Central Spacial Dominon
                14: The Vortex
                15: The Fist
                16: The Nexus
                17: The Balance Imperative
                18: The Covenant

        Which one did you mean? 3
        You chose 'The Road'.

Force fresh data
----------------

Station data gets cached so retrieving it on the next run will be quicker.  If 
you want to clear that cached data, pass the ``--fresh`` option::

    >>> python bin/allow_friendly_bhg.py --fresh "My Station" "Friendly Ally"

Full documentation
------------------

For complete help, see the script's help documentation::

    >>> python bin/allow_friendly_bhg.py -h

.. autoclass:: lacuna.binutils.liballow_friendly_bhg.AllowFriendlyBHG
   :members:
   :show-inheritance:

