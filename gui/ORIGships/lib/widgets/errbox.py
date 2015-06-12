
from PySide.QtGui import QApplication, QDialog
from gui import Ui_ErrBox

class ErrBox(QDialog, Ui_ErrBox):
    def __init__(self, parent=None):
        super(ErrBox, self).__init__(parent)
        self.setupUi(self)

    def accept(self):
        super().accept()

    def set_message(self, msg:str = "Error!"):
        self.label.setText( QApplication.translate("ErrBox", msg, None, QApplication.UnicodeUTF8) )
        self.show()
