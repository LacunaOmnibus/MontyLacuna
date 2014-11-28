MontyLacuna
===========

Python Client for The Lacuna Expanse

This is essentially a port of the Perl Games::Lacuna::Client module to Python.  
No attempt is being made to preseve the same API used by GLC, but I'd like to 
replicate all of the functionality.

The main goal is to help me learn Python, but I'd like to end up with a fully 
working package.

## Prerequisites
- Prereqs for documentation creation; not needed by script runners or writers, 
  only needed if you want to generate the docu yourself.
  - sphinx
    - pip install sphinx
  - Sphinx Read The Docs! theme
    - pip install sphinx_rtd_theme

## Unfinished
- trading (base class)
  - I purposely skipped some methods in both trade.py and transporter.py.  
    They'll never be used and I'm getting bored.  Add them if you're feeling 
    productive.  The skipped methods are noted in comments at the top of both 
    files.
- Space Station Modules
  - policestation

## Incomplete/Not Started
I'm not seeing any need to worry about either of these.
  - Payments
  - Announcement

## TBD
- logging
  - Look at LoggerAdapters - the way the request log is being dealt with (the extra) 
    sucks.
    https://docs.python.org/3.4/howto/logging-cookbook.html#using-loggeradapters-to-impart-contextual-information
  - There's also a RotatingFileHandler handler - that's what I should be using, or people 
    are going to end up with way-too-big logfiles.
- Everything needs to be tested on Windows.  In particular:
  - bin/captcha_test.py
  - installing modules via pip or however it works on windows.
  - Run through the whole Getting Started instruction set on a fresh Python install on 
    Windows to make sure the docs are correct.
- Ack through everything for "CHECK" and fix.
  - Even if you finish this, leave this list item here.  I have a tendency to re-add these 
    marks.
- I'm going to need at least a few useful scripts in bin/ before making this public.
  - starting to play with build_ships.py.

## Building the Documentation
http://sphinx-doc.org/tutorial.html
https://pythonhosted.org/an_example_pypi_project/sphinx.html#full-code-example

- First run only:
  - In ROOT:
    - sphinx-quickstart (this starts a question-and-answer section):
      - root path: ./doc
      - I entered my name, the name of the project, and version 0.1.
      - I chose 'y' for the question about autodoc.
      - All else I accepted the defaults.
  - in ROOT/doc/:
    - Edit conf.py (which was just created):
      - Line 21 (ish):
        - sys.path.insert(0, os.path.abspath('../lib'))
      - That tells Sphinx where the code lives
  - To generate docu based on docstrings:
    - in ROOT:
      - sphinx-apidoc -o doc/ lib/
        - You do not have to manually create doc/ first.
        - http://sphinx-doc.org/invocation.html#invocation-apidoc
        - This creates several more .rst files in doc/
          - lacuna.rst
          - lacuna.buildings.rst
          - modules.rst
          - my_validate_email.rst
      - Of those generated files, the only one I'm explicitly adding to the main toctree 
        is "my_validate_email".  I don't want lacuna or modules listed there at all.  I've 
        added lacuna.buildings to the toctree of buildings.rst.
    - That doesn't get any modules in lib/lacuna/buildings/SUBDIR/, like the LCOT or Space 
      Station modules.
      - To get those specifically, do something like this:
        - sphinx-apidoc -o test/ lib/lacuna/buildings/ss_modules
      - That'll create test/, which will contain your module .rst files.  You're going to 
        want to edit those by hand; they'll list the module names as eg "artmuseum module" 
        instead of "lacuna.buildings.artmuseum module".  Copy the contents of those test/ 
        files into wherever you want them in your existing docu, and then get rid of 
        test/.
  - All of the other .rst files in doc/ were not created automatically, but by hand.  If 
    you add a new module, you'll want to copy one of the existing .rst files and edit it 
    appropriately for your new module.

- To publish the docs generated on the master branch to gh-pages:
  - The HTML pages produced by "make html" end up in {underscore}build/html/.  Those HTML 
    files contain links to _modules/, _sources/, and _static/.  For whatever reason, 
    github pages does not like the underscore on the front of directory names - it refuses 
    to host files from there.  These underscore directories and the links to them are what 
    fix_underscores.pl is fixing.
  - $ pwd
    /home/jon/work/MontyLacuna/doc
  - $ make html
  - $ perl fix_underscores.pl
  - $ cp -Rip {underscore}build/html ~/Desktop
  - $ cd ..
  - $ git status
    - Commit any changes to master
  - $ git co gh-pages
  - $ rm -rf html
  - $ mv ~/Desktop/html ./
  - $ git add -A html
    - There are directories in master containing files in .gitignore.  Since those files 
      don't get commited to master, their directories don't get removed when checking out 
      gh-pages.  So don't just "git add -A .", or you'll add that extraneous crap that has 
      nothing to do with gh-pages.  Just "git add -A html".
  - $ git commit -m "docs!"
  - $ git push origin gh-pages
  - $ git co master
  - Wait a $time_period (Github claims it may take up to 10 minutes, but I've never had it 
    take more than a few seconds), and then go look at your pretty docs online.























