# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/about.ui'
#
# Created: Mon May 18 18:36:20 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_About(object):
    def setupUi(self, About):
        About.setObjectName("About")
        About.resize(400, 300)
        self.verticalLayout_2 = QtGui.QVBoxLayout(About)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.lbl_appname = QtGui.QLabel(About)
        self.lbl_appname.setObjectName("lbl_appname")
        self.verticalLayout.addWidget(self.lbl_appname)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.lbl_pyside_ver = QtGui.QLabel(About)
        self.lbl_pyside_ver.setObjectName("lbl_pyside_ver")
        self.verticalLayout.addWidget(self.lbl_pyside_ver)
        self.lbl_qt_ver = QtGui.QLabel(About)
        self.lbl_qt_ver.setObjectName("lbl_qt_ver")
        self.verticalLayout.addWidget(self.lbl_qt_ver)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.lbl_copyright = QtGui.QLabel(About)
        self.lbl_copyright.setObjectName("lbl_copyright")
        self.verticalLayout.addWidget(self.lbl_copyright)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.buttonBox = QtGui.QDialogButtonBox(About)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout_2.addWidget(self.buttonBox)

        self.retranslateUi(About)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), About.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), About.reject)
        QtCore.QMetaObject.connectSlotsByName(About)

    def retranslateUi(self, About):
        About.setWindowTitle(QtGui.QApplication.translate("About", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.lbl_appname.setText(QtGui.QApplication.translate("About", "App Name and Version", None, QtGui.QApplication.UnicodeUTF8))
        self.lbl_pyside_ver.setText(QtGui.QApplication.translate("About", "PySide Version", None, QtGui.QApplication.UnicodeUTF8))
        self.lbl_qt_ver.setText(QtGui.QApplication.translate("About", "QtCore Version", None, QtGui.QApplication.UnicodeUTF8))
        self.lbl_copyright.setText(QtGui.QApplication.translate("About", "Copyright", None, QtGui.QApplication.UnicodeUTF8))

