MontyLacuna
===========

A Python Client for The Lacuna Expanse.

This is essentially a port of the Perl Games::Lacuna::Client module to Python.  

## Working On
- turnkey.py

## TBD
- Everything needs to be tested on Windows.  In particular:
  - bin/captcha_test.py
  - installing modules via pip or however it works on windows.
  - Run through the whole Getting Started instruction set on a fresh Python install on 
    Windows to make sure the docs are correct.
- Ack through everything for "CHECK" and fix.
  - Even if you find no CHECK marks, leave this list item here.  I have a tendency to 
    re-add these marks.

## jof
- He's trying MontyLacuna out now.  Things he found:
  - He did try running scripts from inside the bin/ directory, so they couldn't find his 
    config file.  Need more explicit instructions to really drive home the fact that where 
    the user is sitting on the filesystem matters.
    - It might be useful to add a "find_config_file()" or some such to try to avoid this 
      problem.
