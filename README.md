MontyLacuna
===========

A Python Client for The Lacuna Expanse.

This is essentially a port of the Perl Games::Lacuna::Client module to Python.  

## Working On
assign_spies.py.  This works as-is right now, but I'd like to add some sort of special 
argument that assigns all idle spies on all planets to Counter Espionage.
    Actually, it shouldn't work at all anymore, as I added the beginning of a structure to 
    do this "counter everywhere" bit.

No point in having Idle spies, and I don't want to have to re-run this damn thing manually 
for every planet.

Also, I have virtually no logging in assign_spies.py, and spies_report.py might be short 
on the same -- update both of those to add some more status info.


## TBD
- Everything needs to be tested on Windows.  In particular:
  - bin/captcha_test.py
  - installing modules via pip or however it works on windows.
  - Run through the whole Getting Started instruction set on a fresh Python install on 
    Windows to make sure the docs are correct.
- Ack through everything for "CHECK" and fix.
  - Even if you find no CHECK marks, leave this list item here.  I have a tendency to 
    re-add these marks.

