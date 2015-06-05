
.. _glyph_repair:

Glyph Repair
============
Repairs any damaged glyph buildings on a given planet::

    >>> python bin/glyph_repair.py Earth

Or on all of your planets::

    >>> python bin/glyph_repair.py all

If you've run this or any other MontyLacuna script recently and you just now 
took damage, this script may not notice the damage because the previous planet 
state is cached, but you need those glyph buildings back up now now now::

    >>> python bin/glyph_repair.py --fresh all

"But what about the non-glyph buildings?"
-----------------------------------------
Those might get added later.  But for now, this script can safely be run on a 
schedule, because glyph building repairs are free and won't use up any of your 
resources.

Full Documentation
------------------

For complete help, see the script's help documentation:

    >>> python bin/glyph_repair.py -h

.. autoclass:: lacuna.binutils.libglyph_repair.GlyphRepair
   :members:
   :show-inheritance:

