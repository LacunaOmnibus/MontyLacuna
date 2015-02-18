
.. _logging:

logging
=======

Logging is performed using Python's core `logging library 
<https://docs.python.org/3.4/library/logging.html>`_.

Three separate logfiles will be written to by most scripts:
    - Request log
    - User log
    - Module log

All log files live in ``ROOT/var/``.  

Log Levels
----------

    ==========  ===============
    Level       Numeric value
    ==========  ===============
    CRITICAL    50
    ERROR       40
    WARNING     30
    INFO        20
    DEBUG       10
    ==========  ===============

Request Log
-----------
The file name will be either what's specified in the config file as the 
``logfile`` option or simply ``request.log`` if no such option exists in your 
config.  This happens automatically; just run your scripts, and you'll be able 
to check that logfile to see what's happening.

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

User Log
--------
Along with the automatic request log, your script can access the user logger 
so you can create whatever log entries you like::

    my_client = lacuna.clients.Member( standard connection arguments )
    l = my_client.user_logger
    l.error( "This is an error message." )
    l.info( "This is an info message." )
    l.debug( "This is a debug message.  You may want a lot of these while you're working." )

User log entries will go into a file named according to the name of the 
current empire, removing all non-letter characters.  eg for the empire "My 
Great Empire", user log entries will go into ``MyGreatEmpire.log``.  If your 
script's client isn't logged in, the user log entries will go into 
``guest.log``.

As with the request log, only WARNING level or higher will display to the 
screen by default, while any lower-level entries will just go into the log 
file.  If you want to change that, for example to display DEBUG level messages 
while you're working on your script, add the following::

    client.user_log_stream_handler.setLevel(logging.DEBUG)

Once you're finished working, maybe you don't want all your DEBUG messages to 
show up for the user, but you do want INFO level messages to continue going to 
the screen to let the user know what's going on, in which case you'd just 
change that previous line to::

    client.user_log_stream_handler.setLevel(logging.INFO)

An example user log entry::

    [2014-11-18 15:49:39] (USER) (INFO) - This is an info message.

- **[2014-11-18 15:49:39]** -- The date and time this entry was generated.
- **(USER)** -- This is a user log entry, rather than a request entry.
- **(INFO)** -- The log level.  This is is an INFO-level entry.
- **This is an info message.** -- The actual log message.

Module Log
----------
The module log is rarely used, and exists for the purpose of debugging 
specific MontyLacuna modules.  The entries are written to ``module.log``, but 
this file will likely be empty most of the time.



