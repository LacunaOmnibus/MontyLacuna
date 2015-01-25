#!/usr/bin/python3

def ReportSingleBuilding(myStation, buildingName):
        buildings=myStation.get_buildings_bytype(buildingName)
        if buildings is None:
                return ","
        building = buildings[0]
        return "{}:{},".format( building.name, str(building.level) )
        
def ReportMultiBuilding(myStation, buildingName, max):
        buildingList = []
        buildings=myStation.get_buildings_bytype(buildingName)
        if buildings is None:
                return ""
        
        buildingCount = len(buildings)
        if buildingCount > max:
                buildingCount = max
                
        for i in range(0,buildingCount):
                buildingList.append(buildings[i])
        
        line = ""       
        for building in sorted(buildingList, key=lambda MyBuilding: MyBuilding.level, reverse=True):
            line += "{}:{},".format( building.name, str(building.level) )
        
        return line

def ReportStation(myStation):
        line = "{},x:{},y:{},zone:{},".format( myStation.name, myStation.x, 
        myStation.y, myStation.zone)

        line += ReportSingleBuilding(myStation, "Station Command Center")
        line += ReportSingleBuilding(myStation, "Parliament")
        line += ReportSingleBuilding(myStation, "Art Museum")
        line += ReportSingleBuilding(myStation, "Culinary Institute")
        line += ReportSingleBuilding(myStation, "Interstellar Broadcast System")
        line += ReportSingleBuilding(myStation, "Opera House")
        line += ReportSingleBuilding(myStation, "Police Station")
        line += ReportMultiBuilding(myStation, "Warehouse", 6)
        return line

def tmt_csv_sample():
    """
    Jof - this is just a quickie example of how to use the csv module.

    Below, I'm creating a list (the "row" variable), and then I'll pass that 
    to the csv module and let it create the actual row for me.

    Note that my "row" variable contains a data field that has a comma already 
    in the data itself (the fourth field is supposed to look like TLE 
    coordinates).  The csv module recognizes that there's a comma in that 
    field already, and so it wraps that field in quotes on output.

    So this example ends up producing this line:
	one,two,three,"(12,45)",another field, still more data

    This way, instead of constructing the "line" variable manually like you've 
    been doing, you could instead just construct a list, and then pass that 
    list to the csv module and have it generate the actual output row for you.

    I did _not_ change your code to use this method, just listing this here as 
    an option if you want to try it.
    """
    import csv

    row = [ 'one', 'two', 'three', "(12,45)" ]
    row.append( "another field" )
    row.append( "still more data" )

    writer = csv.writer( sys.stdout ) 
    writer.writerow( row )




import os, sys
bindir = os.path.abspath(os.path.dirname(sys.argv[0]))
libdir = bindir + "/../lib"
sys.path.append(libdir)

### Uncomment the next two lines if you want to see my csv example function 
### run.
#tmt_csv_sample()
#quit()

import logging
import lacuna, lacuna.exceptions
import lacuna.binutils.libtest_script as lib

my_client = lacuna.clients.Member(
    config_file = os.path.abspath(os.path.dirname(sys.argv[0])) + "/../etc/lacuna.cfg",
    config_section = 'real'
)


### Doing this turns on request caching.  So any time you make a request to 
### the TLE server, and then make another identical request within an hour, 
### that second request just draws its results from the cache instead of 
### re-sending a request to the server.
###
### "jof_stations" is just an arbitrary name for this cache.
###
### So if you run this multiple times, it'll be much faster on the > 1st run.
###
my_client.cache_on( "jof_stations", 3600 )



### alliance.space_stations doesn't actually contain full body objects.  So 
### the station objects you were getting back with this code were unable to 
### call methods like "get_buildings_bytype()".
### 
### I'm aware that this is @#%$ confusing, and I wish that the space station 
### in alliance.space_stations were real, actual body objects that you could 
### call methods on.  But the data that comes back from the server in 
### alliance.space_stations just isn't enough data to construct full Body 
### objects.
###
#alliance = my_client.get_my_alliance()
#stations = sorted(alliance.space_stations, key=lambda Body: Body.name)



### So instead, I'll just grab a list of only station names here, and we'll 
### individually turn those station names into full Body objects in the loop 
### below.
###
station_names = sorted( my_client.empire.station_names.keys() )



### the "cnt" below is just me limiting this to only report on the first 2 
### stations it encounters for testing purposes.
###
cnt = 0
for name in station_names:
        cnt += 1
        station = my_client.get_body_byname( name )
        report = ReportStation(station)
        print(report)
        if cnt >= 2:
                break



