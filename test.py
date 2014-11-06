
import re

str = 'p16-1'

mymatch = re.match("^(p\d+)", str)
if mymatch:
    print( mymatch.group(1) )


