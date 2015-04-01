MontyLacuna
===========

[![Join the chat at https://gitter.im/tmtowtdi/MontyLacuna](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/tmtowtdi/MontyLacuna?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

A Python Client for The Lacuna Expanse.

This is essentially a port of the Perl Games::Lacuna::Client module to Python.  

## TBD
- see stats.py for how methods should be documented throughout.
- Add a "total storage" item to the output of the station report so we know how we're 
  looking for BFG usage.
  - I've done this, but haven't updated any docu.  Do that.
- If the user does not enter a sitter during config file creation, the sitter 
  section does still get created in the config file, with what is obviously 
  NOT the user's password.

  BUT most of the scripts use the sitter section by default.  So in that case, 
  none of the scripts will work since the user's sitter password in the config 
  file is wrong.

******
  I need a good solution to this.  Maybe require that the user have a sitter 
  when they run the config file creator.  Include instructions on how to set 
  it and retrieve it (Etn said he "didn't know his sitter", even though I have 
  it recorded, which means he had one but didn't know how to get at it).
******

- Ack through everything for "CHECK" and fix.
  - Even if you find no CHECK marks, leave this list item here.  I have a tendency to 
    re-add these marks.

