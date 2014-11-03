MontyLacuna
===========

Python Client for The Lacuna Expanse

This is essentially a port of the Perl Games::Lacuna::Client module to Python.  
No attempt is being made to preseve the same API used by GLC, but I'd like to 
replicate all of the functionality.

The main goal is to help me learn Python, but I'd like to end up with a fully 
working package.

## Prerequisites
- pip
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
  - Mostly oopified.  I didn't fully test (and therefore didn't fully oopify) this just 
    because I don't see it being too useful.  Still, it should be completed.
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
    - oopified
  - blackholegenerator
    - oopified
  - development
    - cancel oopified
    - CHECK The two subsidize methods still need to be oopified
  - distributioncenter
    - CHECK I haven't got one of these on US1.
  - embassy
    - What I could test works, but testing of several methods would require making a test 
      account and inviting/rejecting/etc that account.  Currently I'm unable to create a 
      test account on PT.  I have no reason to believe that these untested methods don't 
      work, they just haven't actually been confirmed to work.
    - CHECK so along with testing, this still needs oopificiation
  - energyreserve
    - oopified
  - entertainment
    - oopified
  - foodreserve
    - oopified
  - geneticslab
    - CHECK need PT back up to oopify this
  - intelligence
    - oopified
  - inteltraining
    - oopified
  - libraryofjith
    - oopified
  - mayhemtraining
    - oopified
  - mercenariesguild
    - About halfway oopified
    - CHECK need PT back up to oopify this
  - miningministry
    - oopified
  - missioncommand
    - oopified
  - network19
    - oopified
  - observatory
  - oracleofanid
  - orestorage
  - park
  - planetarycommand
  - politicstraining
    - oopified
  - security
  - shipyard
  - spaceport
  - ssla
  - subspacesupplydepot
    - Thoroughly untested.  Unless you're creating a complete game client (in which case 
      you should have control over a working server), you'll never use this anyway so I'm 
      OK with leaving this as-is.
  - thedillonforge
  - thefttraining
    - oopified
  - themepark
  - trading (base class)
    - trade
    - transporter
    - I purposely skipped some methods in both trade and transporter.  They'll never be 
      used and I'm getting bored.  Add them if you're feeling productive.  The skipped 
      methods are noted in comments at the top of both files.
 - recycler (base class)
    - wasteexchanger
    - wasterecycling

## Incomplete/Not Started
- Payments
 - There's a real good chance this will never be worked on as part of this 
   project.
- Announcement

## TBD
- Everything needs to be tested on Windows.  In particular:
  - bin/captcha_test.py
- Ack through everything for "CHECK" and fix.
- Finish "oopifying" the retvals of all of the building classes.
  - Everything from security.py on down should be OK.
  - PT is down right now, and I'm not willing to destroy my US1 empire in the name of 
    testing.  So find CHECK marks in the building list above once PT comes back and 
    finish.
- I'm describing the "standard TLE search string" in multiple places, with slightly 
  different verbiage each time.  Define that somewhere more common.
    - ack for "standard TLE" and ">= 3" etc
- Investigate the main __init_.py.  I don't think it needs all the imports 
  that are in there.
- A prisoner or two floating around us1 1.1.  Use them to test trade.py and transporter.py
    - get__prisoners()
- Whenever we instantiate a MyBuilding object, we're calling view() on that building 
  automatically - I'm not convinced that's what should be happening.  At the very least, 
  we should be caching the results.

