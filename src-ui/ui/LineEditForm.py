# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'LineEditForm.ui'
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

class Ui_LineEditForm(object):
    def setupUi(self, LineEditForm):
        LineEditForm.setObjectName(_fromUtf8("LineEditForm"))
        LineEditForm.resize(546, 82)
        self.verticalLayout = QtGui.QVBoxLayout(LineEditForm)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.nameLabel = QtGui.QLabel(LineEditForm)
        self.nameLabel.setObjectName(_fromUtf8("nameLabel"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.nameLabel)
        self.nameEdit = QtGui.QLineEdit(LineEditForm)
        self.nameEdit.setObjectName(_fromUtf8("nameEdit"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.nameEdit)
        self.verticalLayout.addLayout(self.formLayout)
        self.boxButton = QtGui.QDialogButtonBox(LineEditForm)
        self.boxButton.setOrientation(QtCore.Qt.Horizontal)
        self.boxButton.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.boxButton.setObjectName(_fromUtf8("boxButton"))
        self.verticalLayout.addWidget(self.boxButton)

        self.retranslateUi(LineEditForm)
        QtCore.QMetaObject.connectSlotsByName(LineEditForm)

    def retranslateUi(self, LineEditForm):
        LineEditForm.setWindowTitle(QtGui.QApplication.translate("LineEditForm", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.nameLabel.setText(QtGui.QApplication.translate("LineEditForm", "Name", None, QtGui.QApplication.UnicodeUTF8))

