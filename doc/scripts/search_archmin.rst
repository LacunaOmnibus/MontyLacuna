
.. _search_archmin:

Search Archaeology Ministry
===========================

Starts a search through available ore for glyphs at your Archaeology Ministry.  
You can specify what glyph type to search for, or just tell the script to 
search for whatever glyph type is most needed.

Remember that you must have 10,000 units of ore to be able to search through 
it for a glyph.  If you pass ``needed`` as the glyph type, the script will 
find the glyph type that your plant has least of, for which you also have at 
least 10,000 ore.  

But if you specify a glyph type yourself, you must make sure that you have 
enough of that ore.  If not, a warning will be issued and the planet will be 
skipped.

Arch min searches take six hours.  So if you plan to set up this script on a 
schedule of some sort, you should schedule it to run every six hours.  Even 
better would be if you could set up your schedule so it runs every (6 hours + 
5 minutes).

To search for rutile glyphs on Earth::

    >>> python bin/search_archmin.py Earth rutile

To search for whatever glyph type Earth has the least of::

    >>> python bin/search_archmin.py Earth needed

To search for the most needed glyph type on all of your planets::

    >>> python bin/search_archmin.py all needed

For complete help, see the script's help documentation:

    >>> python bin/search_archmin.py -h

.. autoclass:: lacuna.binutils.libsearch_archmin.SearchArchmin
   :members:
   :show-inheritance:

