
import os, sys
from PySide.QtGui import QApplication
import widgets

class MyApp(QApplication):

    def __init__(self, argv, instdir):
        super().__init__(argv)
        self.instdir = instdir
        self.config_file = instdir + "/etc/lacuna.cfg"

    def run(self):
        frame = widgets.MainWindow(config_file = self.config_file)
        frame.show()
        sys.exit( self.exec_() )

