#!/usr/bin/env python3

import os, sys

### Assumes we're in MONTY/pyside/bin/
instdir = os.path.abspath(os.path.dirname(sys.argv[0])) + "/../.."

libmonty    = instdir + "/lib"
libguiapp   = instdir + "/pyside/lib"
sys.path.append(libmonty)
sys.path.append(libguiapp)
sys.path.append("lib")
from myapp import MyApp

app = MyApp(sys.argv)
app.run()

