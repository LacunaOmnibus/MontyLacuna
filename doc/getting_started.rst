
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

Create A Config File
--------------------
Open up a terminal window (on Windows, this means CMD.exe) to the MontyLacuna 
folder, and run the config file creation script::

    python3 bin/create_config_file.py

That will ask you several questions, and then create your config file for you.

Script Runners Stop Here
------------------------
**If you're only planning on running scripts, not writing them, you can stop 
reading here; you're done!**

Tell Your Script Where MontyLacuna Lives
----------------------------------------
When you create a new script, you'll need to tell that script how to find the 
MontyLacuna libraries.

Assuming that your script is going to be in ``INSTALLDIR/bin/``, add this to 
the top of the script::

    import os, sys

    libdir = os.path.abspath(os.path.dirname(__file__)) + "/../lib"
    sys.path.append(libdir)

    import lacuna

Connect a client
----------------
::

    my_client = lacuna.clients.Member(
        config_file = os.path.abspath(os.path.dirname(__file__)) + "/../etc/lacuna.cfg",
        config_section = 'sitter',
    )

Please keep in mind that many of the people using your script may not be very 
technically inclined.  The config file creation script that comes with 
MontyLacuna creates config file sections named ``real`` and ``sitter``; if 
your script is meant for distribution, it's strongly suggested that you 
specify one of those two names as your ``config_section``.

Get your empire
---------------
Your empire info is already part of your clien ::

    print( "I have used", my_client.empire.rpc_count, "RPCs so far today.")

    profile = my_client.empire.view_profile()
    print( "I am from {} in {}, and my player name is {}.  I have won {} medals."
        .format(profile.city, profile.country, profile.player_name, len(profile.medals.keys()))
    )

Get info on your alliance
-------------------------
::

    my_alliance = my_client.get_my_alliance();
    print( "My alliance is named", my_alliance.name )

Read mail from your inbox
-------------------------
::

    mail = my_client.get_inbox();
    msgs, ttl = mail.view_inbox( {"tags": ["correspondence"]} )
    print( "I have ", ttl, "messages in my inbox.")

Check on one of your planets by name
------------------------------------
::

    my_planet = my_client.get_body_byname( 'Earth' )
    print( "Earth's ID is", my_planet.id )

Check on one of the buildings on that planet
--------------------------------------------
::

    pcc = my_planet.get_building_coords( 0, 0 )
    print( "My PCC's ID is", pcc.id )
    
Next Steps
----------
From here, check on some of the existing sample scripts in ``bin/``, and the 
full documentation in :ref:`home`
