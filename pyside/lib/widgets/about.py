
import PySide
import PySide.QtCore
from PySide.QtGui import QApplication, QDialog
from gui import Ui_About

class About(QDialog, Ui_About):
    """ Displays the About window.
    """
    def __init__(self, parent=None):
        super(About, self).__init__(parent)
        self.setupUi(self)
        self.lbl_appname.setText("My App Name")
        self.lbl_pyside_ver.setText( "PySide Version {}".format(PySide.__version__) )
        self.lbl_qt_ver.setText( "QtCore Version {}".format(PySide.QtCore.__version__) )
        self.lbl_copyright.setText( "Copyright 2015 Jonathan D. Barton" )
        self.show()

