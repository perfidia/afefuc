# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'BusinessObjectForm.ui'
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

class Ui_BusinessObjectForm(object):
    def setupUi(self, BusinessObjectForm):
        BusinessObjectForm.setObjectName(_fromUtf8("BusinessObjectForm"))
        BusinessObjectForm.resize(855, 513)
        self.verticalLayout = QtGui.QVBoxLayout(BusinessObjectForm)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.nameLabel = QtGui.QLabel(BusinessObjectForm)
        self.nameLabel.setObjectName(_fromUtf8("nameLabel"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.nameLabel)
        self.nameEdit = QtGui.QLineEdit(BusinessObjectForm)
        self.nameEdit.setObjectName(_fromUtf8("nameEdit"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.nameEdit)
        self.idLabel = QtGui.QLabel(BusinessObjectForm)
        self.idLabel.setObjectName(_fromUtf8("idLabel"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.idLabel)
        self.idEdit = QtGui.QLineEdit(BusinessObjectForm)
        self.idEdit.setObjectName(_fromUtf8("idEdit"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.idEdit)
        self.attributesLabel = QtGui.QLabel(BusinessObjectForm)
        self.attributesLabel.setObjectName(_fromUtf8("attributesLabel"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.attributesLabel)
        self.descriptionLabel = QtGui.QLabel(BusinessObjectForm)
        self.descriptionLabel.setObjectName(_fromUtf8("descriptionLabel"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.descriptionLabel)
        self.descriptionEdit = QtGui.QPlainTextEdit(BusinessObjectForm)
        self.descriptionEdit.setObjectName(_fromUtf8("descriptionEdit"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.descriptionEdit)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.attributesView = QtGui.QTableView(BusinessObjectForm)
        self.attributesView.setObjectName(_fromUtf8("attributesView"))
        self.horizontalLayout.addWidget(self.attributesView)
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.addButton = QtGui.QPushButton(BusinessObjectForm)
        self.addButton.setObjectName(_fromUtf8("addButton"))
        self.verticalLayout_2.addWidget(self.addButton)
        self.deleteButton = QtGui.QPushButton(BusinessObjectForm)
        self.deleteButton.setObjectName(_fromUtf8("deleteButton"))
        self.verticalLayout_2.addWidget(self.deleteButton)
        self.moveUpButton = QtGui.QPushButton(BusinessObjectForm)
        self.moveUpButton.setObjectName(_fromUtf8("moveUpButton"))
        self.verticalLayout_2.addWidget(self.moveUpButton)
        self.moveDownButton = QtGui.QPushButton(BusinessObjectForm)
        self.moveDownButton.setObjectName(_fromUtf8("moveDownButton"))
        self.verticalLayout_2.addWidget(self.moveDownButton)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.formLayout.setLayout(3, QtGui.QFormLayout.FieldRole, self.horizontalLayout)
        self.verticalLayout.addLayout(self.formLayout)
        self.boxButton = QtGui.QDialogButtonBox(BusinessObjectForm)
        self.boxButton.setOrientation(QtCore.Qt.Horizontal)
        self.boxButton.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.boxButton.setObjectName(_fromUtf8("boxButton"))
        self.verticalLayout.addWidget(self.boxButton)

        self.retranslateUi(BusinessObjectForm)
        QtCore.QMetaObject.connectSlotsByName(BusinessObjectForm)

    def retranslateUi(self, BusinessObjectForm):
        BusinessObjectForm.setWindowTitle(QtGui.QApplication.translate("BusinessObjectForm", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.nameLabel.setText(QtGui.QApplication.translate("BusinessObjectForm", "Name", None, QtGui.QApplication.UnicodeUTF8))
        self.idLabel.setText(QtGui.QApplication.translate("BusinessObjectForm", "ID", None, QtGui.QApplication.UnicodeUTF8))
        self.attributesLabel.setText(QtGui.QApplication.translate("BusinessObjectForm", "Attributes", None, QtGui.QApplication.UnicodeUTF8))
        self.descriptionLabel.setText(QtGui.QApplication.translate("BusinessObjectForm", "Description", None, QtGui.QApplication.UnicodeUTF8))
        self.addButton.setText(QtGui.QApplication.translate("BusinessObjectForm", "Add", None, QtGui.QApplication.UnicodeUTF8))
        self.deleteButton.setText(QtGui.QApplication.translate("BusinessObjectForm", "Delete", None, QtGui.QApplication.UnicodeUTF8))
        self.moveUpButton.setText(QtGui.QApplication.translate("BusinessObjectForm", "Move up", None, QtGui.QApplication.UnicodeUTF8))
        self.moveDownButton.setText(QtGui.QApplication.translate("BusinessObjectForm", "Move down", None, QtGui.QApplication.UnicodeUTF8))

