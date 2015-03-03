
.. _test_send_excavs:

Send Excavs Tests
==================
This test suite tests ``bin/send_excavs.py``.

Setup
-----
Make sure your config file has a ``test_sitter`` section, pointed at your 
account on PT.

That config section must contain the following settings:
    - planet = *Name of one of your planets to run against*
    - send_excavs_ptypes = *Any planet type, eg "p35"*
    - send_excavs_max_ring = ``1``
    - send_excavs_max_send = ``1``

Running the tests
-----------------
From MontyLacuna's root, run these tests with::

    >>> python lib/lacuna/test/test_send_excavs.py

It took about two minutes to run the entire test suite shortly after a restart 
of PT.  YMMV depending upon your internet connection, your machine's speed, 
how fast PT is running at the moment, whether or not the Saben saw his shadow, 
etc.

