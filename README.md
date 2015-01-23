MontyLacuna
===========

A Python Client for The Lacuna Expanse.

This is essentially a port of the Perl Games::Lacuna::Client module to Python.  

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
    - This shouldn't be a problem.  With no args, the script should look for 
      "../etc/lacuna.cfg" relative to the bin directory, NO MATTER WHERE YOU STARTED FROM.  
      And if you pass a --file arg, the script will look in ROOT/bin/, ROOT/etc/ and ROOT/ 
      for whatever filename was passed in.
  - The ${DEFAULT:test_host} appears to be giving his config file parser a hard time.  
    This might be a Windows thing, but it also might be that I installed a third-party 
    config parser library that I never recorded.
    - The exact cause of his problem, the ExtendedInterpolation, is just a guess on my 
      part based on tracebacks he'd pasted for me.  Since I'm not able to replicate any of 
      his problems, and ExtendedInterpolation is still active, I don't know what's causing 
      his issues.

- I can't replicate any of the above.
    - 64 bit Windows 8
    - Tried both 64 bit and 32 bit AS Python 3.4.1.0
      - On each attempt, after uninstalling the previous python installs, I deleted 
        c:\Python34\
    - For both Python versions, I walked through the instructions and ended up being able 
      to run both ships_report.py and spies_report.py just fine.

