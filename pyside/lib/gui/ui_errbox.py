# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/errbox.ui'
#
# Created: Thu May 14 19:27:09 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_ErrBox(object):
    def setupUi(self, ErrBox):
        ErrBox.setObjectName("ErrBox")
        ErrBox.resize(271, 192)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(ErrBox.sizePolicy().hasHeightForWidth())
        ErrBox.setSizePolicy(sizePolicy)
        ErrBox.setModal(False)
        self.verticalLayout_2 = QtGui.QVBoxLayout(ErrBox)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtGui.QLabel(ErrBox)
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
        self.buttonBox = QtGui.QDialogButtonBox(ErrBox)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout_2.addWidget(self.buttonBox)

        self.retranslateUi(ErrBox)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), ErrBox.reject)
        QtCore.QMetaObject.connectSlotsByName(ErrBox)

    def retranslateUi(self, ErrBox):
        ErrBox.setWindowTitle(QtGui.QApplication.translate("ErrBox", "Error", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("ErrBox", "Blargle Flurble", None, QtGui.QApplication.UnicodeUTF8))

