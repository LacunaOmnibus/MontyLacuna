
import os
import sys
import pprint
import re
import threading
import timeit

bindir = os.path.abspath(os.path.dirname(__file__))
libdir = bindir + "/../lib"
sys.path.append(libdir)

import lacuna as lac
pp = pprint.PrettyPrinter( indent = 4 )

glc = lac.users.Member(
    config_file = bindir + "/../etc/lacuna.cfg",
    config_section = 'my_sitter',
)
print( glc.empire.rpc_count )

#print( timeit.timeit(my_single, number=1) )
#print( timeit.timeit(my_thread, number=1) )

