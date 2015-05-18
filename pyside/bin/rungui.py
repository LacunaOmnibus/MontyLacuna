#!/usr/bin/env python3


### Assumes we're in MONTY/pyside/bin/
instdir = os.path.abspath(os.path.dirname(sys.argv[0])) + "/../.."

import os, sys
libmonty    = instdir + "/lib"
libguiapp   = instdir + "/pyside/lib"
sys.path.append(libmonty)
sys.path.append(libguiapp)
from myapp import MyApp

app = MyApp(sys.argv, instdir)
app.run()

