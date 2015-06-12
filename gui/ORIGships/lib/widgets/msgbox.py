
from PySide.QtGui import QApplication, QDialog
from gui import Ui_MsgBox

class MsgBox(QDialog, Ui_MsgBox):
    def __init__(self, parent=None):
        super(MsgBox, self).__init__(parent)
        self.setupUi(self)

    def accept(self):
        """ Here we're just calling super's accept(), so as it is we could just 
        delete this entire accept() method and let super handle the call in the
        first place.
        But by leaving this method here, we could do also $stuff when the user 
        clicks the accept button.
        """
        super().accept()

    def set_message(self, msg:str = "Message."):
        self.label.setText( QApplication.translate("MsgBox", msg, None, QApplication.UnicodeUTF8) )
        self.show()
