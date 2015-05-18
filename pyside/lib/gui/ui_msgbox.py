# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/msgbox.ui'
#
# Created: Mon May 18 18:36:20 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_MsgBox(object):
    def setupUi(self, MsgBox):
        MsgBox.setObjectName("MsgBox")
        MsgBox.resize(271, 192)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MsgBox.sizePolicy().hasHeightForWidth())
        MsgBox.setSizePolicy(sizePolicy)
        MsgBox.setModal(False)
        self.verticalLayout_2 = QtGui.QVBoxLayout(MsgBox)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtGui.QLabel(MsgBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setCursor(QtCore.Qt.ArrowCursor)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.buttonBox = QtGui.QDialogButtonBox(MsgBox)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout_2.addWidget(self.buttonBox)

        self.retranslateUi(MsgBox)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), MsgBox.accept)
        QtCore.QMetaObject.connectSlotsByName(MsgBox)

    def retranslateUi(self, MsgBox):
        MsgBox.setWindowTitle(QtGui.QApplication.translate("MsgBox", "Message", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("MsgBox", "Blargle Flurble", None, QtGui.QApplication.UnicodeUTF8))

