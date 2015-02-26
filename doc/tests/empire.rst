
.. _test_empire:

Empire Tests
============

The empire test suite is currently testing all classes and methods in 
``lib/lacuna/empire.py``.

Before attempting to run this test suite
----------------------------------------
Most of the classes in the suite are being skipped.  This is because the tests 
are destructive; I don't want them being run accidentally.

If you're sure you know what you're doing, comment out the skip decorators 
above the class declarations, then go ahead and run the test.

Running just the empire tests
-----------------------------
From MontyLacuna's root, run these tests with::

    >>> python lib/lacuna/pyt/empire.py

Destructive things done by this suite of tests
----------------------------------------------
- Spend 5 e on each of the boosts (so a total of 40 e)
- Change your account password
  - The new password will be the old password with a "1" on the end.  So if 
    oldpw was "foobar", newpw will be "foobar1"
- Change your account description
  - Same deal as above - a "1" gets tacked on the end
- Change your species description
  - Same deal as above - a "1" gets tacked on the end
  - This test spends 100 E.
- Change your status message
  - Same deal as above - a "1" gets tacked on the end
- Sends an invite to flurble123456@mailinator.com.
  - This isn't really destructive, but it is doing something external.
  - And the test does not confirm that the message was sent, it just confirms 
    that the send attempt doesn't raise an exception.  You'll need to check 
    that mailbox manually if you want to see if it sent or not (it did on a 
    manual check here.)
  - **After running empire tests**, please go delete that message.

Tests that will always be a bit hokey
-------------------------------------
- redeem_essentia_code
  - Tries to redeem a code that's known to already have been used, and tests 
    that the correct exception gets raised.  Without an admin account to 
    create new essentia codes to test with, this will never be a true test.

