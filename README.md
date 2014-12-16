MontyLacuna
===========

A Python Client for The Lacuna Expanse.

This is essentially a port of the Perl Games::Lacuna::Client module to Python.  

## Currently working on 
- bin/send_excavs.py

## TBD
- Everything needs to be tested on Windows.  In particular:
  - bin/captcha_test.py
  - installing modules via pip or however it works on windows.
  - Run through the whole Getting Started instruction set on a fresh Python install on 
    Windows to make sure the docs are correct.

- Ack through everything for "CHECK" and fix.
  - Even if you find no CHECK marks, leave this list item here.  I have a tendency to 
    re-add these marks.

- AS Python installer does NOT have "register as default python" checked by default - this 
  is what adds python to the PATH.  Include instructions to the user to fix that setting 
  that during the install wizard.
  - I added a blurb, but I need a screenshot and correct verbiage.

- Try to pass a writ named "Not controlled by a station" at one of our stations and see if 
  that shows up any differently than the retval from a star that's really not being 
  controlled by a station.

