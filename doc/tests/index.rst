
.. _tests_index:

Unit Tests
==========

Status
------

I'm currently working on tests for the MyEmpire class.  Once that's to a 
reasonable state, I want to add tests for other classes as well.

Many methods of MyEmpire are not being tested at all.  The methods tested are 
just information returners, while the ones being skipped would change the 
empire in one way or another (spend E, change profile, etc).

I'm thinking that it would probably make sense to force all tests to run on PT 
rather than US1, so we wouldn't care as much about messing up the testing 
empire.

Running tests
-------------

From the root, run the MyEmpire class tests with::

    >>> python pyt/myempire.py

TBD
---
I haven't figured out how to run multiple test scripts yet, since only one 
exists.  But I'm assuming there's some sort of test harness that will run all 
of my test scripts.

List of existing test scripts
-----------------------------

.. toctree::
   :maxdepth: 2

   my_empire

