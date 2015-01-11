
.. _config_file:

Config File
===============
Normally when you connect a client, you'll send along the path to a config 
file, and which section in that file you want to connect with::

    my_client = lacuna.clients.Member(
        config_file = os.path.abspath(os.path.dirname(sys.argv[0])) + "/../etc/lacuna.cfg",
        config_section = 'sitter',
    )

The easiest way to create a config file with a new install is to run 
``bin/create_config_file.py``.  It will ask you a few basic questions and then 
create a working config file based on your responses.

After that config file has been created, you can feel free to edit it as 
desired.  Often you'll want to add a section for an alliance mate for whom 
you're running scripts; see the ``some_alliance_mate`` section in the example 
below.

You can add as many additional named sections as you'd like.

.. code-block:: ini

    [DEFAULT]
    api_key = anonymous
    host = us1.lacunaexpanse.com
    logfile = us1.log
    proto = https
    show_captcha = True
    sleep_on_call = 1
    sleep_after_error = True
    testhost = pt.lacunaexpanse.com
    warn_on_sleep = True

    [real]
    username = My Empire Name
    password = My Real Password

    [sitter]
    username = My Empire Name
    password = My Sitter Password

    [some_alliance_mate]
    username = My Alliance Mate's Empire Name
    password = My Alliance Mate's Sitter Password
    logfile = ally_mate.log

    [playtest]
    host = ${DEFAULT:testhost}
    username = My PT Empire Name
    password = My PT Password

Setting Descriptions
--------------------
- **api_key**

  - Just leave this as ``anonymous``.  A key is required, and you can sign up 
    for your own key if you want to, but it seems to be largely unused.

- **host**

  - The hostname to connect to.  Either ``us1.lacunaexpanse.com`` or 
    ``pt.lacunaexpanse.com``

- **logfile**

  - The name of your logfile.  This file will live in ``ROOT/var/``, and will 
    be created if it doesn't already exist.  *Don't* include a path here, just 
    a filename.

- **proto**

  - The protocol to connect with.  Either ``http`` or ``https``.  ``https`` is 
    more secure, but may cause connection problems in some rare cases.  It's 
    recommended you use ``https``, and only switch to ``http`` if there's a 
    problem.

- **show_captcha**

  - Boolean.  Defaults to True.
  - When True, if anything is done that requires a captcha be solved, the 
    captcha image will be fetched and displayed to the user in a browser, and 
    the user will be prompted to enter the solution.  This is usually what you 
    want.  However, if you're using MontyLacuna to create something other than 
    a terminal application (eg a web app), you'll need to manage the captcha 
    display yourself, and should set this to False.

- **sleep_after_error**

  - Boolean.  Defaults to True.
  - If you do hit the 60 RPC per minute limit error and this is set to True, 
    your script will go to sleep for a minute, then pick up where it left off.  
    If this is set to False and you hit that limit, your script will raise a 
    ServerError exception.

- **sleep_on_call**

  - Integer.  Defaults to 1.
  - Number of seconds to sleep after each request is made to the TLE server.  
    This is meant to keep you from hitting the 60 RPC per minute limit.  
    Setting it to 0 to not sleep at all will speed up your scripts, but you 
    run a much greater risk of hitting that limit.

- **warn_on_sleep**

  - True or False.  Defaults to True.
  - If the script sleeps because of the 60 RPC per minute limit, and this is 
    True, a message will be printed to the screen (STDOUT) letting you know 
    the script is pausing.  Not knowing why your script is suddenly taking so 
    long is frustrating.

Default Values
--------------
The ``[DEFAULT]`` section is the only one whose name matters to MontyLacuna.  
Any of the settings that appear in that ``[DEFAULT]`` section can also appear 
in any other named section.  However, most settings do not need to appear in 
each section.  Any setting that does not appear in a given section will simply 
use the value listed in ``[DEFAULT]``.  Note that the ``[some_alliance_mate]`` 
section contains its own ``logfile`` setting, while most of the other sections 
don't.  This means that any scripts that connect using the 
``[some_alliance_mate]`` section will write to the ``var/ally_mate.log`` log 
file, while scripts that connect using any other section will write to the 
default ``var/us1.log`` log file.

Although the names of the other sections don't matter to MontyLacuna, remember 
that the default config file creation script that everybody else using 
MontyLacuna uses is going to create sections named ``real`` and ``sitter``.  
If you're going to be writing scripts that are meant to be run by other 
people, you'll probably want your client connection to use one of those names.

Section Variable Interpolation
------------------------------
The ``[playtest]`` section interpolates the ``testhost`` value from the 
``DEFAULT`` section, and uses that value as its own ``host`` value.  That 
interpolation format will work for any other setting as well.  Or, you could 
certainly just type ``pt.lacunaexpanse.com`` there instead of using the 
variable interpolation.

