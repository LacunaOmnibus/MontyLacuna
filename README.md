MontyLacuna
===========

Python Client for The Lacuna Expanse

This is essentially a port of the Perl Games::Lacuna::Client module to Python.  
No attempt is being made to preseve the same API used by GLC, but the goal is 
to replicate all of the functionality.

The main goal is to help me learn Python, but I'd like to end up with a fully 
working package.

## Complete
Nothing.

## Working
"working" means that all functionality exists, and quickie scripts appear to 
work, but it hasn't been fully tested yet.

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
 - archaeology
 - blackholegenerator
 - development
 - distributioncenter
 - embassy
   - What I could test works, but testing of several methods would require making a test 
     account and inviting/rejecting/etc that account.  Currently I'm unable to create a 
     test account on PT.  I have no reason to believe that these untested methods don't 
     work, they just haven't actually been confirmed to work.

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




