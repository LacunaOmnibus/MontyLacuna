
from PySide.QtGui import QMainWindow, QComboBox

class BodiesComboBox():
    """ Manages a combo box containing body names

    Arguments:
        combo (QTableWidget): The actual table widget.
        parent (QWidget): The widget that owns the table widget.
    """

    def __init__(self, combo:QComboBox, parent:QMainWindow):
        self.widget = combo
        self.parent = parent

    def add_colonies(self):
        """ Add colony names owned by the current client's empire to the combo box
        """
        for pname in sorted( self.parent.app.client.empire.colony_names.keys() ):
            self.widget.addItem( pname )
        self.widget.repaint()

    def currentText(self):
        """ Get the current text (body name) from the combo box
        """
        return self.widget.currentText()

    def clear(self):
        """ Clear the combo box
        """
        self.widget.clear()

    def setEnabled(self, flag:bool):
        self.widget.setEnabled(flag)

