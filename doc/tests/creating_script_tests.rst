
.. _creating_script_tests:

Creating Script Tests
=====================
If you create a new MontyLacuna script, you may well want to ("you are 
encouraged to") add a test suite to go along with the script, to safeguard 
against regressions.

The instructions here assume that your script follows the conventions used by 
the existing MontyLacuna scripts:

    - Your script imports a library that implements a class that does most of 
      the heavy lifting
    - Your library inherits from :class:`lacuna.binutils.libbin.Script`

The problem with testing MontyLacuna scripts is that most of these scripts 
expect arguments to be passed along on the command line, and your test scripts 
won't be doing that.  So we'll need to make some minor code changes to allow 
your test suite to work without passing arguments at the command line.

Modify your library
-------------------
Your library will need to accept an optional argument, which is a dict named 
``testargs``, and then pass that dict along to the call to your library's 
parent's constructor::

    def __init__( self, testargs:dict = {} ):
    ...
    super().__init__( parser, testargs = testargs )

If you initially created your script and library by copying one of the 
existing MontyLacuna scripts and editing it to suit your needs, there's a good 
chance that code is already there.

Set up your test suite
----------------------
Again, you'll probably be better off copying one of the existing script test 
suites and modifying it for your own use.  These modules live in 
``ROOT/lib/lacuna/test/test_SCRIPTNAME.py``.

Connect to TLE
~~~~~~~~~~~~~~
Your test class will need to inherit from both ``unittest.TestCase`` and 
``lacuna.test.connector.Connector``.  My tests usually import 
``lacuna.test.connector`` as simply ``conn`` to save a little typing.

Create a ``setUpClass()`` method to connect for you::

    class MyTestClass( unittest.TestCase, conn.Connector ):

        @classmethod
        def setUpClass( self ):
            self.tle_connect(self)

The ``setUpClass()`` will be run once when your test suite begins, and will 
create ``self.test_sitter`` and ``self.test_real`` connection objects.

Instantiate your script's main object
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Your test will need to construct an object from your script's library's class, 
and pass along whatever command-line arguments it wants to test out.

For example - to test out the ``excavs_report.py`` script, I need to set up a 
dict containing the command line arguments that script is expecting, and then 
pass along that dict to the constructor.  You need to pass along all arguments 
that the script allows, and also pass along the client you're using::

    args = {
        'client': self.sitter,
        'fresh': True,              # don't want to be reading from and old
                                    # cache for tests.
        'name': self.sitter.planet  # more on this below
    }
    self.er = lib.ExcavsReport( testargs = args )

At this point, ``self.er`` is an ExcavsReport object that we can happily test 
against.  Your tests can create multiple ExcavsReport (or whatever) objects 
with different faked-up command-line arguments so you can test all the 
argument combinations you wish.

Edit your config file
---------------------
Test scripts are going to create two TLE connections; one logged in with a 
sitter password and one logged in with a real password.  These connections 
assume that your config file contains the sections ``test_sitter`` and 
``test_real``. 

You'll need to add those two sections to your config file.  **Make sure that 
both of these sections are connecting to your PT account rather than your US1 
account!**

Empire-specific testing
-----------------------
There's no way around it; some tests are going to require information about a 
specific empire.  The best way to deal with this is going to be by editing the 
config file, instead of having to edit each specific test script.

So, if your test script needs to work as sitter against a specific planet, eg 
``Earth``, you can add a ``planet`` setting to your config file's 
``test_sitter`` section::

    planet: Earth

In your test script, there's an attribute named ``sitter`` that's an object  
representing your sitter login.  That object now has an attribute named 
``planet``::

    print( self.sitter.planet ) # Earth

Different tests will have different config file requirements; you'll need to 
check the documentation for each individual test to see all of the config file 
edits you'll need to make.


