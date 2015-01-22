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
  - The ${DEFAULT:test_host} appears to be giving his config file parser a hard time.  
    This might be a Windows thing, but it also might be that I installed a third-party 
    config parser library that I never recorded.
    - I need to try running through from scratch, including using a brand new virtualenv.
      - OK, done.  No issues here.  So it could be that my /usr/bin/python3 is modified 
        from the default, or there's a difference between python 3.4.0 (which I have) and 
        3.4.1.0 (which is what's on ActiveState's website), or there's a difference 
        between windows and linux.
    - I think that the best bet is to just get rid of the ExtendedInterpolation 
      altogether.  I'm finding hints that the newest version of configparser may not be 
      supporting that.  Even if that's not the case, ExtendedInterpolation seems to be the 
      source of the problem, and it's not providing that much benefit.

