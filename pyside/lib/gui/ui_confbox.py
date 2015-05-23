# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/confbox.ui'
#
# Created: Fri May 22 17:04:27 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_ConfBox(object):
    def setupUi(self, ConfBox):
        ConfBox.setObjectName("ConfBox")
        ConfBox.resize(271, 192)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(ConfBox.sizePolicy().hasHeightForWidth())
        ConfBox.setSizePolicy(sizePolicy)
        ConfBox.setModal(True)
        self.verticalLayout_2 = QtGui.QVBoxLayout(ConfBox)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtGui.QLabel(ConfBox)
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
        self.buttonBox = QtGui.QDialogButtonBox(ConfBox)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.No|QtGui.QDialogButtonBox.Yes)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout_2.addWidget(self.buttonBox)

        self.retranslateUi(ConfBox)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), ConfBox.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), ConfBox.reject)
        QtCore.QMetaObject.connectSlotsByName(ConfBox)

    def retranslateUi(self, ConfBox):
        ConfBox.setWindowTitle(QtGui.QApplication.translate("ConfBox", "Query", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("ConfBox", "Blargle Flurble Foo", None, QtGui.QApplication.UnicodeUTF8))

