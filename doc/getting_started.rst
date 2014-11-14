
Getting Started
===============

Install
-------
Info on how to install the package.

Create config file
------------------
The :doc:`config_file` document describes the config file pretty well, but CHECK I 
also want to flesh out and document ``bin/create_default_config_file.py``.


Set up your environment
-----------------------
I'm wanting to end up in a situation where this section is not necessary.  No 
"use lib" statements needed; the user installs the package and then starts 
using it right away.

But if that can't happen for whatever reason, this section needs to describe 
how to properly set the path to the lib, via "use lib" or setting ENV 
variables, or virtualenv, or whatever.

Connect a client
----------------

::

    my_client = lac.clients.Member(
        config_file = "/home/me/MontyLacuna/etc/lacuna.cfg",
        config_section = 'my_sitter',
    )

Get your empire
---------------
Your empire info is already part of your client.

::

    print( "I have used", my_client.empire.rpc_count, "RPCs so far today.")
    profile = my_client.empire.view_profile()
    print( "I am from {} in {}, and my player name is {}.  I have won {} medals."
        .format(profile.city, profile.country, profile.player_name, len(profile.medals.keys()))
    )

Get info on your alliance
-------------------------

::

    my_all = my_client.get_my_alliance();
    print( "My alliance is named", my_all.name )

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
    





