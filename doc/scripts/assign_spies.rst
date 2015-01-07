
.. _assign_spies:

Assign Spies
============

Assigns spies based on a single planet, in bulk, to a specified task.  

Note that this does not send any spies to a target.  You must make sure that 
your spies are in the correct locations before attempting to use this to 
assign them to tasks.

See also :ref:`spies_report`, to check out what your spies are doing right 
now, then use this script to assign them to some other task.

Assign all Idle spies on Earth to Counter Espionage::

    >>> python bin/assign_spies.py Earth "Counter Espionage"

Assign only 20 spies on Earth to Counter Espionage::

    >>> python bin/assign_spies.py --num 20 Earth "Counter Espionage"

Assign only your 20 highest-level spies on Earth to Counter Espionage::

    >>> python bin/assign_spies.py --num 20 --top level Earth "Counter Espionage"

    (This is actually exactly the same as the previous example, since 'level'
    is the default value for the --top option.)

Assign 20 spies who are currently doing Counter Espionage to Idle::

    >>> python bin/assign_spies.py --num 20 --doing "Counter Espionage" Earth "Idle"

Assume you've sent all 90 of your spies from your planet, Earth, to Mars, your 
mortal enemy.  You want to have 20 of those spies run assassinate operatives, 
but you only want your best Mayhem spies to try those assassinations::

    >>> python bin/assign_spies.py --num 20 --on Mars --top mayhem Earth "Assassinate Operatives"

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

All Possible Tasks
------------------

You obviously won't be able to run all possible tasks with all possible spies, 
but here's a list of all tasks available in-game:

    - Idle
    - Bugout
    - Counter Espionage
    - Security Sweep
    - Political Propaganda
    - Gather Resource Intelligence
    - Gather Empire Intelligence
    - Gather Operative Intelligence
    - Hack Network 19
    - Sabotage Probes
    - Rescue Comrades
    - Sabotage Resources
    - Appropriate Resources
    - Assassinate Operatives
    - Sabotage Infrastructure
    - Sabotage Defenses
    - Sabotage BHG
    - Incite Mutiny
    - Abduct Operatives
    - Appropriate Technology
    - Incite Rebellion
    - Incite Insurrection

Task Abbreviations
------------------

The names of some of the spy tasks are somewhat onerous to type (kinda like 
typing the phrase "somewhat onerous").  Anyway, casing does not matter when 
specifying task names ("idle" == "iDlE" == "Idle").  Also, some abbreviations 
for tasks have been added:

    - Counter Espionage

      - counter

    - Political Propaganda

      - pp
      - prop

    - Gather Resource Intelligence
    
      - gather resint
      - get resint

    - Gather Empire Intelligence

      - gather empint
      - get empint

    - Gather Operative Intelligence

      - gather opint
      - get opint

    - Hack Network 19

      - hack net19
      - hack

    - Sabotage Probes

      - sab probes

    - Rescue Comrades

      - rescue

    - Sabotage Resources

      - sabotage res
      - sab res

    - Appropriate Resources

      - appropriate res
      - app res

    - Assassinate Operatives

      - ass op
      - kill

    - Sabotage Infrastructure

      - sab infra

    - Sabotage Defenses

      - sab def

    - Sabotage BHG

      - sab bhg

    - Incite Mutiny

      - mutiny

    - Abduct Operatives

      - abduct op
      - kidnap

    - Appropriate Technology

      - app tech

    - Incite Rebellion

      - rebellion
      - rebel

    - Incite Insurrection

      - insurrection
      - insurrect
      - insurect (because somebody is going to miss that second ``r``.)

Because of these abbreviations, we could shorten the previous example about 
assassinating operatives to::

    >>> python bin/assign_spies.py --num 20 --on Mars --top mayhem Earth kill

Force Fresh Data
----------------

Most of the time, before you assign spies, you'll probably first run
:ref:`spies_report` to see what your spies are doing.  This script shares 
cache data with that spies report script, so this doesn't have to re-look-up 
the spy data that the spy report almost certainly just looked up.

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

