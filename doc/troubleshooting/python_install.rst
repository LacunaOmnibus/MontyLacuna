
.. _troubleshoot_python_install:

Troubleshooting Python Install
------------------------------
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
        type "explorer".  This will restart Windows Explorer (and your desktop 
        will reappear).

Open a new CMD window and try to run "python --version" again.

If your system still can't find Python, uninstall it and then re-install it.  
Follow the instructions above carefully, and be sure to check the part about 
registering as default python.  After re-installing, reboot your machine and 
try the ``python --version`` command again after the reboot.


