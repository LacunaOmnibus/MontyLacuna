
from PySide.QtGui import QApplication, QDialog
from gui import Ui_ConfBox

class ConfBox(QDialog, Ui_ConfBox):
    """ Displays the requested message with Yes and No buttons in an app-modal window. 

    Returns either QDialog.Accepted (1) or QDialog.Rejected (0).
    """
    def __init__(self, parent=None):
        super(ConfBox, self).__init__(parent)
        self.setupUi(self)

    def accept(self):
        super().accept()

    def reject(self):
        super().reject()

    def set_message(self, msg:str = "Are you sure?"):
        self.label.setText( QApplication.translate("ConfBox", msg, None, QApplication.UnicodeUTF8) )
        return self.exec()

