
.. _getting_started:

Getting Started
===============

Install Python 3
----------------
If you're on Windows, you can download Python 3 from `ActiveState's website.  
<http://www.activestate.com/activepython/downloads>`_  Make sure you download 
version 3.whatever, NOT version 2.whatever.

If you're on Linux or Mac, you probably already have Python installed.  But 
make sure that you've got Python 3.  Many systems come with Python 2, not 3, 
and MontyLacuna will not work with Python 2.  Python 3 should be available via 
your package manager.

Install MontyLacuna
-------------------
- Download the ``.zip`` file from `the MontyLacuna home page 
  <http://tmtowtdi.github.io/MontyLacuna/>`_.

- Open the ``zip`` file using whatever unzip tool you like.  It contains just 
  one folder - drag that out to ``My Documents`` on your computer.

- The folder you just dragged and dropped will have a long name, something 
  like ``tmtowtdi-MontyLacuna-1234abc``.  You can leave that as is or rename 
  it to whatever you want, but I strongly suggest you just rename it to 
  ``MontyLacuna``.

  - The rest of this documentation will assume that's what you named it.

Install pip and Prerequisite Libraries
--------------------------------------
pip is a tool for installing Python libraries.  Installing pip is very easy, 
as MontyLacuna includes a script to install it for you.

Open up a terminal window (on Windows, this means CMD.exe) to the MontyLacuna 
folder, and run pip installer script::

    python3 bin/get-pip.py

There are only two Python libraries to install, ``requests`` and ``beaker``, 
and you install both of them using ``pip``::

    pip install requests
    pip install beaker

Leave that CMD window open for the next step.

Create A Config File
--------------------
Using the CMD window you left open from the previous step, run the config file 
creation script::

    python3 bin/create_config_file.py

That will ask you several questions, and then create your config file for you.

Script Runners Stop Here
------------------------
**If you're only planning on running scripts, not writing them, you can stop 
reading here; you're done!**

Test Scripts
------------
There are a bunch of test scripts in ``INSTALLDIR/t/``.  These are not meant 
to be attached to any test harness, and almost all the code in all of the 
scripts has been commented out.  

Instead of automated unit tests, those are to-be-run-manually test scripts.  
You can run them as you like, but you'll need to edit each one to make sense 
to you, and be careful; some of the example code in those scripts can be 
damaging to your empire.

Those scripts really exist as examples of how to use MontyLacuna.

Tell Your Script Where MontyLacuna Lives
----------------------------------------
When you create a new script, you'll need to tell that script how to find the 
MontyLacuna libraries.

Add this to the top of your script::

    import os, sys

    libdir = os.path.abspath(os.path.dirname(__file__)) + "/../lib"
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
        config_file = os.path.abspath(os.path.dirname(__file__)) + "/../etc/lacuna.cfg",
        config_section = 'sitter',
    )

As with the previous step, the path to the config file is relative to the 
location of your script.  Adjust the path accordingly if your script is going 
to live somewhere other than ``INSTALLDIR/bin/``.

Please keep in mind that many of the people using your script may not be very 
technically inclined.  The config file creation script that comes with 
MontyLacuna creates config file sections named ``real`` and ``sitter``; if 
your script is meant for distribution, it's strongly suggested that you 
specify one of those two names as your ``config_section``.

Example Snippets
----------------

Get your empire
~~~~~~~~~~~~~~~
Your empire info is already part of your client::

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

Check on one of the buildings on that planet
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
::

    pcc = my_planet.get_building_coords( 0, 0 )
    print( "My PCC's ID is", pcc.id )
    
Next Steps
~~~~~~~~~~
From here, check on some of the existing sample scripts in ``bin/``, and the 
full documentation in :ref:`home`
