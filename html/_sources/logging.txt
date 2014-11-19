
.. _logging:

Logging
=======

Logging is performed using Python's core `logging library 
<https://docs.python.org/3.4/library/logging.html>`_.

Both Request and User log entries will be written to the same logfile, 
specified in your config file.

Log Levels
----------
This is documented at the URL above, but it's being repeated here for 
convenience.

    ==========  ===============
    Level       Numeric value
    ==========  ===============
    CRITICAL    50
    ERROR       40
    WARNING     30
    INFO        20
    DEBUG       10
    ==========  ===============
  

Request Log Entries
-------------------
All requests to the TLE server will be written to the logfile specified in the 
config file.  This happens automatically, so you don't have to do anything.  
Just run your scripts as needed, and you'll be able to check that logfile to 
see what's happening.

Most request log entries will only display to the file.  However, in the case 
of something going wrong, entries of WARNING level or higher will also be 
shown on-screen.

An example request log entry::

    [2014-11-18 15:49:39] (REQ) (INFO) - tmtowtdi - stats::alliance_rank - Success

- **[2014-11-18 15:49:39]** -- The date and time this entry was generated.
- **(REQ)** -- This is a request log entry, rather than a user entry.
- **(INFO)** -- The log level.  This is is an INFO-level entry.
- **tmtowtdi** -- The name of the empire that generated this entry.  Handy if 
  you're running scripts for multiple different empires and logging them all 
  to the same file.
- **stats::alliance_rank** -- The TLE server module and method that were 
  called.
- **Success** -- The actual log message.  For most request log entries, the 
  entire message will simply be "Success".   

User Log Entries
----------------
Along with the automatic request log, your script can access the user logger 
so you can create whatever log entries you like::

    glc = lac.clients.Member( standard connection arguments )
    l = glc.user_logger
    l.error( "This is an error message." )
    l.info( "This is an info message." )

You can use all of the log levels in the table above.  Again, only WARNING 
level or higher will display to the screen; any lower-level entries will just 
go into the log file.

An example user log entry::

    [2014-11-18 15:49:39] (USER) (INFO) - This is an info message.

- **[2014-11-18 15:49:39]** -- The date and time this entry was generated.
- **(USER)** -- This is a user log entry, rather than a request entry.
- **(INFO)** -- The log level.  This is is an INFO-level entry.
- **This is an info message.** -- The actual log message.

