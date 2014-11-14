MontyLacuna
===========

Python Client for The Lacuna Expanse

This is essentially a port of the Perl Games::Lacuna::Client module to Python.  
No attempt is being made to preseve the same API used by GLC, but I'd like to 
replicate all of the functionality.

The main goal is to help me learn Python, but I'd like to end up with a fully 
working package.

## Prerequisites
- virtualenv
  - You want to do this before any other installing, so the module installs will install 
    to your virtual environment.
  - $ sudo apt-get install python-virtualenv
  - Again, this probably doesn't count as a true prereq, but it's something I did.
  - After installing virtualenv, I created one for this project with:
    - $ virtualenv -p /usr/bin/python Python3
    - $ source Python3/bin/activate
      - Now "python script.py" will call Python3/bin/python.
    - You can turn that virtualenv off with just $ deactivate
- pip
  - This gets installed by virtualenv, so if you're using that, you're good.
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
CHECK add this to an .rst file.

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
  - CHECK this definitely still needs work.
  - And repair_list() needs to be tested; I need to snark myself on PT I guess.
- Alliance
  - CHECK this definitely still needs work.
- Captcha
  - May be oopified, may not.  CHECK.
- Clients
  - May be oopified, may not.  CHECK.
- Empire
  - oopified, but still needs testing in a couple methods - see CHECK.
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
- The logfile attribute of clients is meant to be optional, but ISTR getting an explosion 
  on a test at some point where I didn't have a logfile set.  Confirm that setting a 
  logfile is optional.
- Figure out how to generate HTML documentation from my docstrings.
- Figure out how to install this puppy (setup.py?)

## Documentation
http://sphinx-doc.org/tutorial.html
https://pythonhosted.org/an_example_pypi_project/sphinx.html#full-code-example

- First run only:
  - Create ROOT/doc/
  - In ROOT:
    - sphinx-quickstart (this starts a question-and-answer section):
      - root path: ./doc
      - I entered my name, the name of the project, and version 0.1.
      - I chose 'y' for the questions about autodoc and viewcode.
      - All else I accepted the defaults.
  - in ROOT/doc/:
    - Edit conf.py (which was just created):
      - Line 21 (ish):
        - sys.path.insert(0, os.path.abspath('../lib'))
      - That should tell Sphinx where my code lives
  - I created these by hand:
    - bc.rst
    - body.rst
    - building.rst
    - captcha.rst
    - clients.rst
    - config_file.rst
    - empire.rst
    - getting_started.rst
    - inbox.rst
    - map.rst
    - stats.rst
- To generate docu based on docstrings:
  - in ROOT:
    - sphinx-apidoc -o doc/ lib/ lacuna
      - However, I don't think I'm using this at this point.  CHECK I need to clean up and 
      - http://sphinx-doc.org/invocation.html#invocation-apidoc
      - Re-run that anytime you update docstrings in the modules.
      - This creates several more .rst files in doc/
        - lacuna.rst
        - lacuna.buildings.rst
        - modules.rst
        - my_validate_email.rst
    - Of those generated files, the only one I'm explicitly adding to the main toctree is 
      "my_validate_email".  I don't want lacuna or modules listed there at all.  I've 
      added lacuna.buildings to the toctree of buildings.rst.
      - Add these lines under the toctree:: directive:
        - lacuna
        - my_validate_email
    - Now, when you generate the HTML docu, links to your API docs will be included.
- Each time you want to update the generated documentation:
  - in ROOT/doc:
    - make html
  - The generated HTML ends up in {underscore}build/html/.  Those HTML files 
    reference CSS and JS files that get produced in _static/.
    - For whatever reason, github pages does not like the underscore on that 
      _static/ directory - it refuses to host files from there.
    - So before publishing to gh-pages:
      - Rename _static to static
      - Change all references in all .html files (recursively) from _static to 
        static.
        - CHECK I don't have a decent tool for doing this yet.
  - To publish to gh-pages:
    - $ cp -Rip doc/{underscore}build/html ~/Desktop
    - $ git co gh-pages
    - $ rm -rf html_docs
    - $ mv ~/Desktop/html ./html_docs
    - $ git add -A html_docs
    - $ git commit -m "docs!"
    - $ git push origin gh-pages






