'''
Created on Apr 25, 2013

@author: Bartosz Alchimowicz
'''

from PyQt4 import QtCore, QtGui
from ui.PropertiesTab import Ui_PropertiesTab

try:
		_fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
		_fromUtf8 = lambda s: s

class PropertiesTabWrapper():
	def __init__(self, parent, afefuc):
		self.parent = parent
		self.child = QtGui.QWidget(self.parent)
		self.tab = Ui_PropertiesTab()
		self.afefuc = afefuc

	def load(self):
		self.tab.projectNameEdit.setText(_fromUtf8(self.afefuc['project'].name))
		self.tab.versionEdit.setText(_fromUtf8(self.afefuc['project'].version))

		index = self.tab.languageComboBox.findText(_fromUtf8(self.afefuc['project'].language))
		if index != -1:
			self.tab.languageComboBox.setCurrentIndex(index);

	def show(self):
		self.tab.setupUi(self.child)
		self.parent.mainWindow.tabWidget.addTab(self.child, _fromUtf8("Properties"))

		self.tab.languageComboBox.addItems(["en", "pl"])
