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
  - CHECK It might make sense to replace this with urllib, since it's standard - one less 
    thing for the user to have to install
- beaker
  - pip install beaker

## Complete
Nothing.

## Glossary
- Standard search string
  - Several methods allow you to search for an item by name (a star, an empire, etc).  
    Some of these methods allow a "search string" instead of a full name.  A search string 
    must be at least three characters long.  All objects whose names match that string 
    will be returned:
        Search string: "Ear"
        Returns: [ "Earth", "Ears is a strange name for a planet", "Earp, Wyatt" ]

    These methods return *lists*, not single objects.  You often really want a single 
    object; just remember that you're getting a list.
- TLE date format
  - Many methods include dates as part of their returns.  TLE dates are in the format:
    "01 31 2010 13:09:05 +0000"

## Working
"working" means that all functionality exists, and quickie scripts appear to 
work, but it hasn't been fully tested yet.

- Captcha
  - Including session persistence between scripts
- Client
  - Guest
  - Member
- Empire
  - oopified
- Inbox
  - oopified
- Map
  - oopified
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
  - blackholegenerator
  - development
  - distributioncenter
    - CHECK I haven't got one of these on US1.
  - embassy
    - What I could test works, but testing of several methods would require making a test 
      account and inviting/rejecting/etc that account.  Currently I'm unable to create a 
      test account on PT.  I have no reason to believe that these untested methods don't 
      work, they just haven't actually been confirmed to work.
    - CHECK so along with testing, this still needs oopificiation
  - energyreserve
  - entertainment
  - foodreserve
  - geneticslab
    - CHECK need PT back up to oopify this
  - intelligence
  - inteltraining
  - libraryofjith
  - mayhemtraining
  - mercenariesguild
    - About halfway oopified
    - CHECK need PT back up to oopify this
  - miningministry
  - missioncommand
  - network19
  - observatory
    - Mostly oopified
    - CHECK need PT back up to test abandoning all probes
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
- The caching right now is very naive - every call sent to the server is curried.  The 
  cache actually needs to be cleared periodically
  - What's there now probably won't hurt any short quickie scripts, though it probably 
    won't help those much either.  But it would hurt a long-running program, eg LacunaWaX.
- Everything needs to be tested on Windows.  In particular:
  - bin/captcha_test.py
- Ack through everything for "CHECK" and fix.
- Whenever we instantiate a MyBuilding object, we're calling view() on that building 
  automatically - I'm not convinced that's what should be happening.  At the very least, 
  we should be caching the results.
- I'm going to want a "convert_date()" method, which'll probably mean I'll want a TZ 
  attribute of clients.Member.  And I'll need to learn about python date handling.
- For some stupid reason I keep referring to dicts as "structs".  Ack for "struct" and fix 
  that.


