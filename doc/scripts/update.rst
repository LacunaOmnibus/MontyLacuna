
.. _update:

Update MontyLacuna
==================
Updates MontyLacuna from GitHub so you don't have to walk through the download 
process again.

To get the newest scripts, libraries, bugfixes, etc, just run the update 
script::

    >>> python bin/update.py

``update.py`` is different from pretty much all of the other MontyLacuna 
scripts in that it does not accept any arguments from the command line.  It 
doesn't respond to the standard ``--help`` flag, or provide basic usage 
information at all.


CAUTION!
--------
This update script is mainly meant with the non-programmer in mind.  If you've 
edited any existing MontyLacuna scripts yourself, those edits will be lost 
when you update.

You don't have to worry about your ``lacuna.cfg`` file being overwritten, just 
any scripts you've modified.

If you've made any brand-new scripts (rather than editing existing MontyLacuna 
scripts), your new scripts should be untouched.  The possible exception to 
this is if you create a script and name it eg ``do_neat_stuff.py``, and 
sometime in the future a script named ``do_neat_stuff.py`` gets added to the 
official MontyLacuna distribution just by coincidence, then the official 
MontyLacuna script will overwrite yours.

So when writing your own scripts, it might make sense to prepend the script 
filenames with your name or initials or something.  So when Infinate Ones 
makes his own custom script, he'd name it ``io_do_neat_stuff.py``.


Full documentation
------------------
.. autoclass:: lacuna.binutils.libupdate.Update
   :members:
   :show-inheritance:

