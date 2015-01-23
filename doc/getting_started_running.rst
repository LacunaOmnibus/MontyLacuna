
.. |as_python_default| image:: images/as_python_default.png
.. |as_python_fixed| image:: images/as_python_fixed.png

.. _getting_started_running:

Getting Started Running Scripts
===============================

Overview of Steps
-----------------

To get MontyLacuna working, you'll have to follow a few steps.  These are 
similar to the steps necessary to setting up the standard Lacuna scripts 
written in Perl, but these steps should be simpler.

- Install Python 3
- Install MontyLacuna
- Install Python libraries
- Create a config file
- Run a test script

Install Python 3
----------------

Windows
~~~~~~~
You can download Python 3 from `ActiveState's website.  
<http://www.activestate.com/activepython/downloads>`_  Make sure you download 
version **3.whatever**, *not* version **2.whatever**.  

During installation, the installer will show you what features will be 
installed.  In some cases, *Register as Default Python* will be unselected, as 
indicated by the red X in the picture:

    |as_python_default|

We want that turned on.  Click on the little down arrow just to the right of 
the red X, and set this feature to be installed.  When you're done, the window 
should look like this:

    |as_python_fixed|

From here on, just click the Next button until the installer completes.

After the installer is complete, open up a new ``CMD`` window (if you already 
had one open, close it and open a new one) and type::

    python --version

That should respond with something like this::

    Python 3.4.1.0

If that's what you see, then Python has been installed successfully.

Troubleshooting Python Install
------------------------------
If python installed properly in the previous step, skip this section - scroll 
down to the :ref:`install_monty` section.

Especially if you've installed Python before, it's possible that, after 
installing it this time, the ``python --version`` command will tell you 
something like::

    'python' is not recognized as an internal or external command, operable 
    program or batch file.

Most likely, everything is fine, but Windows just hasn't caught up to the
new install yet.  The easiest way to fix this is just to reboot.

Another option is to restart Windows Explorer in your Task Manager:

    - Make sure to close any open CMD windows you might have lying around.
    - Hit Ctrl-Alt-Del, and choose "Task Manager".
    - Windows 8

      - Right-click the Windows Explorer entry, and choose "Restart"
    - Any other version of Windows

      - Highlight "explorer.exe", and chose "End Process"

        - This is going to look a little scary - all of the icons on your 
          desktop are going to disappear!  It's not a problem; your desktop is 
          actually displayed by explorer.exe, and you just ended that process.  
          Your icons are fine, you just can't see them right now.

        - Restart explorer.exe - from the Task Manager, select File... Run and 
          type "explorer".  This will restart Windows Explorer (and your 
          desktop will reappear).

Open a new CMD window and try to run "python --version" again.

If your system still can't find Python, uninstall it and then re-install it.  
Follow the instructions above carefully, and be sure to check the part about 
registering as default python.  After re-installing, reboot your machine and 
try the ``python --version`` command again after the reboot.

Non-Windows
~~~~~~~~~~~

If you're on Linux or Mac, you should already have Python installed.  But make 
sure that you've got Python 3.  Many systems come with Python 2, not 3, and 
MontyLacuna will not work with Python 2.  Python 3 should be available via 
your package manager.

.. _install_monty:

Install MontyLacuna
-------------------
Download your preferred filetype.  For most people, that will be the "zip" 
file.

    ====  ===============
    Type  Link
    ====  ===============
    Zip   `Download zip file <https://github.com/tmtowtdi/MontyLacuna/zipball/master>`_
    Tar   `Download tar file <https://github.com/tmtowtdi/MontyLacuna/tarball/master>`_
    ====  ===============

- Open the ``zip`` file using whatever unzip tool you like.  It contains just 
  one folder, named something like ``tmtowtdi-MontyLacuna-1234abc``.  Drag 
  that out to ``My Documents`` on your computer.

  - On Windows, you don't need to go download an unzip tool.  Double-click on 
    the .zip file after you've downloaded it, and Windows will open it up like 
    it's a regular folder.

- After dragging that oddly-named folder into ``My Documents``, rename it to 
  simply ``MontyLacuna``.

Install pip and Prerequisite Libraries
--------------------------------------
pip is a tool for installing Python libraries.  Installing pip is very easy, 
as MontyLacuna includes a script to install it for you.

Open up a terminal window (on Windows, this means ``CMD.exe``).  Change into 
the root MontyLacuna folder -  the one you just extracted in the previous step 
- and run the pip installer script::

    >>> python bin/get-pip.py

*NOTE* -- please don't get clever and change into the ``bin/`` folder and try 
to run that as just::

    >>> python get-pip.py
    (Don't do this)

Anyway, after running that script, pip is now installed.

There are only two Python libraries to install, ``requests`` and ``beaker``, 
and you install both of them using ``pip`` by typing these two commands one at 
a time::

    >>> pip install requests
    >>> pip install beaker

Troubleshooting Pip Install
---------------------------
As with the Python install, if those two ``pip install ...`` commands seemed 
to work, you can skip down to the :ref:`create_config_file` section.

If you ran one of the ``pip install`` commands above, and it told you 
something like::

    Unknown or unsupported command 'install'

...here's what happened.  You probably have Strawberry Perl installed, and 
Strawberry Perl has, for some bizarre reason, a completely different 
program named 'pip', and that's what you're running right now.

The fix is easy enough.  Instead of just typing ``pip``, you need to type 
the full path to your Python pip program.  So do this::

    c:\Python34\Scripts\pip install requests
    c:\Python34\Scripts\pip install beaker

Leave that CMD window open for the next step.

.. _create_config_file:

Create A Config File
--------------------
For this next step, you'll need to know your Lacuna password.  And if you have 
a sitter password setup, you should know that too.  Make sure you have those 
in front of you before trying to create your config file.

Using the CMD window you left open from the previous step, run the config file 
creation script::

    python bin/create_config_file.py

That will ask you several questions, and then create your config file for you.

Ready to Test
-------------
At this point, you should be set to run any of the available scripts in the 
``bin/`` directory.  There's a test script that will show you a few details 
about your empire, and requires no arguments.  Try it out by typing::

    python bin/test_script.py

If that tells you "Congratulations", you're all set.  Now you can move on to 
running whatever :ref:`scripts_index` you want.

