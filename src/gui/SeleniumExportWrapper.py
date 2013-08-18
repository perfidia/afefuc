#! /usr/bin/env python
#-*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
from generated.ui.SeleniumExport import Ui_SeleniumExport
from format.writer.selenium import selenium
from testcases.highlighter import highlighter

try:
		_fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
		_fromUtf8 = lambda s: s

class SeleniumExportWrapper():
	def __init__(self, parent, afefuc):
		self.parent = parent

		self.dialog = QtGui.QDialog()
		self.form = Ui_SeleniumExport()
		self.afefuc = afefuc
		self.system = None
		self.browser = None
		self.path = None
		self.tc = None

	def load(self):
		self.form.testCaseComboBox.addItem('All test cases', self.afefuc['project'].testcases.tests)

		for testcase in self.afefuc['project'].testcases.tests:
			self.form.testCaseComboBox.addItem(testcase.title, testcase)

	def show(self):
		self.form.setupUi(self.dialog)

		self.load()

		QtCore.QObject.connect(self.form.boxButton, QtCore.SIGNAL(_fromUtf8("accepted()")), self.clickedOKButton)
		QtCore.QObject.connect(self.form.boxButton, QtCore.SIGNAL(_fromUtf8("rejected()")), self.clickedCancelButton)
		QtCore.QObject.connect(self.form.selectPathButton, QtCore.SIGNAL(_fromUtf8("clicked()")), self.clickedSelectButton)

		self.dialog.exec_()

	def clickedCancelButton(self):
		self.dialog.close()

	def clickedOKButton(self):
		tccb = self.form.testCaseComboBox
		self.tc = tccb.itemData(tccb.currentIndex()).toPyObject()

		bccb = self.form.browserComboBox
		self.browser = bccb.currentText()

		sccb = self.form.systemComboBox
		self.system = sccb.currentText()
		
		if self.path:
			if len(self.tc) > 0:
				print '* exporting tests to selenium *'

				sb = None

				if self.afefuc['project'].language == 'en':
					sb = highlighter('generated/testcases/en.xml')
				else:
					sb = highlighter('generated/testcases/pl.xml')

				s = selenium(sb)

				for test in self.tc:
					try:
						s.generateCode(test, self.browser, self.system, self.path)
					except Exception as e:
						print 'Unexpected error occured in TC: ' + test.title
						print 'Error message: ' + e.message									

				print '* export finished *'
			else:
				print '* nothing to export *'
		else:
			print '* directory is not selected *'

		self.dialog.close()
		

	def clickedSelectButton(self):
		self.path = QtGui.QFileDialog.getExistingDirectory(self.dialog, 'Select directory')

		if self.path:
			self.form.pathLineEdit.setText(self.path)