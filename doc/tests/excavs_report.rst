
.. _test_excavs_report:

Excavs Report Tests
===================
This test suite tests ``bin/excavs_report.py``.

Setup
-----
Make sure your config file has both ``test_sitter`` and ``test_real`` 
sections, both pointed at your account on PT.

Add a ``planet`` setting to your config file's ``test_sitter`` section.  This 
``planet`` setting will be the planet name you want to send to the excavator 
report script to test, so it can either be the name of a planet or the word 
``all``.

Running the tests
-----------------
From MontyLacuna's root, run these tests with::

    >>> python lib/lacuna/test/test_excavs_report.py

