
.. _tests_index:

Unit Tests
==========

Existing tests
--------------
.. toctree::
    :maxdepth: 1

    empire
    excavs_report

Running all tests
-----------------
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

Creating script tests
---------------------
See :ref:`creating_script_tests`

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

