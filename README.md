MontyLacuna
===========

A Python Client for The Lacuna Expanse.

This is essentially a port of the Perl Games::Lacuna::Client module to Python.  

## TBD
- fix .gitignore
    - var/* is no good; we need var/ to get created, that's what the .githold is for.
    - At the same time, we want the contents of the 2 cache dirs, plus all logs and 
      rotated logs, to be omitted from commits.
- Send excavs should cache tested planet and star info.  When running for 'all' planets, 
  if multiple planets are ROFd, it's re-testing the same systems and planets 
    over and over again.  Fix.
- Everything needs to be tested on Windows.  In particular:
  - bin/captcha_test.py
  - installing modules via pip or however it works on windows.
  - Run through the whole Getting Started instruction set on a fresh Python install on 
    Windows to make sure the docs are correct.
- Ack through everything for "CHECK" and fix.
  - Even if you find no CHECK marks, leave this list item here.  I have a tendency to 
    re-add these marks.

