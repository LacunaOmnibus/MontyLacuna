#!/usr/bin/env python3

import os, sys
bindir      = os.path.abspath(os.path.dirname(sys.argv[0]))
libmonty    = bindir + "/../../lib"
libpyside   = bindir + "/../lib"
sys.path.append(libmonty)
sys.path.append(libpyside)

from PySide.QtGui import QApplication
import widgets

### assumes we're in MONTY/pyside/bin/
config_file = os.path.dirname(os.path.realpath(__file__)) + "/../../etc/lacuna.cfg"

if __name__ == '__main__':
    app = QApplication(sys.argv)
    frame = widgets.MainWindow(config_file = config_file)
    frame.show()
    sys.exit( app.exec_() )

