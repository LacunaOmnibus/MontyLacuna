
from PySide.QtGui import QDialog
from gui import Ui_PickList

class PickList(QDialog, Ui_PickList):
    def __init__(self, parent=None):
        self.items = ()
        super(PickList, self).__init__(parent)
        self.setupUi(self)

    def add(self, items:list):
        self.listWidget.addItems( items )

    def pickone(self):
        if self.exec() == QDialog.Accepted:
            return self.listWidget.currentItem().text()
        return None

