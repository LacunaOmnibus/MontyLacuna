#!/usr/bin/python3

import datetime, os, sys, time
bindir = os.path.abspath(os.path.dirname(sys.argv[0]))
libdir = bindir + "/../lib"
sys.path.append(libdir)

import lacuna, logging
import lacuna.exceptions as err
import lacuna.binutils.libss_lab as lib
import lacuna.exceptions as err

ssl     = lib.SSLab()
l       = ssl.client.user_logger


plans_built = 0
while(True):

    l.info( "Building a {} plan.".format(ssl.args.plan) )
    timeleft    = ssl.build_plan()
    plans_built += 1

    if( ssl.args.sub ):
        l.info( "Subsidizing your plan for 2 E." )
        ssl.subsidize_plan()
        timeleft = 0

    if( plans_built >= ssl.args.num ):
        break
        
    if( timeleft ):
        plans_left  = ssl.args.num - plans_built
        sleep_secs  = timeleft + 5
        now         = datetime.datetime.now()
        wake_time   = now + datetime.timedelta( 0, sleep_secs )
        
        l.info( "{} more plans to build.  I'll continue building at {}."
            .format(plans_left, wake_time.strftime("%Y-%m-%d %H:%M:%S"))
        )
        time.sleep( sleep_secs )

l.info( "I built {} {} plans on {}."
    .format(plans_built, ssl.args.plan, ssl.planet.name)
)




#l.info( "{} does not have any shipyards of the right level.  Skipping.".format(bs.planet.name) )

