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
from testcases.Models.sentenceBuilder import sentenceBuilder
from testcases.Models.sentenceBuilder import sentenceElement

try:
	_fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
			 _fromUtf8 = lambda s: s

#wstawic tabele
#jako pole tabeli dac comboBox

class CompleteTextEditDelegate(QtGui.QItemDelegate):
	def __init__(self, parent, item): #item trzyma informacje o naszym modelu
		QtGui.QItemDelegate.__init__(self, parent)
		self.item = item


	def createEditor(self, parent, option, index):
		editor = TextEdit(parent)
		self.completer = QtGui.QCompleter(self)

		sb = sentenceBuilder('testcases/Models/sentencesStructure.XML')
		editor.setSentenceBuilder(sb)
		output = sb.getNext('')
		words = []
		for element in output[1]:
			words.append(element.getValue())
		self.completer.setModel(QtGui.QStringListModel(words, self.completer))
		self.completer.setModelSorting(QtGui.QCompleter.CaseInsensitivelySortedModel)
		self.completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
		self.completer.setWrapAround(False)
		editor.setCompleter(self.completer)
		

		return editor

	def setEditorData(self, editor, index):	#transfers data from internal model to editor
		editor.setHtml(self.item.path[index.row()])
		print 'setEditorData placeholder'

	def setModelData(self, editor, model, index):	#Ttransfers data from editor to internal model
		self.item.path[index.row()] = editor.toPlainText()
		#self.item.html = editor.toHtml()
		#model.setData(index, QtCore.QVariant('self.item.text'), QtCore.Qt.EditRole) #po co?
		print 'setModelData placeholder'

	def updateEditorGeometry(self, editor, option, index):
		editor.setGeometry(option.rect)


class SampleTableModel(QtCore.QAbstractTableModel):
	def __init__(self, parent, afefuc, items):
		QtCore.QAbstractItemModel.__init__(self,parent)
		self.afefuc = afefuc
		self.parent = parent
		self.item = items[1]
		self.item_original = items[0]
		self.headerdata = ["No", "Description"]

	def headerData(self, column, orientation, role):
		if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
			return QtCore.QVariant(self.headerdata[column])
		return QtCore.QVariant()

	def rowCount(self, index):
		return len(self.item.path)

	def columnCount(self, parent):
		return 2

	def index(self, row, column, parent): #TODO ok (?)
		if not parent.isValid():
			return self.createIndex(row, column, None)

	def data(self, index, role): #kod wyswietlajacy zawartosc elementu z modelu
		column = index.column()
		row = index.row()
		
		if column == 0 and role == QtCore.Qt.DisplayRole:
			return QtCore.QVariant(row+1)
		elif column == 1 and role in [QtCore.Qt.DisplayRole, QtCore.Qt.EditRole]:
			#step = self.item.scenario.items[row]
			#TODO converter
			step = self.item.path[row]
			return QtCore.QVariant(step)

	def parent(self, index):
		return QtCore.QModelIndex()

	def flags(self, index):
		flags = super(QtCore.QAbstractTableModel, self).flags(index)

		if(index.column() == 1):
			flags |= QtCore.Qt.ItemIsEditable|QtCore.Qt.ItemIsSelectable
			
		return flags	

	def setData(self, index, value, role):
		if index.isValid() and role == QtCore.Qt.EditRole:
			value = unicode(value.toString().toUtf8(), 'utf-8')
			#kod wstawiajacy czesc elementu do naszego modelu
			#if index.column() == 0:
			#	self.item.attributes[index.row()].name = value
			#elif index.column() == 1:
			#	self.item.attributes[index.row()].type = value
			#elif index.column() == 2:
			#	self.item.attributes[index.row()].description = converter.textToItems(self.afefuc['project'], value)
			self.item.path[index.row()] = items
			return True

		return False

	def insertItem(self, item, position = None):
		if position is None:
			first = self.rowCount(QtCore.QModelIndex())
			last = self.rowCount(QtCore.QModelIndex())
		else:
			first = position 	#wstawianie wiersza pomiedzy inne wiersze
			last = position

		self.beginInsertRows(QtCore.QModelIndex(), first, last)
#TODO item.scenario.items (lista)
		if position is None: #dodanie nowego wezla do modelu
			#self.item.scenario.items.append(item)
			self.item.path.append(item)
			print 'position is None'
		else: #dodanie nowego wezla w srodek modelu
			#self.item.scenario.items.insert(position, item)
			self.item.path.insert(position, item)
			print 'position is not None'

		self.endInsertRows()

	def removeItem(self, position):
		self.beginRemoveRows(QtCore.QModelIndex(), position, position)
		#TODO usuwanie danych z modelu
		#del(self.item.scenario.items[position])
		self.endRemoveRows()
		return True

	def movePositionUp(self, position):
		if position <= 0 or position == self.rowCount(QtCore.QModelIndex()):
			return

		pos1 = position
		pos2 = position - 1
		#kod zamieniajacy dwa elementy miejscami w modelu
		(
				self.item.path[pos1],\
				self.item.path[pos2] \
		) = (\
				self.item.path[pos2],\
				self.item.path[pos1] \
		)

		self.emit(
				QtCore.SIGNAL("dataChanged(QModelIndex, QModelIndex)"),
				self.createIndex(min(pos1, pos2), 0, None),
				self.createIndex(max(pos1, pos2), 1, None)
		)

	def movePositionDown(self, position):
		self.movePositionUp(position + 1)

class Test(QtGui.QWidget):
	def __init__( self, labelText, parent=None):
		super(Test, self).__init__(parent)

		self.completingTextEdit = TextEdit()
		self.completer = QtGui.QCompleter(self)

		sb = sentenceBuilder('testcases/Models/sentencesStructure.XML')
		self.completingTextEdit.setSentenceBuilder(sb)
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
		self._sentenceBuilder = None

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

	def setSentenceBuilder(self, s):
		self._sentenceBuilder = s

	def sentenceBuilder(self):
		return self._sentenceBuilder

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

		#sb = sentenceBuilder('XMLConverter/sentencesStructure.XML')
		output = self._sentenceBuilder.getNext(self.lineUnderCursor())
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
		#output = self._sentenceBuilder.getNext(self.lineUnderCursor())
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

		output = self._sentenceBuilder.getNext(self.lineUnderCursor())
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
		#self.foo = self.form.boxButton
		#self.model = SampleTableModel(self.form.stepView, self.afefuc, self.item)

	def load(self):
		pass

	def show(self):
		self.form.setupUi(self.dialog)

		self.load()

		#self.addButton = QtGui.QPushButton('button to add other widgets')
#       self.form.widget.addWidget(self.addButton2)
		#self.form.insertStep.clicked.connect(self.addWidget)

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
		#self.form.widget.addWidget(self.scrollArea)

		# central widget
#       self.centralWidget = QtGui.QWidget()
#       self.centralWidget.setLayout(self.mainLayout)

		# set central widget
# 		self.setCentralWidget(self.centralWidget)

		QtCore.QObject.connect(self.form.boxButton, QtCore.SIGNAL(_fromUtf8("accepted()")), self.clickedOKButton)
		QtCore.QObject.connect(self.form.boxButton, QtCore.SIGNAL(_fromUtf8("rejected()")), self.clickedCancelButton)
		QtCore.QObject.connect(self.form.insertStepButton, QtCore.SIGNAL(_fromUtf8("clicked()")), self.clickedInsertStepButton)

		self.modelTC = SampleTableModel(self.form.stepView, self.afefuc, (self.item_original, self.item))
		self.form.stepView.setModel(self.modelTC)
		self.form.stepView.setItemDelegateForColumn(1, CompleteTextEditDelegate(self.form.stepView, self.item))
		
		self.form.stepView.horizontalHeader().setResizeMode(0, QtGui.QHeaderView.ResizeToContents)
		self.form.stepView.horizontalHeader().setResizeMode(1, QtGui.QHeaderView.Stretch)
		self.form.stepView.setColumnWidth(2, 20)
		#self.form.stepView.horizontalHeader().hide()
		#self.form.stepView.verticalHeader().hide()
		#self.form.stepView.setEditTriggers(QtGui.QAbstractItemView.CurrentChanged)
		#self.form.stepView.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
		#self.form.stepView.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)


		self.dialog.exec_()

	def clickedInsertStepButton(self):
		step = model.Step()
		step.setParent(self.item)

		if len(self.form.stepView.selectedIndexes()) != 0:
			position = self.form.stepView.selectedIndexes()[0].row()

			self.modelTC.insertItem(step, position)
		else:
			self.modelTC.insertItem(step)

	#def addWidget(self):
	#	self.scrollLayout.addRow(Test('testowy tekst'))

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
