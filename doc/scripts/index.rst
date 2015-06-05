
.. _scripts_index:

MontyLacuna Scripts
===================

Starter Scripts
---------------

There are a few scripts that help with the initial MontyLacuna setup.  By the 
time you're reading this, you've probably run them already as you were 
following through the setup process.

They're being listed below for completeness, but if you've already run these 
scripts (and if you just finished walking through the install instructions, 
you've run both of these), you shouldn't need to run them again.

.. toctree::
   :maxdepth: 2

   create_config_file
   get_pip

Regular Scripts
---------------

Most of the available scripts are Lacuna Expanse toolkit-type scripts, similar 
to the GLC scripts many players are already familiar with.

These scripts have built-in documentation.  You can get the basic command-line 
syntax just by running the script with no arguments::

    >>> python bin/scriptname.py

Or, you can get more in-depth information on the script by passing the ``-h`` 
(or ``--help``) flag::

    >>> python bin/scriptname.py -h

Most scripts allow you to send various command-line arguments.  Remember that 
if your arguments contain spaces, you have to quote them::

    >>> python bin/scriptname.py --planet "My Planet Name"

When you're running MontyLacuna scripts, don't forget that you can set up and 
use :ref:`abbrvs` for your colony and space station names.

Scripts that tell you about stuff
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. toctree::
   :maxdepth: 1

   ships_report
   show_laws
   spies_report
   stations_report
   version


Scripts that do stuff
~~~~~~~~~~~~~~~~~~~~~
.. toctree::
   :maxdepth: 1

   assign_spies
   build_ships
   excavs_report
   glyph_repair
   post_starter_kit
   recall_all_ships
   recall_all_spies
   scuttle_ships
   send_excavs
   search_archmin
   train_spies
   turnkey
   update

