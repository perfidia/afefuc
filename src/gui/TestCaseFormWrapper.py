import re
import inspect

from PyQt4 import QtCore, QtGui
from generated.ui.TestCaseForm import Ui_TestCaseForm
from format import model
from utils import converter
from SelectActorsFormWrapper import SelectActorsFormWrapper

import sip
#sip.setapi('QString', 2)

from os import path
from sys import argv, exit
from xml.dom import minidom
from testcases.highlighter import highlighter

try:
	_fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
			 _fromUtf8 = lambda s: s

class Test(QtGui.QWidget):
	def __init__( self, labelText, parent=None):
		super(Test, self).__init__(parent)

		self.completingTextEdit = TextEdit()
		self.completer = QtGui.QCompleter(self)

		sb = highlighter('./generated/testcases/en.xml')
		self.completingTextEdit.sethighlighter(sb)
		output = sb.getNext('')
		words = []
		for element in output[1]:
			words.append(element.getValue())
		self.completer.setModel(QtGui.QStringListModel(words, self.completer))
		self.completer.setModelSorting(QtGui.QCompleter.CaseInsensitivelySortedModel)
		self.completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
		self.completer.setWrapAround(False)
		self.completingTextEdit.setCompleter(self.completer)

		self.label = QtGui.QLabel(labelText)

		layout = QtGui.QVBoxLayout()
		layout.addWidget(self.label)
		layout.addWidget(self.completingTextEdit)
		self.setLayout(layout)

class TextEdit(QtGui.QTextEdit):
	def __init__(self, parent=None):
		super(TextEdit, self).__init__(parent)

		self._completer = None
		self._highlighter = None

	def setCompleter(self, c):
		if self._completer is not None:
				self._completer.activated.disconnect()

		self._completer = c

		c.setWidget(self)
		c.setCompletionMode(QtGui.QCompleter.PopupCompletion)
		c.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
		c.activated.connect(self.insertCompletion)

	def completer(self):
		return self._completer

	def sethighlighter(self, s):
		self._highlighter = s

	def highlighter(self):
		return self._highlighter

	def textUnderCursor(self):
		tc = self.textCursor()
		tc.select(QtGui.QTextCursor.WordUnderCursor)
		return tc.selectedText()

	def lineUnderCursor(self):
		tc = self.textCursor()
		tc.select(QtGui.QTextCursor.LineUnderCursor)
		return tc.selectedText()

	def insertCompletion(self, completion):
		if self._completer.widget() is not self:
			return

		if self.textUnderCursor() == completion:
			return

		tc = self.textCursor()
		extra = len(completion) - len(self._completer.completionPrefix())
		tc.movePosition(QtGui.QTextCursor.EndOfWord)
		tc.insertText(completion[-extra:])
		self.setTextCursor(tc)

	def focusInEvent(self, e):
		if self._completer is not None:
			self._completer.setWidget(self)

		super(TextEdit, self).focusInEvent(e)

	def formatInput(self):
		textInTheBox = self.toPlainText()
		#
		#here goes parser code
		#
		tekstWyjsciowy = ""
		licznik = 0

		#sb = highlighter('XMLConverter/sentencesStructure.XML')
		output = self._highlighter.getNext(self.lineUnderCursor())
		#print self.lineUnderCursor()
		#print output[2]

		oldCursor = self.textCursor().position()
		myCursor = self.textCursor()

		#self.setHtml('<font color=red>'+textInTheBox+'</font>')

		myCursor.select(QtGui.QTextCursor.LineUnderCursor)
		myCursor.removeSelectedText()
		self.insertHtml(output[2])

		myCursor.setPosition(oldCursor)
		self.setTextCursor(myCursor)

	def keyReleaseEvent(self, e):
		#print e.key()
		if e.key() != 16777220 and e.key() != 32:
			self.formatInput()
		#output = self._highlighter.getNext(self.lineUnderCursor())
		#tc = self.textCursor()
		#tc.select(QtGui.QTextCursor.LineUnderCursor)
		#tc.removeSelectedText()
		#tc.insertHtml(output[2])
		#self.formatInput()
		#return

	def keyPressEvent(self, e):
		if self._completer is not None and self._completer.popup().isVisible():
			if e.key() in (QtCore.Qt.Key_Enter, QtCore.Qt.Key_Return, QtCore.Qt.Key_Escape, QtCore.Qt.Key_Tab, QtCore.Qt.Key_Backtab):
				e.ignore()
				return

		modifiers = e.modifiers()
		isShortcut = (modifiers == QtCore.Qt.ControlModifier and e.key() == QtCore.Qt.Key_Space)
		if self._completer is None or not isShortcut:
			super(TextEdit, self).keyPressEvent(e)

		output = self._highlighter.getNext(self.lineUnderCursor())
		words = []
		for element in output[1]:
			words.append(element.getValue())
		self._completer.setModel(QtGui.QStringListModel(words, self._completer))

		completionPrefix = self.textUnderCursor()

		if completionPrefix != self._completer.completionPrefix():
			self._completer.setCompletionPrefix(completionPrefix)
			self._completer.popup().setCurrentIndex(self._completer.completionModel().index(0, 0))

		cr = self.cursorRect()
		cr.setWidth(self._completer.popup().sizeHintForColumn(0) + self._completer.popup().verticalScrollBar().sizeHint().width())
		self._completer.complete(cr)

class TestCaseFormWrapper():
	def __init__(self, parent, afefuc, item=None):
		self.parent = parent

		self.dialog = QtGui.QDialog()
		self.form = Ui_TestCaseForm()
#self.form.handler.add(buttonAddingEditTexts)
#self.form.handler.add(ourTextEdit)
		self.afefuc = afefuc
		self.item = item[1]
		self.item_original = item[0]

	def load(self):
		pass

	def show(self):
		self.form.setupUi(self.dialog)

		self.load()

		#self.addButton = QtGui.QPushButton('button to add other widgets')
#       self.form.widget.addWidget(self.addButton2)
		self.form.insertStep.clicked.connect(self.addWidget)

		# scroll area widget contents - layout
		self.scrollLayout = QtGui.QFormLayout()

		# scroll area widget contents
		self.scrollWidget = QtGui.QWidget()
		self.scrollWidget.setLayout(self.scrollLayout)

		# scroll area
		self.scrollArea = QtGui.QScrollArea()
		self.scrollArea.setWidgetResizable(True)
		self.scrollArea.setWidget(self.scrollWidget)

		# main layout
		#self.mainLayout = self.form.widget

		# add all main to the main vLayout
		#self.form.widget.addWidget(self.addButton)
		self.form.widget.addWidget(self.scrollArea)

		# central widget
#       self.centralWidget = QtGui.QWidget()
#       self.centralWidget.setLayout(self.mainLayout)

		# set central widget
# 		self.setCentralWidget(self.centralWidget)

		QtCore.QObject.connect(self.form.boxButton, QtCore.SIGNAL(_fromUtf8("accepted()")), self.clickedOKButton)
		QtCore.QObject.connect(self.form.boxButton, QtCore.SIGNAL(_fromUtf8("rejected()")), self.clickedCancelButton)

		self.dialog.exec_()

	def addWidget(self):
		self.scrollLayout.addRow(Test('testowy tekst'))

	def getTextAttribute(self, node):
		if node.attributes:
			for i in range(node.attributes.length):
				if node.attributes.item(i).name == 'value':
					return node.attributes.item(i).value

	def readNodes(self, inputNodes, outputList):
		for element in inputNodes:
			if element.attributes:
				attr = self.getTextAttribute(element)
				outputList.insert(len(outputList), [self.getTextAttribute(element)])
			if element.childNodes:
				self.readNodes(element.childNodes, outputList[len(outputList)-1])

	def findChild(self, myList, childName):
		for idx, elem in enumerate(myList):
			for childName in elem:
				return idx
		return -1

	#returns 'children'
	def goDeeperForCompletion(self, myList):
		toReturn = []
		self.goDeeperForCompletionRecursive(myList[1:], toReturn)
		return toReturn

	def goDeeperForCompletionRecursive(self, myList, toReturn):
		for elem in myList:
			if elem[0][0] == '[':
				toReturn = (self.goDeeperForCompletionRecursive(elem[1:], toReturn))
			else:
				for idx, elem in enumerate(myList):
					toReturn.append(elem)
		return toReturn

	def getCurrentOptions(self, myList):
		toReturn = []
		for elem in myList:
			toReturn.append(elem[0])
		return toReturn

	def get_data(self, model):
		#model.setStringList(["completion", "data", "goes", "here"]) #works
		self.currentOptions = self.getCurrentOptions(self.completionInformation)
		#self.currentOptions = ['foo', 'bar', 'chicken'] #doesn't work
		model.setStringList(self.currentOptions)
		print self.getCurrentOptions(self.completionInformation)

	def createMenu(self):
		exitAction = QtGui.QAction("Exit", self)

		exitAction.triggered.connect(QtGui.qApp.quit)

		fileMenu = self.menuBar().addMenu("File")
		fileMenu.addAction(exitAction)

	def modelFromFile(self, fileName):
		f = QtCore.QFile(fileName)
		if not f.open(QtCore.QFile.ReadOnly):
			return QtGui.QStringListModel(self.completer)

		QtGui.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))

		words = []
		while not f.atEnd():
			line = f.readLine().trimmed()
			if line.length() != 0:
				try:
					line = str(line, encoding='ascii')
				except TypeError:
					line = str(line)

				words.append(line)

		QtGui.QApplication.restoreOverrideCursor()

		return QtGui.QStringListModel(words, self.completer)

	def clickedCancelButton(self):
		self.dialog.close()

	def clickedOKButton(self):
		self.dialog.close()
