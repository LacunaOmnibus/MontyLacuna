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
- sphinx
  - pip install sphinx
  - This isn't really a prerequisite of using MontyLacuna, but it's (likely) what I'm 
    using to generate the documentation.

## Complete
Nothing.

## Glossary
This should all end up somewhere more reasonable than this file eventually.

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

- Body
  - May be oopified, may not.  CHECK.
- Alliance
  - May be oopified, may not.  CHECK.
- Captcha
  - May be oopified, may not.  CHECK.
- Clients
  - May be oopified, may not.  CHECK.
- Empire
  - oopified
- Inbox
  - oopified
- Map
  - oopified
- Stats
  - Mostly oopified.  I didn't fully test (and therefore didn't fully oopify) 
    this just because I don't see it being too useful.  Still, it should be 
    completed.

- Buildings
  - "all functionality" is a bit of a stretch here.  The Buildings base class 
exists, and stub classes exist for all buildings in the game.  I need to work 
through those building stubs to make them each do whatever-it-is they're each 
supposed to do.
  - archaeology
  - blackholegenerator
  - development
  - distributioncenter
  - embassy
  - energyreserve
  - entertainment
  - foodreserve
  - geneticslab
  - intelligence
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
  - thedillonforge
  - thefttraining
  - themepark
  - trading (base class)
    - trade (trade ministry)
    - transporter (sst)
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
  - The more I look at what's there, the more I think it exists as an example of how 
    beaker (the caching module) works.  I don't think the cache-every-call that I've got 
    in there now is sensible at all.
  - CHECK the caching problem is way worse than I thought - the cache is _not_ always being 
    cleared after each run; I apparently do not understand how __del__ works.  For now, 
    I've commented the caching out entirely.
    - Instead of caching every request, I'm going to need to be more selective.  Which is 
      more work, but makes more sense.
- Everything needs to be tested on Windows.  In particular:
  - bin/captcha_test.py
- Ack through everything for "CHECK" and fix.
- Whenever we instantiate a MyBuilding object, we're calling view() on that building 
  automatically - I'm not convinced that's what should be happening.  At the very least, 
  we should be caching the results.
- lacuna.bc.SubClass is idiotically named.  It's meant as a full-coverage superclass, not 
  a subclass.  Do something about that name.
- Figure out how to generate HTML documentation from my docstrings.
- Figure out how to install this puppy (setup.py?)


