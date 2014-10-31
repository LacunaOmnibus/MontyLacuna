MontyLacuna
===========

Python Client for The Lacuna Expanse

This is essentially a port of the Perl Games::Lacuna::Client module to Python.  
No attempt is being made to preseve the same API used by GLC, but the goal is 
to replicate all of the functionality.

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
    - oopified
  - inteltraining
  - libraryofjith
  - mayhemtraining
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
- Fix intelligence.py to use the Spy class (and anything else that touches spies).
- Fix planetarycommand.py to use the Plan class (and anything else that touches plans).
- A prisoner or two floating around us1 1.1.  Use them to test trade.py and transporter.py
    - get_prisoners()
- Any method that's returning a list of dicts (ships, spies, whatever) should be fixed to 
  return instead a list of objects.
  - I started doing this somewhere around the time I was working on security.py.  
    Everything listed below that (in the list of completed buildings above) should be 
    DingTRT.  Everthing listed above that should be looked at.
- The Building class should be renamed to MyBuilding, so we can use "Building" for a much 
  more generic building base classname.

