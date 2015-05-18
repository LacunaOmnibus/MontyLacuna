
.. |as_python_default| image:: images/as_python_default.png
.. |as_python_fixed| image:: images/as_python_fixed.png

.. _getting_started_running:

Getting Started Running Scripts
===============================

Overview of Steps
-----------------

To get MontyLacuna working, you'll have to follow a few steps.  These are 
similar to the steps necessary to setting up the standard Lacuna scripts 
written in Perl.

- Install Python 3

  - :ref:`inst_python_windows`
  - :ref:`inst_python_nonwindows`
  - :ref:`inst_monty`
  - :ref:`inst_pip`
  - :ref:`create_config_file`
  - :ref:`run_test_script`
 
.. _inst_python:

Install Python 3
----------------

.. _inst_python_windows:

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

If that's what you see, then Python has been installed successfully.  If 
that's not what you see, then see the :ref:`troubleshoot_python_install` docs.

.. _inst_python_nonwindows:

Non-Windows
~~~~~~~~~~~

If you're on Linux or Mac, you should already have Python installed.  But make 
sure that you've got Python 3.  Many systems come with Python 2, not 3, and 
MontyLacuna will not work with Python 2.  Python 3 should be available via 
your package manager.

If you do already have python installed on your system, and it's version 2, 
then when you install python version 3, it will probably install the language 
as ``python3``, not just ``python``.  If that's the case, you're going to need 
to actually type ``python3`` anywhere the instructions below tell you to type 
``python``.

.. _inst_monty:

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

.. _inst_pip:

Install pip and Prerequisite Libraries
--------------------------------------
pip is a tool for installing Python libraries.  Installing pip is very easy, 
as MontyLacuna includes a script to install it for you.

Open up a terminal window (on Windows, this means ``CMD.exe``).  Change into 
the root MontyLacuna folder -  the one you just extracted in the previous step 
- and run the pip installer script::

    >>> python bin/get-pip.py
    (remember to actually type 'python3' instead of 'python' if you're on a 
    Linux or Mac machine that already had python version 2 installed).

``pip`` is now installed.

**On a Mac**, pip did get installed, but it may have been named ``pip3`` 
rather than just ``pip``.  Typing ``pip -V`` (that's a capital V) will tell 
you which version of python your pip will update.  If your pip is set to 
update your python2 installation, then check if you have a ``pip3`` and use 
that instead.

There are only three Python libraries to install, ``beaker``, ``pyside``, and 
``requests``, and you install them using ``pip`` by typing these commands one 
at a time::

    >>> pip install beaker
    >>> pip install pyside
    >>> pip install requests

If any of those ``pip`` commands produced errors, see the 
:ref:`troubleshoot_pip_install` docs.

After pip and the prerequisite libraries are installed, leave that CMD window 
open for the next step.

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
Note that, when the script asks you to type your password, it will not 
actually print what you type onto the screen.  You'll type, but you won't see 
anything.  That's OK; it's just doing that to keep your little sister who's 
watching over your shoulder from seeing your password.

.. _run_test_script:

Ready to Test
-------------
At this point, you should be set to run any of the available scripts in the 
``bin/`` directory.  There's a test script that will show you a few details 
about your empire, and requires no arguments.  Try it out by typing::

    python bin/test_script.py

If that tells you "Congratulations", you're all set.  Now you can move on to 
running whatever :ref:`scripts_index` you want.

