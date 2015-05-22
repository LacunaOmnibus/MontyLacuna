# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/picklist.ui'
#
# Created: Fri May 22 15:06:18 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_PickList(object):
    def setupUi(self, PickList):
        PickList.setObjectName("PickList")
        PickList.resize(276, 353)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(PickList.sizePolicy().hasHeightForWidth())
        PickList.setSizePolicy(sizePolicy)
        PickList.setModal(True)
        self.verticalLayout_2 = QtGui.QVBoxLayout(PickList)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.listWidget = QtGui.QListWidget(PickList)
        self.listWidget.setObjectName("listWidget")
        self.verticalLayout.addWidget(self.listWidget)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.buttonBox = QtGui.QDialogButtonBox(PickList)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout_2.addWidget(self.buttonBox)

        self.retranslateUi(PickList)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), PickList.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), PickList.reject)
        QtCore.QObject.connect(self.listWidget, QtCore.SIGNAL("itemDoubleClicked(QListWidgetItem*)"), PickList.accept)
        QtCore.QMetaObject.connectSlotsByName(PickList)

    def retranslateUi(self, PickList):
        PickList.setWindowTitle(QtGui.QApplication.translate("PickList", "Pick One", None, QtGui.QApplication.UnicodeUTF8))

