
clients
=======

Connecting a client should always be your first step in any script.  There are 
two types of clients - Guest and Member.  

Guest clients are not yet logged in, and exist so that new players can set up 
a new account.  For the purposes of scripting, you'll probably never need to 
use a Guest account.

So what you'll almost always be doing, is creating a Member client, by using a 
specific section in a config file::

    import lacuna

    client = lacuna.clients.Member(
        config_file     = "etc/lacuna.cfg"
        config_section  = "sitter"
    )


.. automodule:: lacuna.clients
   :members:
   :show-inheritance:

