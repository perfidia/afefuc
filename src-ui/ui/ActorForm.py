# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ActorForm.ui'
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

class Ui_ActorForm(object):
    def setupUi(self, ActorForm):
        ActorForm.setObjectName(_fromUtf8("ActorForm"))
        ActorForm.resize(546, 307)
        self.verticalLayout = QtGui.QVBoxLayout(ActorForm)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.nameLabel = QtGui.QLabel(ActorForm)
        self.nameLabel.setObjectName(_fromUtf8("nameLabel"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.nameLabel)
        self.idLabel = QtGui.QLabel(ActorForm)
        self.idLabel.setObjectName(_fromUtf8("idLabel"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.idLabel)
        self.descriptionLabel = QtGui.QLabel(ActorForm)
        self.descriptionLabel.setObjectName(_fromUtf8("descriptionLabel"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.descriptionLabel)
        self.nameEdit = QtGui.QLineEdit(ActorForm)
        self.nameEdit.setObjectName(_fromUtf8("nameEdit"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.nameEdit)
        self.idEdit = QtGui.QLineEdit(ActorForm)
        self.idEdit.setObjectName(_fromUtf8("idEdit"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.idEdit)
        self.descriptionEdit = QtGui.QPlainTextEdit(ActorForm)
        self.descriptionEdit.setPlainText(_fromUtf8(""))
        self.descriptionEdit.setObjectName(_fromUtf8("descriptionEdit"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.descriptionEdit)
        self.typeLabel = QtGui.QLabel(ActorForm)
        self.typeLabel.setObjectName(_fromUtf8("typeLabel"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.typeLabel)
        self.typeComboBox = QtGui.QComboBox(ActorForm)
        self.typeComboBox.setObjectName(_fromUtf8("typeComboBox"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.typeComboBox)
        self.verticalLayout.addLayout(self.formLayout)
        self.boxButton = QtGui.QDialogButtonBox(ActorForm)
        self.boxButton.setOrientation(QtCore.Qt.Horizontal)
        self.boxButton.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.boxButton.setObjectName(_fromUtf8("boxButton"))
        self.verticalLayout.addWidget(self.boxButton)

        self.retranslateUi(ActorForm)
        QtCore.QMetaObject.connectSlotsByName(ActorForm)

    def retranslateUi(self, ActorForm):
        ActorForm.setWindowTitle(QtGui.QApplication.translate("ActorForm", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.nameLabel.setText(QtGui.QApplication.translate("ActorForm", "Name", None, QtGui.QApplication.UnicodeUTF8))
        self.idLabel.setText(QtGui.QApplication.translate("ActorForm", "ID", None, QtGui.QApplication.UnicodeUTF8))
        self.descriptionLabel.setText(QtGui.QApplication.translate("ActorForm", "Description", None, QtGui.QApplication.UnicodeUTF8))
        self.typeLabel.setText(QtGui.QApplication.translate("ActorForm", "Type", None, QtGui.QApplication.UnicodeUTF8))

