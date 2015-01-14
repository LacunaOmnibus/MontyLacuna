
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

Arch min searches take five hours, fifty minutes.  So if you plan to set up 
this script on a schedule of some sort, you should schedule it to run every 
six hours.  That way, you can get four arch min searches per planet, per day.

To search for rutile glyphs on Earth::

    >>> python bin/search_archmin.py Earth rutile

To search for whatever glyph type Earth has the least of::

    >>> python bin/search_archmin.py Earth needed

To search for the most needed glyph type on all of your planets::

    >>> python bin/search_archmin.py all needed

See the :ref:`ores_list` for a complete list of ores you can search.  For a 
quick ore list reminder from the terminal, just include the ``-l`` or 
``--list`` argument, which will list out all ores and then quit::

    >>> python bin/search_archmin.py -l

For complete help, see the script's help documentation:

    >>> python bin/search_archmin.py -h

.. autoclass:: lacuna.binutils.libsearch_archmin.SearchArchmin
   :members:
   :show-inheritance:

