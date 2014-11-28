
.. _getting_started_running:

Getting Started Running Scripts
===============================

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
folder, and run the pip installer script::

    python3 bin/get-pip.py

pip is now installed.

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

Ready to Run Scripts
--------------------
At this point, you should be set to run any of the available scripts in the 
``bin/`` directory, by typing::

    python bin/SCRIPTNAME.py


