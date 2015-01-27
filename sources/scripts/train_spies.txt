
.. _train_spies:

Train Spies
===========

Assigns Idle spies to training tasks, either on a single planet or across your 
whole empire.

See also :ref:`spies_report`, to check out what your spies are doing right 
now.

Assign the 10 Idle spies with the *highest* intel ratings (but still under the 
max) on Earth to further Intel Training:: 

    >>> python bin/train_spies.py Earth intel

Assign the 20 Idle spies with the *highest* intel ratings (but still under the 
max) on Earth to further Intel Training:: 

    >>> python bin/train_spies.py --num 20 Earth intel
    The default number to be assigned per skill is 10, but you can change that 
    number if desired.

Assign the 20 Idle spies with the *lowest* intel ratings (but still under the 
max) on Earth to further Intel Training:: 

    >>> python bin/train_spies.py --num 20 --lvl bad Earth intel
    By default, the guys who already have the highest score in the requested 
    skill are trained first (--lvl good).  But if, instead of a few 
    highly-trained spies, you want a bunch of less-well-trained, but better 
    than average, spies, you can specify "--lvl bad".

The ``--num`` argument is a "topoff" -type argument.  The script is going to 
assume that you want a *total* of ``--num`` spies in training.  So if you have 
9 spies in Intel training, and want to round that off to 10, this *will not 
work*::

    >>> python bin/train_spies.py --num 1 Earth intel
    This will eventually tell you:
        Any training buildings you have on Earth are currently full.

...That's not going to add one more spy.  Instead, it's going to ensure that 
you have at least 1 spy in training (which you do, since 9 is at least 1).  
Instead, what you want to do is tell the script that you want a total of 10 
spies doing Intel Training::

    >>> python bin/train_spies.py --num 10 Earth intel
    And there was much rejoicing.

Assign 10 spies to each of the training buildings you have on Earth.  This 
works fine even if you don't have all four possible training buildings::

    >>> python bin/train_spies.py Earth all

Assign 10 spies to intel training on all of the colonies in your empire::

    >>> python bin/train_spies.py all intel

Assign 10 spies to each type of skill training on all of the colonies in your 
empire::

    >>> python bin/train_spies.py all all
    So if Earth has Intel and Mayhem training buildings, this will train a 
    total of 20 spies on Earth.  And if Venus has Politics, Mayhem, and Theft 
    training buildings, this will train a total of 30 spies on Venus.  etc.  
    across all of the colonies in your empire.

Taking Spies out of Training
----------------------------

If you've set some spies to train already, and want to take them off training 
for whatever reason, you'll use :ref:`assign_spies` rather than this script.  
To take 10 spies on Earth who are currently doing Intel training and assign 
them to the Idle task instead::

    >>> python bin/assign_spies.py --num 10 --doing inttrain Earth idle

See the :ref:`assign_spies` docs for more details.

Cache
-----
This script uses two caches.  The 'my_colonies' cache just lists out the names 
of the colonies in your empire, and isn't something you have to worry about 
unless you've just colonized a new (or lost an old) colony.

The second cache helps keep track of the spies themselves, and isn't shared 
with any other script.  The only time I've seen an issue with this was when I 
stopped a run partway through because I realized that all of the spies on my 
planet were still named "Agent Null".  I went off to rename them, but when I 
came back to re-run this training script, it still thought that they were 
named "Agent Null".

You can always ensure that you're getting brand new, fresh data at the start 
of each run, by passing the ``--fresh`` argument.

Full Documentation
------------------

For complete help, see the script's help documentation:

    >>> python bin/train_spies.py -h

.. autoclass:: lacuna.binutils.libtrain_spies.TrainSpies
   :members:
   :show-inheritance:

