MontyLacuna
===========


[![Join the chat at https://gitter.im/tmtowtdi/MontyLacuna](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/tmtowtdi/MontyLacuna?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

A Python Client for The Lacuna Expanse.

This is essentially a port of the Perl Games::Lacuna::Client module to Python.  

## TBD
- GET RID of update.py.  I'm tired of babysitting it.  The user can install 
  git and learn to "git clone" and "git pull origin master" or they can just 
  update by re-installing by hand each time.  Trying to replicate "git pull 
  origin master" with a Python script because the user can't be arsed to 
  install git is stupid.
    - The other option is to back up their config files (etc/lacuna.cfg and 
      var/*.bodyabbrv.pkl) somewhere, pull down all of master, extract it 
      somewhere new, put the config files into that new dir, and then direct 
      the user to go there, letting them know they can blow away the old monty 
      dir.  Use "your old stuff is over there --> along with your old log 
      files" as an excuse.
- build_ships.py blows up with an exception if a SY is out of commission 
  (damaged).  
- ships_report.py doesn't appear to be reporting on fighters that have been 
  recalled from a deployment
  - Are we just reporting on Docked ships?  If so, the report should have the 
    option of displaying other tasks, and should make clear what it's 
    displaying.
- see stats.py for how methods should be documented throughout.
- Ack through everything for "CHECK" and fix.
  - Even if you find no CHECK marks, leave this list item here.  I have a tendency to 
    re-add these marks.

