# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ItemsTab.ui'
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

class Ui_ItemsTab(object):
    def setupUi(self, ItemsTab):
        ItemsTab.setObjectName(_fromUtf8("ItemsTab"))
        ItemsTab.resize(524, 404)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(ItemsTab.sizePolicy().hasHeightForWidth())
        ItemsTab.setSizePolicy(sizePolicy)
        self.horizontalLayout_2 = QtGui.QHBoxLayout(ItemsTab)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setSizeConstraint(QtGui.QLayout.SetMaximumSize)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.itemsView = QtGui.QTableView(ItemsTab)
        self.itemsView.setObjectName(_fromUtf8("itemsView"))
        self.horizontalLayout.addWidget(self.itemsView)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.addButton = QtGui.QPushButton(ItemsTab)
        self.addButton.setObjectName(_fromUtf8("addButton"))
        self.verticalLayout.addWidget(self.addButton)
        self.editButton = QtGui.QPushButton(ItemsTab)
        self.editButton.setObjectName(_fromUtf8("editButton"))
        self.verticalLayout.addWidget(self.editButton)
        self.deleteButton = QtGui.QPushButton(ItemsTab)
        self.deleteButton.setObjectName(_fromUtf8("deleteButton"))
        self.verticalLayout.addWidget(self.deleteButton)
        self.moveUpButton = QtGui.QPushButton(ItemsTab)
        self.moveUpButton.setObjectName(_fromUtf8("moveUpButton"))
        self.verticalLayout.addWidget(self.moveUpButton)
        self.moveDownButton = QtGui.QPushButton(ItemsTab)
        self.moveDownButton.setObjectName(_fromUtf8("moveDownButton"))
        self.verticalLayout.addWidget(self.moveDownButton)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.horizontalLayout_2.addLayout(self.horizontalLayout)

        self.retranslateUi(ItemsTab)
        QtCore.QMetaObject.connectSlotsByName(ItemsTab)

    def retranslateUi(self, ItemsTab):
        ItemsTab.setWindowTitle(QtGui.QApplication.translate("ItemsTab", "ItemsTab", None, QtGui.QApplication.UnicodeUTF8))
        self.addButton.setText(QtGui.QApplication.translate("ItemsTab", "Add", None, QtGui.QApplication.UnicodeUTF8))
        self.editButton.setText(QtGui.QApplication.translate("ItemsTab", "Edit", None, QtGui.QApplication.UnicodeUTF8))
        self.deleteButton.setText(QtGui.QApplication.translate("ItemsTab", "Delete", None, QtGui.QApplication.UnicodeUTF8))
        self.moveUpButton.setText(QtGui.QApplication.translate("ItemsTab", "Move up", None, QtGui.QApplication.UnicodeUTF8))
        self.moveDownButton.setText(QtGui.QApplication.translate("ItemsTab", "Move down", None, QtGui.QApplication.UnicodeUTF8))

