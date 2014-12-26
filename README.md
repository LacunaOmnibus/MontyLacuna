MontyLacuna
===========

A Python Client for The Lacuna Expanse.

This is essentially a port of the Perl Games::Lacuna::Client module to Python.  

## TBD
- Update send_excavs.py to allow for an 'all' planet like build_ships.py uses.
- send_excavs.py will send to a target that's uninhabited, but which has 
  inhabited planets in the same system.  Those will shoot down the excav if 
  they have saws (and everybody has saws).  Need to:
  - Check for any inhabited in the system
  - If any exist, add the star to a bad_stars hash so no other planets in that 
    system will be checked.

- My last run of send_excavs.py with planet 'all' ended in this:
Traceback (most recent call last):
  File "bin/send_excavs.py", line 30, in <module>
    stars = send.get_map_square()
  File "/home/jon/work/MontyLacuna/bin/../lib/lacuna/binutils/libsend_excavs.py", line 178, in get_map_square
    req_cell = self.ring.get_next_cell()
  File "/home/jon/work/MontyLacuna/bin/../lib/lacuna/binutils/libsend_excavs.py", line 459, in get_next_cell
    return next(self.next_cell)
  File "/home/jon/work/MontyLacuna/bin/../lib/lacuna/binutils/libsend_excavs.py", line 468, in _gen_next_cell
    yield Cell( col, row, x, y, self.cell_size )
  File "/home/jon/work/MontyLacuna/bin/../lib/lacuna/binutils/libsend_excavs.py", line 520, in __init__
    self._set_bounding_points()
  File "/home/jon/work/MontyLacuna/bin/../lib/lacuna/binutils/libsend_excavs.py", line 530, in _set_bounding_points
    self.client.user_logger.debug( "This cell is entirely out of bounds." )
AttributeError: 'Cell' object has no attribute 'client'


fix it.



- Everything needs to be tested on Windows.  In particular:
  - bin/captcha_test.py
  - installing modules via pip or however it works on windows.
  - Run through the whole Getting Started instruction set on a fresh Python install on 
    Windows to make sure the docs are correct.
- Ack through everything for "CHECK" and fix.
  - Even if you find no CHECK marks, leave this list item here.  I have a tendency to 
    re-add these marks.

