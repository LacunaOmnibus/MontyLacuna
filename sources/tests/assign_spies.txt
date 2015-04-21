
.. _test_assign_spies:

Assign Spies Tests
==================
This test suite tests ``bin/assign_spies.py``.

Setup
-----
Make sure your config file has a ``test_sitter`` section, pointed at your 
account on PT.

That config section must contain the following settings:
    - test_planet = *Name of one of your planets to run against*

This test will assign a single spy on the specified planet to Counter 
Espionage.

Running the tests
-----------------
From MontyLacuna's root, run these tests with::

    >>> python lib/lacuna/test/test_assign_spies.py

It takes 20-30 seconds to run the entire test suite including the captcha.

Test module documentation
-------------------------
.. autoclass:: lacuna.test.test_assign_spies.TestAssignSpies
   :members:
   :show-inheritance:
