MontyLacuna
===========

A Python Client for The Lacuna Expanse.

This is essentially a port of the Perl Games::Lacuna::Client module to Python.  

## Working on
post_starter_kits.py
    - Need trade posting methods for SST, but it's working for the TM now.

    - All of the named kits have been tested:
        - res
        - stor
        - mil
        - ute
        - beach
        - deco
        - full
        - big

    - You can set the price with or without quotes - tested both of these:
        - py bin/post_starter_kits.py bmots01 --price "2.2" beach
        - py bin/post_starter_kits.py bmots01 --price 2.2 beach

    - I have not tested changing the plan levels.

    - Once it's fully working, I need to figure out some reasonable facility for allowing 
      the user to create his own kit combos.

    ~ The documentation file exists and has been started, but it's absolutely not 
    finished.


## TBD
- Everything needs to be tested on Windows.  In particular:
  - bin/captcha_test.py
  - installing modules via pip or however it works on windows.
  - Run through the whole Getting Started instruction set on a fresh Python install on 
    Windows to make sure the docs are correct.
- Ack through everything for "CHECK" and fix.
  - Even if you find no CHECK marks, leave this list item here.  I have a tendency to 
    re-add these marks.

