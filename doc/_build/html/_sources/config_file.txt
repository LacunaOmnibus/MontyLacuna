
Config File
===============
When creating a Guest or Member object (from the clients module), you can send 
all of your credentials manually (host, username, password, protocol, etc), or 
you can just send a config filename and the section of that config file to 
use.

The config file is preferred because you can add it to your .gitignore file to 
be sure not to accidentally check in your passwords.

The DEFAULT section isn't strictly required, but having it allows you to add 
as many other sections as you'd like, and only include the information in 
those sections that differ from what appears in DEFAULT.

An example config file:

.. code-block:: ini

    [DEFAULT]
        proto = https
        host = us1.lacunaexpanse.com
        testhost = pt.lacunaexpanse.com
        api_key = anonymous
        show_captcha = True
        sleep_on_call = 1
        sleep_after_error = True
        warn_on_sleep = True
        logfile = var/tle.log

    [my_account]
        username = My Empire Name
        password = My Real Password

    [my_sitter]
        password = My Sitter Password

    [some_alliance_mate]
        username = My Alliance Mate's Empire Name
        password = My Alliance Mate's Sitter Password
        logfile = var/ally_mate.log

    [playtest]
        host = ${DEFAULT:testhost}
        username = My PT Empire Name
        password = My PT Password

- proto
    - The protocol to connect with.  Either ``http`` or ``https``.  https is 
      more secure, but slower, and may cause connection problems in some rare 
      cases.  It's recommended you use https, and only switch to http if 
      there's a problem.
- host
    - The hostname to connect to.  Either ``us1.lacunaexpanse.com`` or 
      ``pt.lacunaexpanse.com``
    - ``testhost`` is included in my example config file, but it's not used by 
      the connection library.  Instead, I'm using it later in the example 
      config file itself under the ``playtest`` section.
- api_key
    - Just leave this as ``anonymous``.  A key is required, and you can sign 
      up for your own key if you want to, but it seems to be largely unused.
- show_captcha
    - Boolean.  Defaults to True.
    - When True, if anything is done that requires a captcha be solved, the 
      captcha image will be fetched and displayed to the user in a browser, 
      and the user will be prompted to enter the solution.  This is usually 
      what you want.  However, if you're using MontyLacuna to create something 
      other than a terminal application (eg a web app), you'll need to manage 
      the captcha display yourself, and should set this to False.
- sleep_on_call
    - Integer.  Defaults to 1.
    - Number of seconds to sleep after each request is made to the TLE server.  
      This is meant to keep you from hitting the 60 RPC per minute limit.  
      Setting it to 0 to not sleep at all will speed up your scripts, but you 
      run a much greater risk of hitting that limit.
- sleep_after_error
    - Boolean.  Defaults to True.
    - If you do hit the 60 RPC per minute limit error and this is set to True, 
      your script will go to sleep for a minute, then pick up where it left 
      off.  If this is set to False and you hit that limit, your script will 
      raise a ServerError exception.
- warn_on_sleep
    - True or False.  Defaults to True.
    - If the script sleeps because of the 60 RPC per minute limit, and this is 
      True, a message will be printed to the screen (STDOUT) letting you know 
      the script is pausing.  Not knowing why your script is suddenly taking 
      so long is frustrating.

Those other sections ("other" meaning "everything but DEFAULT") can be named 
whatever makes sense to you.

*Note* that the `[playtest]` section interpolates the `testhost` value from 
the `DEFAULT` section, and uses that value as its own `host` value.  That 
interpolation format will work for any other setting as well.  Or, you could 
certainly just type `pt.lacunaexpanse.com` there instead of using the variable 
interpolation.

To connect:

::

    import lacuna as lac

    my_real_connection = lac.users.Member(
        config_file    = "etc/lacuna.cfg",
        config_section = 'my_account',
    )

    my_sitter_connection = lac.users.Member(
        config_file    = "etc/lacuna.cfg",
        config_section = 'my_sitter',
    )

    my_friends_connection = lac.users.Member(
        config_file    = "etc/lacuna.cfg",
        config_section = 'some_alliance_mate',
    )

This should make it easy, especially for those who run scripts for multiple 
friends, to keep all credentials in a single file and just change the 
`config_section` value in your script depending on the account you want to 
run.

