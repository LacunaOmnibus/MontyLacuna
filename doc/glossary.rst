
.. _glossary:

Glossary
========

**Standard Search String**
    Several methods allow you to search for an item by name (a star, an 
    empire, etc).  Some of these methods allow a "search string" instead of a 
    full name.  A search string must be at least three characters long.  All 
    objects whose names match that string will be returned.

    So, for the search string: "Ear", you'd get back the list:
        ``[ "Earth", "Ears is a strange name for a planet", "Earp, Wyatt" ]``

    Often with these methods, you're really interested in getting back info on 
    just one item (planet, empire, whatever), and so the search string you're 
    passing in will be complete ("Earth").  Don't fall into the mindset that 
    "I'm searching for one thing so I should be getting back one thing".  
    You're still going to be getting back a list.  It'll be a list of a single 
    item, but it'll still be a list.

**TLE date format**
    Many methods include dates as part of their returns.  TLE dates are in the 
    format "01 31 2010 13:09:05 +0000".

    The "+0000" is meant to indicate a Time Zone, but all date returns from 
    the server will be in UTC, so they'll always be "+0000".

    Almost all MontyLacuna objects have a ``tle2date`` method, so you can 
    translate those TLE date strings to a Python datetime.datetime object:

        ::

            dt = my_client.tle2date( my_client.SOME_DATE_ATTRIBUTE )
            print( "Something happened on day {} of month {}, in the year {}, at {}:{}:{}."
                .format(dt.day, dt.month, dt.year, dt.hour, dt.minute, dt.second)
            )
            



