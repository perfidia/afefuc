'''
Created on Apr 25, 2013

@author: Bartosz Alchimowicz
'''

import os

from PyQt4 import QtCore, QtGui
from ui.MainWindow import Ui_MainWindow
from gui.ActorsTabWrapper import ActorsTabWrapper
from gui.PropertiesTabWrapper import PropertiesTabWrapper
from gui.UseCasesTabWrapper import UseCasesTabWrapper
from gui.PrioritiesTabWrapper import PrioritiesTabWrapper
from gui.GoalLevelsTabWrapper import GoalLevelsTabWrapper
from gui.BusinessObjectsTabWrapper import BusinessObjectsTabWrapper
from gui.BusinessRulesTabWrapper import BusinessRulesTabWrapper
from gui.TestCasesTabWrapper import TestCasesTabWrapper
import format.writer.xml
import format.reader.xml
import format.model

try:
		_fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
		_fromUtf8 = lambda s: s

class MainWindowWrapper(QtGui.QMainWindow):
	def __init__(self, parent=None):
		QtGui.QWidget.__init__(self, parent)
		self.mainWindow = Ui_MainWindow()
		self.afefuc = {'project': None}
		self.filename = None

	def show(self):
		super(QtGui.QMainWindow, self).show()

		self.mainWindow.setupUi(self)

		self.afefuc["project"] = format.model.Project()
		self.mainWindow.tabWidget.hide()

		screen = QtGui.QApplication.desktop().screenGeometry()
		self.move(screen.center() - self.rect().center())
		self.activateWindow()

		self.mainWindow.actionNew.triggered.connect(self.clickedNew)
		self.mainWindow.actionOpen.triggered.connect(self.clickedOpen)
		self.mainWindow.actionSave.triggered.connect(self.clickedSave)
		self.mainWindow.actionSaveAs.triggered.connect(self.clickedSaveAs)
		self.mainWindow.actionClose.triggered.connect(self.clickedClose)
		self.mainWindow.actionQuit.triggered.connect(self.clickedQuit)
		self.mainWindow.actionDump.triggered.connect(self.clickedDump)

		self.propertiesTab = PropertiesTabWrapper(self, self.afefuc)
		self.propertiesTab.show()

		self.prioritiesTab = PrioritiesTabWrapper(self, self.afefuc)
		self.prioritiesTab.show()

		self.goalLevelTab = GoalLevelsTabWrapper(self, self.afefuc)
		self.goalLevelTab.show()

		self.businessObjectsTab = BusinessObjectsTabWrapper(self, self.afefuc)
		self.businessObjectsTab.show()

		self.businessRulesTab = BusinessRulesTabWrapper(self, self.afefuc)
		self.businessRulesTab.show()

		self.actorsTab = ActorsTabWrapper(self, self.afefuc)
		self.actorsTab.show()

		self.usecasesTab = UseCasesTabWrapper(self, self.afefuc)
		self.usecasesTab.show()

		self.testcasesTab = TestCasesTabWrapper(self, self.afefuc)
		self.testcasesTab.show()

		if os.path.isfile("../private/data.py"):
			import sys
			print "using debug data"

			sys.path.append('../private')
			import data
			self.afefuc["project"] = data.project
			self.load()
			self.mainWindow.tabWidget.show()

	def load(self):
		self.propertiesTab.load()
		self.prioritiesTab.load()
		self.goalLevelTab.load()
		self.businessObjectsTab.load()
		self.businessRulesTab.load()
		self.actorsTab.load()
		self.usecasesTab.load()
		self.testcasesTab.load()

	def clickedNew(self):
		self.clickedClose()
		self.mainWindow.tabWidget.show()

		self.afefuc["project"] = format.model.Project()

		self.load()

	def clickedOpen(self):
		filename = QtGui.QFileDialog.getOpenFileName(self, "Open", "", "AFEFUC (*.auc)")

		if filename:
			filename = unicode(filename.toUtf8(), "utf-8")

			self.clickedClose()

			self.filename = filename

			self.afefuc['project'] = format.reader.xml.read(self.filename)

			self.load()
			self.mainWindow.tabWidget.show()

	def clickedSave(self, saveAs = False):
		if self.afefuc['project'] and (not self.filename or saveAs == True):
			self.filename = QtGui.QFileDialog.getSaveFileName(self, "Save as", "", "AFEFUC (*.auc)")

		if self.filename:
			if self.filename[-4:] != '.auc':
				self.filename += ".auc"

			format.writer.xml.write(self.filename, self.afefuc['project'])

	def clickedSaveAs(self):
		self.clickedSave(saveAs = True)

	def clickedClose(self):
		self.filename = None
		self.afefuc['project']= None
		self.mainWindow.tabWidget.hide()

	def clickedQuit(self):
		self.close()

	def clickedDump(self):
		format.writer.xml.attach();
		retval = self.afefuc['project'].to_xml();
		open("tmp.auc", "w").write(retval)

		format.writer.xml.detach()
