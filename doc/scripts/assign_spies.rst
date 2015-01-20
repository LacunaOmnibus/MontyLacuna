
.. _assign_spies:

Assign Spies
============

Assigns spies based out of a single planet, in bulk, to a specified task.  
Note that this does not send any spies to a target.  You must make sure that 
your spies are in the correct locations before attempting to use this to 
assign them to tasks.

The name of the task to be performed must be translatable, see 
:ref:`spy_assg_translations`.

See also :ref:`spies_report`, to check out what your spies are doing right 
now, then use this script to assign them to some other task.

Assign all Idle spies on Earth to Counter Espionage::

    >>> python bin/assign_spies.py Earth "Counter Espionage"

Assign only 20 spies on Earth to Counter Espionage::

    >>> python bin/assign_spies.py --num 20 Earth counter 

Assign only your 20 highest-level spies on Earth to Counter Espionage::

    >>> python bin/assign_spies.py --num 20 --top level Earth counter

    This is actually exactly the same as the previous example, since 'level'
    is the default value for the --top option.

The special planet name 'all' will rotate through all of your planets, making 
the same assignments on each one.  This usually doesn't make much sense, 
except in the case of Counter Espionage.  If you want to assign all of your 
Idle spies on all of your planets to Counter Espionage::

    >>> python bin/assign_spies.py all counter

On the other hand, you might just want a maximum of 20 assigned to Counter on 
each planet::

    >>> python bin/assign_spies.py --num 20 --topoff all counter

    So if one planet already has 11 guys on counter, 9 more will be set to 
    counter.  If the next planet has nobody on counter, it'll get 20
    assigned, etc.

Assign 20 spies who are currently doing Counter Espionage to Idle::

    >>> python bin/assign_spies.py --num 20 --doing counter Earth idle

Assume you've sent all 90 of your spies from your planet, Earth, to Mars, your 
mortal enemy.  You want to have 20 of those spies run assassinate operatives, 
but you only want your best Mayhem spies to try those assassinations::

    >>> python bin/assign_spies.py --num 20 --on Mars --top mayhem Earth kill

Valid "Top" Settings
--------------------

The ``--top`` argument ensures that the requested task is run by only your 
best spies.  You don't want to waste your good mayhem guys on intel missions, 
or your good theft guys on politics missions, etc.

When specifying which spies should perform your task with the ``--top`` 
option, you can pass any of the following values:

    - level
    - politics
    - mayhem
    - theft
    - intel
    - offense_rating
    - defense_rating

Force Fresh Data
----------------

Most of the time, before you assign spies, you'll probably first run
:ref:`spies_report` to see what your spies are doing.  This task assignment 
script shares cache data with that spies report script, so this doesn't have 
to re-look-up the spy data that the spy report almost certainly just looked 
up.

However, after this script completes, if it assigned any spies, it will clear 
that cache automatically.  This way, you can go back and re-run the spy report 
script and be sure to see information on your newly-assigned spies.

Full Documentation
------------------

For complete help, see the script's help documentation:

    >>> python bin/assign_spies.py -h

.. autoclass:: lacuna.binutils.libassign_spies.AssignSpies
   :members:
   :show-inheritance:

