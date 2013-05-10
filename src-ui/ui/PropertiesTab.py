# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'PropertiesTab.ui'
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

class Ui_PropertiesTab(object):
    def setupUi(self, PropertiesTab):
        PropertiesTab.setObjectName(_fromUtf8("PropertiesTab"))
        PropertiesTab.resize(517, 450)
        self.formLayoutWidget = QtGui.QWidget(PropertiesTab)
        self.formLayoutWidget.setGeometry(QtCore.QRect(9, 9, 285, 98))
        self.formLayoutWidget.setObjectName(_fromUtf8("formLayoutWidget"))
        self.widget = QtGui.QFormLayout(self.formLayoutWidget)
        self.widget.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.widget.setMargin(0)
        self.widget.setObjectName(_fromUtf8("widget"))
        self.projectNameLabel = QtGui.QLabel(self.formLayoutWidget)
        self.projectNameLabel.setObjectName(_fromUtf8("projectNameLabel"))
        self.widget.setWidget(0, QtGui.QFormLayout.LabelRole, self.projectNameLabel)
        self.projectNameEdit = QtGui.QLineEdit(self.formLayoutWidget)
        self.projectNameEdit.setObjectName(_fromUtf8("projectNameEdit"))
        self.widget.setWidget(0, QtGui.QFormLayout.FieldRole, self.projectNameEdit)
        self.versionLabel = QtGui.QLabel(self.formLayoutWidget)
        self.versionLabel.setObjectName(_fromUtf8("versionLabel"))
        self.widget.setWidget(1, QtGui.QFormLayout.LabelRole, self.versionLabel)
        self.versionEdit = QtGui.QLineEdit(self.formLayoutWidget)
        self.versionEdit.setObjectName(_fromUtf8("versionEdit"))
        self.widget.setWidget(1, QtGui.QFormLayout.FieldRole, self.versionEdit)
        self.languageLabel = QtGui.QLabel(self.formLayoutWidget)
        self.languageLabel.setObjectName(_fromUtf8("languageLabel"))
        self.widget.setWidget(2, QtGui.QFormLayout.LabelRole, self.languageLabel)
        self.languageComboBox = QtGui.QComboBox(self.formLayoutWidget)
        self.languageComboBox.setObjectName(_fromUtf8("languageComboBox"))
        self.widget.setWidget(2, QtGui.QFormLayout.FieldRole, self.languageComboBox)

        self.retranslateUi(PropertiesTab)
        QtCore.QMetaObject.connectSlotsByName(PropertiesTab)

    def retranslateUi(self, PropertiesTab):
        PropertiesTab.setWindowTitle(QtGui.QApplication.translate("PropertiesTab", "PropertiesTab", None, QtGui.QApplication.UnicodeUTF8))
        self.projectNameLabel.setText(QtGui.QApplication.translate("PropertiesTab", "Project name", None, QtGui.QApplication.UnicodeUTF8))
        self.versionLabel.setText(QtGui.QApplication.translate("PropertiesTab", "Version", None, QtGui.QApplication.UnicodeUTF8))
        self.languageLabel.setText(QtGui.QApplication.translate("PropertiesTab", "Language", None, QtGui.QApplication.UnicodeUTF8))

