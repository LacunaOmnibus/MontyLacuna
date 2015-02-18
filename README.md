MontyLacuna
===========

A Python Client for The Lacuna Expanse.


This is essentially a port of the Perl Games::Lacuna::Client module to Python.  

## TBD
- update.py should somehow check to see if an update is needed.
  - Save the latest commit hash from github and see if that's changed when update.py is 
    run?
  - Just download the .zip file always and get a digest of that, and compare it to the zip 
    digest from the last time update.py was run?
  - Just check the date of most recent commit and compare that to the date of the local 
    most recent update?
  - Whatever.  Something along those lines.
- Some sort of update script
    - Something that does the same job as "git pull origin master", but doesn't require 
      the user to install git.
        - for list of files and/or directories:
            - back up and archive existing stuff
            - pull down newest latest greatest from github using http
            - leave the (dated) backup lying around somewhere (var/ probably)
        - The point is to save the user from having to re-download the whole package, 
          re-create their config file again, and lose any customizations they might have 
          made to the code.
- Ack through everything for "CHECK" and fix.
  - Even if you find no CHECK marks, leave this list item here.  I have a tendency to 
    re-add these marks.

