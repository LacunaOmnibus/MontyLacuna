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
  - miningministry
  - missioncommand
  - network19
  - observatory
  - oracleofanid
  - orestorage
  - park
  - planetarycommand
  - politicstraining
  - security (left off here - totally un-worked-on)
  - spaceport (done)

## Incomplete/Not Started
- Payments
 - There's a real good chance this will never be worked on as part of this 
   project.
- Announcement

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

