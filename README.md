MontyLacuna
===========

A Python Client for The Lacuna Expanse.

This is essentially a port of the Perl Games::Lacuna::Client module to Python.  


"""
AS Python installer does NOT have "register as default python" checked by 
default - this is what adds python to the PATH.  Include instructions to the 
user to fix that setting that during the install wizard.
    I added a blurb, but I need a screenshot and correct verbiage.

Try to pass a writ named "Not controlled by a station" at one of our stations and see if 
that shows up any differently than the retval from a star that's really not being 
controlled by a station.
"""





## Currently working on 
- bin/send_excavs.py

## TBD
- Everything needs to be tested on Windows.  In particular:
  - bin/captcha_test.py
  - installing modules via pip or however it works on windows.
  - Run through the whole Getting Started instruction set on a fresh Python install on 
    Windows to make sure the docs are correct.

- Ack through everything for "CHECK" and fix.
  - Even if you find no CHECK marks, leave this list item here.  I have a 
    tendency to re-add these marks;

## Building the Documentation
http://sphinx-doc.org/tutorial.html
https://pythonhosted.org/an_example_pypi_project/sphinx.html#full-code-example

- To generate docu based on docstrings:
  - sphinx-apidoc -o test/ lib/lacuna/buildings/ss_modules (or whatever)
  - That'll create test/, which will contain your module .rst files.  You're going to want 
    to edit those by hand.  Copy the contents of those test/ files into wherever you want 
    them in your existing docu, and then get rid of test/.

- To publish the docs generated on the master branch to gh-pages:
  - This procedure will remove any files in the master branch's .gitignore file.  This 
    includes your logs and lacuna.cfg file.  The procedure below assumes you don't care 
    too much about the log files; those are going to go away.  But re-creating your 
    lacuna.cfg file each time is a pain, so that gets backed up and restored.

  - ``$ cd doc``
  - ``$ make html``
  - ``$ perl fix_underscores.pl``
    - The HTML pages produced by "make html" end up in {underscore}build/html/. They 
      contain links to _modules/, _sources/, and _static/.  Github pages refuses to host 
      files from dirs starting with underscores.  These underscore directories and the 
      links to them are what fix_underscores.pl is fixing.
  - ``$ cp -Rip {underscore}build/html ~/Desktop``
  - ``cp etc/lacuna.cfg ~/Desktop``
  - ``$ cd ..``
  - ``$ git status``
    - Commit any changes to master
  - ``$ git co gh-pages``
  - ``$ rm -rf *``
    - ya rly
  - ``$ mv ~/Desktop/html/*``
  - ``$ mv ~/Desktop/lacuna.cfg ./etc/``
  - ``$ git add -A .``
  - ``$ git commit -m docs``
  - ``$ git push origin gh-pages``
    - It'll take anywhere from a few seconds to up to 10 minutes for github 
      pages to refresh
  - ``$ git co master``














































k
