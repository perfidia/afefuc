# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'SelectForm.ui'
#
# Created: Thu May  9 16:07:11 2013
#      by: PyQt4 UI code generator 4.9.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_SelectForm(object):
    def setupUi(self, SelectForm):
        SelectForm.setObjectName(_fromUtf8("SelectForm"))
        SelectForm.resize(390, 315)
        self.verticalLayout = QtGui.QVBoxLayout(SelectForm)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.itemsView = QtGui.QTableView(SelectForm)
        self.itemsView.setObjectName(_fromUtf8("itemsView"))
        self.verticalLayout.addWidget(self.itemsView)
        self.boxButton = QtGui.QDialogButtonBox(SelectForm)
        self.boxButton.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.boxButton.setObjectName(_fromUtf8("boxButton"))
        self.verticalLayout.addWidget(self.boxButton)

        self.retranslateUi(SelectForm)
        QtCore.QMetaObject.connectSlotsByName(SelectForm)

    def retranslateUi(self, SelectForm):
        SelectForm.setWindowTitle(QtGui.QApplication.translate("SelectForm", "Form", None, QtGui.QApplication.UnicodeUTF8))

