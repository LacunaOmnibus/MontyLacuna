
.. _troubleshoot_pip_install:

Troubleshooting Pip Install
---------------------------
If you ran one of the ``pip install`` commands noted in the 
:ref:`getting_started_running` docs, and it told you something like::

    Unknown or unsupported command 'install'

...here's what happened.  You probably have Strawberry Perl installed, and 
Strawberry Perl has, for some bizarre reason, a completely different 
program named 'pip', and that's what you're running right now.

The fix is easy enough.  Instead of just typing ``pip``, you need to type 
the full path to your Python pip program.  So do this::

    c:\Python34\Scripts\pip install requests
    c:\Python34\Scripts\pip install beaker

