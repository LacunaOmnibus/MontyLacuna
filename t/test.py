
import os
import sys
import pprint
pp = pprint.PrettyPrinter( indent = 4 )
import re
import threading
import timeit

bindir = os.path.abspath(os.path.dirname(__file__))
libdir = bindir + "/../lib"
sys.path.append(libdir)

import lacuna as lac

glc = lac.clients.Member(
    config_file = bindir + "/../etc/lacuna.cfg",
    config_section = 'my_real',
)

my_planet = glc.get_body_byname( 'bmots rof 2.1' )

