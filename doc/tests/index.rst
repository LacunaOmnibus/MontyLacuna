
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

Setting up to run tests
-----------------------
Test scripts are going to connect to using the config file sections named 
``test_real`` and ``test_sitter``.  Those sections do not get created by the 
config file creator script, so you'll need to test them yourself.  *Be sure 
that those new sections are connecting to PT*, and make sure that the account 
to which you're connecting has a good supply of E (ask an admin; they'll give 
you a bunch).

CAUTION
-------
Some of these tests are going to be fairly destructive to your empire - 
they're going to spend your E, change your empire description, downgrade and 
demolish buildings, etc.

**DO NOT run these tests using your real game account!**

Running tests
-------------
To run all tests, use ``nose``::

    >>> nosetests

This requires that you've installed nose first (``pip install nose``).  

*However*, before you just go blindly running all tests using ``nose``, be 
sure to check the docs for each test suite.  Some of the test cases are being 
skipped by default because of their destructive nature; you'll need to 
manually un-skip them if you want them to run.

nose will autodiscover the tests provided they exist in files named 
``test_SOMETHING.py``.  nose's documentation uses a lot of talk about how 
clever it is at discovering tests, but putting test modules in a directory 
named ``test`` and subclassing from unittest.TestCase was not enough of a hint 
for nose; the test module filename has to actually begin with ``test_``.

Individual test suites can be run individually; see the docs on each below.

TBD
---
I haven't figured out how to run multiple test scripts yet, since only one 
exists.  But I'm assuming there's some sort of test harness that will run all 
of my test scripts.

List of existing test suites
----------------------------

.. toctree::
   :maxdepth: 2

   empire

