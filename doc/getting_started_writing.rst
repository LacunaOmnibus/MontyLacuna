
.. _getting_started_writing:

Getting Started Writing Scripts
===============================

Be sure to follow the :ref:`getting_started_running` section first.  This 
section assumes that you're already to the point of being able to run scripts.

Test Scripts
------------
There are a bunch of test scripts in ``INSTALLDIR/t/``.  These are not meant 
to be attached to any test harness, and almost all the code in those scripts 
has been commented out.

Instead of automated unit tests, those are to-be-run-manually test scripts.  
You can run them as you like, but you'll need to edit each one to make sense 
to you, and be careful; some of the example code in those scripts can be 
damaging to your empire.

Those scripts really exist as examples of how to use MontyLacuna.  If you want 
to see how something is done, check there first.

Tell Your Script Where MontyLacuna Lives
----------------------------------------
When you create a new script, you'll need to tell that script how to find the 
MontyLacuna libraries.

Add this to the top of your script::

    import os, sys
    libdir = os.path.abspath(os.path.dirname(sys.argv[0])) + "/../lib"
    sys.path.append(libdir)
    import lacuna

The path to the ``lib/`` directory is relative to the location of your script, 
and this example assumes your script is going to live in ``INSTALLDIR/bin/``.  
If you're going to put your script somewhere else, adjust the path 
accordingly.

Connect a client
----------------
::

    my_client = lacuna.clients.Member(
        config_file = os.path.abspath(os.path.dirname(sys.argv[0])) + "/../etc/lacuna.cfg",
        config_section = 'sitter',
    )

As with the previous step, the path to the config file is relative to the 
location of your script.  Adjust the path accordingly if your script is going 
to live somewhere other than ``INSTALLDIR/bin/``.

Please keep in mind that many of the people using your script may not be very 
technically inclined.  The config file creation script that comes with 
MontyLacuna creates config file sections named ``real`` and ``sitter``.  If 
your script is meant for distribution, it's strongly suggested that you 
specify one of those two names as your ``config_section``.

Logging and Caching
-------------------
Logging and caching facilities are set up for use in your scripts, and are 
both easy to access.  For details, see :ref:`logging` and :ref:`caching`.

Debugging Requests
------------------
If you ever need to see the exact JSON that a given method would send to the 
server, you can assign a ``debugging_method`` on your client, eg::

    client.debugging_method = 'view_profile'
    empire.view_profile()

Once a ``debugging_method`` has been assigned, the next time a method by that 
name is called, the JSON that would normally be passed to the TLE servers will 
instead be dumped to the screen, and the script will terminate immediately, to 
allow you to inspect the JSON dump.

A ``debugging_method`` must be the name of a TLE API method.  Most MontyLacuna 
methods are mirrors of TLE API methods, but not all.  To check if a given 
method is a published TLE API method, check out the TLE API documentation:
https://us1.lacunaexpanse.com/api/

Method Calling
--------------
Almost all MontyLacuna methods require positional, not named, arguments.  

The method documentation includes argument names and types for clarity of what 
data types need to be sent, not as an indication that named arguments can be 
used.

eg The documentation for the Embassy's ``accept_invite`` method looks like 
this:

    **accept_invite(invite_id: int, message: str='', \**kwargs)**

So, to call ``accept_invite``, you'd do something like this::

    embassy.accept_invite( 12345, "Come join my alliance!" )

But you wouldn't do this, because the invite_id has to come before the 
message::

    ### GONNNNG!  Don't do this.
    embassy.accept_invite( message = "Come join my alliance!", invite_id = 12345 )

Example Snippets
----------------

Get your empire
~~~~~~~~~~~~~~~
Your empire object is already part of your client::

    print( "I have used", my_client.empire.rpc_count, "RPCs so far today.")
    profile = my_client.empire.view_profile()
    print( "I am from {} in {}, and my player name is {}.  I have won {} medals."
        .format(profile.city, profile.country, profile.player_name, len(profile.medals.keys()))
    )

Get info on your alliance
~~~~~~~~~~~~~~~~~~~~~~~~~
::

    my_alliance = my_client.get_my_alliance();
    print( "My alliance is named {}, and its ID is {}."
        .format(my_alliance.name, my_alliance.id)
    )

Read mail from your inbox
~~~~~~~~~~~~~~~~~~~~~~~~~
::

    mail = my_client.get_inbox();
    msgs, ttl = mail.view_inbox( {"tags": ["correspondence"]} )
    print( "I have ", ttl, "messages in my inbox.")

Check on one of your planets by name
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
::

    my_planet = my_client.get_body_byname( 'Earth' )
    print( "Earth's ID is", my_planet.id )

Check on one of the buildings based on coordinates
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
::

    pcc = my_planet.get_building_coords( 0, 0 )
    print( "My PCC's ID is", pcc.id )

Check on all of the buildings of a certain type
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
::

    min_level = 1
    min_efficiency = 100
    sps = my_planet.get_buildings_bytype( 'spaceport', min_level, min_efficiency )
    for s in sps:
        print( "This sp is located at ({},{})",format(s.x, s.y) )

Check on just one building of a certain type
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
::

    min_level = 1
    min_efficiency = 100
    sp = my_planet.get_buildings_bytype( 'spaceport', min_level, min_efficiency )[0]

    ### Or, if you don't care about level or efficiency...
    sp = my_planet.get_buildings_bytype( 'spaceport' )[0]

    print( "This space port's ID is {}.".format(sp.id) )

Adding Unit Tests
-----------------
See :ref:`tests_index`.
    
Script Parent Class
~~~~~~~~~~~~~~~~~~~
To create a script similar to the scripts that come bundled with MontyLacuna, 
including command-line argument parsing, your script should inherit from:

.. automodule:: lacuna.binutils.libbin
   :members:
   :show-inheritance:

