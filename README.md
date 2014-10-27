MontyLacuna
===========

Python Client for The Lacuna Expanse

This is essentially a port of the Perl Games::Lacuna::Client module to Python.  
No attempt is being made to preseve the same API used by GLC, but the goal is 
to replicate all of the functionality.

The main goal is to help me learn Python, but I'd like to end up with a fully 
working package.

## Prerequisites
- requests
  - pip install requests
  - CHECK It might make sense to replace this with urllib, since it's standard.

## Complete
Nothing.

## Working
"working" means that all functionality exists, and quickie scripts appear to 
work, but it hasn't been fully tested yet.

- Captcha
  - Including session persistence between scripts
- Client
  - Guest
  - Member
- Empire
- Inbox
- Map
- Stats
- Body
- Buildings
  - "all functionality" is a bit of a stretch here.  The Buildings base class 
exists, and stub classes exist for all buildings in the game.  I need to work 
through those building stubs to make them each do whatever-it-is they're each 
supposed to do.
  - Existing base classes:
    - Building
      - All buildings inherit from this
      - SingleStorage
        - Base class for storage buildings for single-type resources (energy, water).
      - MultiStorage
        - Base class for storage buildings for multi-type resources (food, ore).
  - archaeology
  - blackholegenerator
  - development
  - distributioncenter
  - embassy
    - What I could test works, but testing of several methods would require making a test 
      account and inviting/rejecting/etc that account.  Currently I'm unable to create a 
      test account on PT.  I have no reason to believe that these untested methods don't 
      work, they just haven't actually been confirmed to work.
  - energyreserve
  - entertainment
  - foodreserve
  - geneticslab
  - intelligence
  - libraryofjith
  - mercenariesguild

  - CHECK ALL OF THE ABOVE FOR CORRECT @Building.set_building_status decorators; I think I 
    may have missed a bunch.

  - miningministry
  - missioncommand
  - network19

  - spaceport
   


## Incomplete/Not Started
- Payments
 - There's a real good chance this will never be worked on as part of this 
   project.
- Announcement
- Captcha

## TBD
- Add another attribute to the client classes - warn_on_sleep.  Default it to true.  If a 
  call to send() needs to sleep because of the 60 RPC per minute limit, issue a warning 
  letting the user know that's what's happening and is why their script is taking so long.  
  Unless this attribute has been specifically set to false, in which case issue no 
  warning.

- Everything needs to be tested on Windows.  In particular:
 - bin/captcha_test.py

- Ack through everything for "CHECK" and fix.

- Go back to intelligence.py and see about creating a Spy class.

- call_building_named_meth() decorator is already in the Building class; we don't need the 
  "building" in there.  change it to just "call_named_meth" and fix all calls.

- map.Star() is currently reading the 'bodies' dict list attribute, keeping it, and also 
  creating the 'body_objects' object list attribute.  I see no need to keep both of those 
  attributes, and suddenly switching to the name "body_objects" is confusing.  Get rid of 
  "body_objects", replace "bodies" with a list of objects instead of the original list of 
  dicts, and fix all calls.
    - I've already set the 'bodies' attribute to the same list of objects currently 
      pointed to by the 'body_objects' attribute; all new code should use that 'bodies' 
      attribute.  Just need to get rid of existing calls to body_objects, then delete the 
      attribute.

