#!/usr/bin/python3

import os, sys
bindir = os.path.abspath(os.path.dirname(sys.argv[0]))
libdir = bindir + "/../lib"
sys.path.append(libdir)

import logging
import lacuna
import lacuna.exceptions as err
import lacuna.binutils.libmail_compile as lib
import lacuna.exceptions as err

mc  = lib.MailCompile()
l   = mc.client.user_logger


"""
The report, especially the output of any tables, could stand to be prettified up a bit.

But this works:
    $ py bin/mail_compile.py --tag Attack attack > jontest.txt



Also, there's zero documentation for this.


"""




l.info( "Looking for matching messages..." )
date_summaries = mc.get_dated_summaries()
l.debug( "found {} messages within our date range.".format(len(date_summaries)) )
summaries      = mc.get_matching_summaries( date_summaries )
l.debug( "found {} messages within our date range that match our subject." .format(len(summaries)) )

if len(summaries):
    l.info( "Found {} matching messages; compiling report...".format(len(summaries)) )
    report = mc.compile_full_messages( summaries )
    print( report )
else:
    l.info( "Found no matching messages." )


