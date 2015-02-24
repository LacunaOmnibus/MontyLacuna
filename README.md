MontyLacuna
===========


[![Join the chat at https://gitter.im/tmtowtdi/MontyLacuna](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/tmtowtdi/MontyLacuna?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

A Python Client for The Lacuna Expanse.

This is essentially a port of the Perl Games::Lacuna::Client module to Python.  

## TBD
- send_excavs.py
  - coords seem to be starting from 0|0 regardless of location of sending 
    planet.  See emails to tmtowtdi@gmail.com from Tomas Miko (The 
    Collective).
  - -t/--t arg is now required, not sure how it was documented before, but 
    ensure it's doc'd as required now.
- stations_report
    - think about adding a --spy report.  Include how many are on counter, how 
      many are idle, etc.
- update.py should somehow check to see if an update is needed.
  - Save the latest commit hash from github and see if that's changed when update.py is 
    run?
  - Just download the .zip file always and get a digest of that, and compare it to the zip 
    digest from the last time update.py was run?
  - Just check the date of most recent commit and compare that to the date of the local 
    most recent update?
  - Whatever.  Something along those lines.
- Also, having update.pl NOT respond to -h and behave like all the other 
  scripts is a copout.  Fix it.
- Ack through everything for "CHECK" and fix.
  - Even if you find no CHECK marks, leave this list item here.  I have a tendency to 
    re-add these marks.


