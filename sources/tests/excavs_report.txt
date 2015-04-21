
.. _test_excavs_report:

Excavs Report Tests
===================
This test suite tests ``bin/excavs_report.py``.

Setup
-----
Make sure your config file has a ``test_sitter`` section, pointed at your 
account on PT.

That config section must contain the following settings:
    - test_planet = *Name of one of your planets to run against*

Running the tests
-----------------
From MontyLacuna's root, run these tests with::

    >>> python lib/lacuna/test/test_excavs_report.py

Test module documentation
-------------------------
.. autoclass:: lacuna.test.test_excavs_report.TestExcavsReport
   :members:
   :show-inheritance:
