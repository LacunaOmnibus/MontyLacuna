
.. _stations_report:

Stations Report
===============

Produces several different types of reports on one or all space stations in 
your alliance.

You specify the report type you want and the station name.  If you want to run 
the report against all stations in your empire, specify ``all`` as the station 
name.

The ``All Resources`` and ``Low Resources`` reports' output both look the 
same::

    >>> python bin/stations_report --report allres "ISS"
    ISS (1, 1) - Zone 0|0
            Food / hour:           10,123,456
            Ore / hour:            10,123,456
            Water / hour:          10,123,456
            Energy / hour:         10,123,456
    ---------------
    Reported on 1 total station.

The ``Influence`` report::

    >>> python bin/stations_report.py --report inf "ISS"
    ISS (1, 1) - Zone 0|0
            Spent/Available -- 100/100
    Reported on 1 total station.

The ``Building`` report::

    >>> python bin/stations_report.py --report bldg "ISS"
    ISS (1, 1) - Zone 0|0
        NAME                                  COORDS    LEVEL   EFFICIENCY
        Art Museum                            (-2,3)       10          100
        Culinary Institute                     (4,4)       10          100
        Interstellar Broadcast System         (-3,4)       10          100
        Opera House                           (-4,4)       10          100
        Parliament                             (3,4)       10          100
        Police Station                         (2,3)       10          100
        Station Command Center                 (0,0)       10          100
        Warehouse                             (0,-5)       10          100
        Warehouse                            (-3,-4)       10          100
        Warehouse                             (2,-5)       10          100
    ---------------

The ``Supply Chains`` report::

    >>> python bin/stations_report.py --report chain "ISS"
    ISS (1, 1) - Zone 0|0
        SOURCE                     RES TYPE          RES/HOUR    EFFICIENCY
        Earth                      bauxite            100,000          1100
        Earth                      energy             100,000          1100
        Earth                      fungus             100,000          1100
        Earth                      water              100,000          1100
        Mars                       energy             300,000            98
        Mars                       halite             300,000            98
        Mars                       root               300,000            98
        Mars                       water              300,000            98
    ---------------
    [2015-02-17 15:30:35] (USER) (INFO) - Reported on 1 total station.

    Note that this station might have problems, since four of its chains are 
    operating at under 100% efficiency.

All vs Low resource reports
---------------------------
The difference between these two reports is that the ``all`` version will 
always show you the station's resource income, but the ``low`` version will 
only show resource income if any of the resources are at or below 0.

So the low report is most useful when run against all stations in your empire, 
to make sure no stations are currently resource starved.

The ``allres`` report is the default, so if you just want to do a quick check 
on a given station's resource situation, this will work::

    >>> python bin/stations_report.py ISS

Long reports on all stations
----------------------------
The output of some of the reports is a bit long, and if you're running one of 
those reports against all of your stations, the output will probably end up 
scrolling way off your screen.  If that's the case, just run the report and 
redirect the output to a file.  You'll still see logging statements on the 
screen so you'll know what's going on, but you'll probably want to turn on 
more vocal logging output.  

eg::

    >>> python bin/stations_report.py -v all > stations.txt

Now you can just open up ``stations.txt`` in Notepad or whatever editor you 
like.

Force fresh data
----------------

Station data gets cached so retrieving it on the next run will be quicker.  
This way you can conveniently run a report multiple times, or even run 
different reports, without having to wait or waste your RPCs.  

However, if you run a report once, then update something (eg you update a 
supply chain to send more resources) and want to run the same report again to 
see your new resource situation, you won't want to look at data cached from 
the previous run.  In that case, pass the ``--fresh`` option::

    >>> python bin/stations_report.py --fresh ISS

Full documentation
------------------

For complete help, see the script's help documentation::

    >>> python bin/stations_report.py -h

.. autoclass:: lacuna.binutils.libstations_report.StationsReport
   :members:
   :show-inheritance:

