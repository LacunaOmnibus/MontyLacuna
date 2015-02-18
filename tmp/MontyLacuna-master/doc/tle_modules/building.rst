
Building
========

The various building modules all inherit from either the 
:class:`lacuna.building.Building` or, more often, 
:class:`lacuna.building.MyBuilding` classes.

Each individual building module has a variable named ``path``.  That variable 
is going to show up in the documentation for most of those buildings.  It's 
been documented in one or two, but not all, and the documentation will always 
be more or less the same:

        ``This variable determines which TLE module gets accessed by this
        MontyLacuna module.  Don't change it.``

Here and there you'll encounter methods that state that they require a captcha 
be filled out.  As long as you're working on some sort of command-line script, 
the captcha will be displayed to the user and handled automatically -- you 
won't need to do anything in your code to handle the captchas yourself.

.. toctree::
   :maxdepth: 1

   buildings/beach/index
   buildings/lcot/index
   buildings/permanent/index
   buildings/ss_modules/index
   buildings/training/index
   buildings/callable/index
   buildings/boring/index

.. automodule:: lacuna.building
   :members:
   :show-inheritance:

