
### Leave this around for eg until I've got the launcher datetime code figured 
### out.


import time
from datetime import datetime
import pytz

if time.localtime().tm_isdst > 0:
    print( "We're currently in DST." )
else:
    print( "We're currently NOT in DST." )


local_tz_tuple  = time.tzname   # ["EST", "EDT"]
local_tz_name   = local_tz_tuple[ time.localtime().tm_isdst ]
local_tz_2      = pytz.timezone( local_tz_name )
server_tz       = pytz.timezone("UTC")

### We can also hardcode this format of local TZ name, but we can't get this 
### format from time.tzname.
### There apparently is a Python library that includes an Olson database, and 
### I could probably dig "America/New_York" out of that, but that library is 
### not core.
local_tz_1      = pytz.timezone("America/New_York")

now             = datetime.now()
local_now_1     = datetime.now( local_tz_1 )
local_now_2     = datetime.now( local_tz_2 )
utc_now         = datetime.now( server_tz )

print( now )
print( local_now_1 )
print( local_now_2 )
print( utc_now )

