
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

Shared Cache
------------
Very often, you'll run :ref:`spies_report` before running this script.  This 
script shares cache data (which persists for one hour) with that report 
script, which will mean that this script will run more quickly if you've just 
run the spies report script.

After this script completes, it always clears out that shared cache, because 
it knows that spies have just been assigned new tasks, rendering the data in 
that cache invalid.

So you can always run the spy report script after running this and be sure 
that you're seeing fresh data.

However, there's also a case where the shared cache can cause a problem with this script:
    - You run :ref:`spies_report` to check on your spies.
    - You send some of your spies to a nearby target and wait for them to 
      arrive.
    - You try to use this script to assign those spies to a task.

If the spies you sent reached their destination in under an hour, then when 
you run this assignment script, it'll be reading that cached data and will 
still think those spies are in their old locations.

To fix this, simply send the ``--fresh`` argument to this script.  So the 
process would look something like this::

    >>> py bin/spies_report.py Earth
    Check the output, send some of your spies to your mortal enemy planet 
    Mars, which is nearby, so the trip only takes a few minutes.  Wait for 
    them to arrive.

    >>> py bin/assign_spies.py --on Mars --fresh Earth kidnap
    Tell the spies that you just sent to Mars to run the Abduct Operatives 
    task.  Since you passed that "--fresh" argument, the script will see your 
    newly-placed spies on Mars.

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

Full Documentation
------------------

For complete help, see the script's help documentation:

    >>> python bin/assign_spies.py -h

.. autoclass:: lacuna.binutils.libassign_spies.AssignSpies
   :members:
   :show-inheritance:

