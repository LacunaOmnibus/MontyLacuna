
.. _scripts_index:

MontyLacuna Scripts
===================

Starter Scripts
---------------

There are a few scripts that help with the initial MontyLacuna setup.  By the 
time you're reading this, you've probably run them already as you were 
following through the setup process.

They're being listed below for completeness, but if you've already run these 
scripts, you shouldn't need to run them again.

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

.. toctree::
   :maxdepth: 2

   build_ships
   recall_all_ships
   recall_all_spies
   send_excavs
   ships_report

