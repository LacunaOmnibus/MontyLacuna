
.. _test_send_excavs:

Send Excavs Tests
==================
This test suite tests ``bin/send_excavs.py``.

Setup
-----
Make sure your config file has a ``test_sitter`` section, pointed at your 
account on PT.

That config section must contain the following settings:
    - test_planet = *Name of one of your planets to run against*
    - send_excavs_ptypes = *Any planet type, eg "p35"*
    - send_excavs_max_ring = ``1``
    - send_excavs_max_send = ``1``

Running the tests
-----------------
From MontyLacuna's root, run these tests with::

    >>> python lib/lacuna/test/test_send_excavs.py

It takes about two minutes to run the entire test suite.

Test module documentation
-------------------------
.. autoclass:: lacuna.test.test_send_excavs.TestSendExcavs
   :members:
   :show-inheritance:

.. autoclass:: lacuna.test.test_send_excavs.TestBodyCache
   :members:
   :show-inheritance:

.. autoclass:: lacuna.test.test_send_excavs.TestPoint
   :members:
   :show-inheritance:

.. autoclass:: lacuna.test.test_send_excavs.TestCell
   :members:
   :show-inheritance:

