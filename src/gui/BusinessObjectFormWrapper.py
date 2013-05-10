'''
Created on Apr 25, 2013

@author: Bartosz Alchimowicz
'''

from PyQt4 import QtCore, QtGui
from ui.BusinessObjectForm import Ui_BusinessObjectForm
from format import model
from utils import converter

try:
		_fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
		_fromUtf8 = lambda s: s

class ComboBoxDelegate(QtGui.QItemDelegate):
	def __init__(self, parent, item):
		QtGui.QItemDelegate.__init__(self, parent)
		self.item = item
		self.options = ["Main", "Supplementary"]

	def paint(self, painter, option, index):
		idx = self.item.attributes[index.row()].type
		idx = 0 if idx is None else self.options.index(idx)
		value = self.options[idx]

		style = QtGui.QApplication.style()

		opt = QtGui.QStyleOptionComboBox()
		opt.currentText = value
		opt.rect = option.rect

		style.drawComplexControl(QtGui.QStyle.CC_ComboBox, opt, painter)
		style.drawControl(QtGui.QStyle.CE_ComboBoxLabel, opt, painter)

	def createEditor(self, parent, option, index):
		editor = QtGui.QComboBox(parent)
		editor.addItems(self.options)

		return editor

	def setEditorData(self, editor, index):
		idx = self.item.attributes[index.row()].type
		idx = 0 if idx is None else self.options.index(idx)

		editor.setCurrentIndex(idx)

	def setModelData(self, editor, model, index):
		value = self.options[editor.currentIndex()]
		model.setData(index, QtCore.QVariant(value), QtCore.Qt.EditRole)

	def updateEditorGeometry(self, editor, option, index):
		editor.setGeometry(option.rect)

class AttributesTableModel(QtCore.QAbstractTableModel):
	def __init__(self, parent, afefuc, item):
		QtCore.QAbstractItemModel.__init__(self, parent)
		self.afefuc = afefuc
		self.parent = parent
		self.item = item
		self.headerdata = ["Name", "Type", "Description"]

	def headerData(self, column, orientation, role):
		if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
			return QtCore.QVariant(self.headerdata[column])

		return QtCore.QVariant()

	def rowCount(self, index):
		return len(self.item.attributes)

	def columnCount(self, parent):
		return 3

	def index(self, row, column, parent):
		if not parent.isValid():
			return self.createIndex(row, column, None)

	def data(self, index, role):
		column = index.column()

		if column == 0 and role in [QtCore.Qt.DisplayRole, QtCore.Qt.EditRole]:
			return QtCore.QVariant(self.item.attributes[index.row()].name)
		elif column == 1 and role == QtCore.Qt.DisplayRole:
			return QtCore.QVariant(self.item.attributes[index.row()].type)
		elif column == 2 and role == QtCore.Qt.DisplayRole:
			return QtCore.QVariant(converter.itemsToText(self.item.attributes[index.row()].description, edit = False))
		elif column == 2 and role == QtCore.Qt.EditRole:
			return QtCore.QVariant(converter.itemsToText(self.item.attributes[index.row()].description, edit = True))

	def parent(self, index):
		return QtCore.QModelIndex()

	def flags(self, index):
		flags = super(QtCore.QAbstractTableModel, self).flags(index)

		flags |= QtCore.Qt.ItemIsEditable|QtCore.Qt.ItemIsSelectable

		return flags

	def setData(self, index, value, role):
		if index.isValid() and role == QtCore.Qt.EditRole:
			value = unicode(value.toString().toUtf8(), 'utf-8')

			if index.column() == 0:
				self.item.attributes[index.row()].name = value
			elif index.column() == 1:
				self.item.attributes[index.row()].type = value
			elif index.column() == 2:
				self.item.attributes[index.row()].description = converter.textToItems(self.afefuc['project'], value)

			return True

		return False

	def removeItem(self, position):
		self.beginRemoveRows(QtCore.QModelIndex(), position, position);

		del(self.item.attributes[position])

		self.endRemoveRows()

		return True

	def insertItem(self, item):
		self.beginInsertRows(
				QtCore.QModelIndex(),
				self.rowCount(QtCore.QModelIndex()),
				self.rowCount(QtCore.QModelIndex())
		)

		self.item.attributes.append(item)

		self.endInsertRows()

	def movePositionUp(self, position):
		if position <= 0 or position == self.rowCount(QtCore.QModelIndex()):
			return

		pos1 = position
		pos2 = position - 1

		(
				self.item.attributes[pos1],\
				self.item.attributes[pos2] \
		) = (\
				self.item.attributes[pos2],\
				self.item.attributes[pos1] \
		)

		self.emit(
				QtCore.SIGNAL("dataChanged(QModelIndex, QModelIndex)"),
				self.createIndex(min(pos1, pos2), 0, None),
				self.createIndex(max(pos1, pos2), 1, None)
		)

	def movePositionDown(self, position):
		self.movePositionUp(position + 1)

class BusinessObjectFormWrapper():
	def __init__(self, parent, afefuc, item = None):
		self.parent = parent

		self.dialog = QtGui.QDialog()
		self.form = Ui_BusinessObjectForm()
		self.afefuc = afefuc
		self.item = item[1]
		self.item_orginal = item[0]

	def __fill(self):
		self.form.nameEdit.setText(_fromUtf8(converter.itemsToText(self.item.name, edit = True)))
		self.form.idEdit.setText(_fromUtf8(self.item.identifier))
		self.form.descriptionEdit.setPlainText(_fromUtf8(converter.itemsToText(self.item.description, edit = True)))

	def show(self):
		self.form.setupUi(self.dialog)

		self.model = AttributesTableModel(self.form.attributesView, self.afefuc, self.item)
		self.form.attributesView.setModel(self.model)
		self.form.attributesView.setItemDelegateForColumn(1, ComboBoxDelegate(self.form.attributesView, self.item))
		#self.form.attributesView.horizontalHeader().setResizeMode(0, QtGui.QHeaderView.ResizeToContents)
		self.form.attributesView.horizontalHeader().setResizeMode(2, QtGui.QHeaderView.Stretch)
		#self.form.attributesView.horizontalHeader().hide()
		self.form.attributesView.verticalHeader().hide()
		self.form.attributesView.setEditTriggers(QtGui.QAbstractItemView.CurrentChanged)

		self.__fill()

		QtCore.QObject.connect(self.form.boxButton, QtCore.SIGNAL(_fromUtf8("clicked(QAbstractButton*)")), self.clickedBoxButton)
		QtCore.QObject.connect(self.form.addButton, QtCore.SIGNAL(_fromUtf8("clicked()")), self.clickedAddButton)
		QtCore.QObject.connect(self.form.deleteButton, QtCore.SIGNAL(_fromUtf8("clicked()")), self.clickedDeleteButton)
		QtCore.QObject.connect(self.form.moveUpButton, QtCore.SIGNAL(_fromUtf8("clicked()")), self.clickedMoveUpButton)
		QtCore.QObject.connect(self.form.moveDownButton, QtCore.SIGNAL(_fromUtf8("clicked()")), self.clickedMoveDownButton)

		self.dialog.exec_()

	def clickedCancelButton(self):
		self.dialog.close()

	def clickedOKButton(self):
		self.item.name = converter.textToItems(
				self.afefuc['project'],
				unicode(self.form.nameEdit.text().toUtf8(), "utf-8")
		)
		self.item.identifier = unicode(self.form.idEdit.text().toUtf8(), "utf-8")
		self.item.description = converter.textToItems(
				self.afefuc['project'],
				unicode(self.form.descriptionEdit.toPlainText().toUtf8(), "utf-8")
		)

		if self.item_orginal:
			self.parent.model.updateItem((self.item_orginal, self.item))
		else:
			self.parent.model.insertItem((self.item_orginal, self.item))

		self.dialog.close()

	def clickedBoxButton(self, btn):
		{
			'&Cancel': self.clickedCancelButton,
			'&OK': self.clickedOKButton,
		}.get(str(btn.text()))()

	def clickedAddButton(self):
		self.model.insertItem(model.Attribute())

	def clickedDeleteButton(self):
		if len(self.form.attributesView.selectedIndexes()) == 1:
			position = self.form.attributesView.selectedIndexes()[0].row()

			self.model.removeItem(position)

	def clickedMoveUpButton(self):
		if len(self.form.attributesView.selectedIndexes()) == 1:
			position = self.form.attributesView.selectedIndexes()[0].row()

			self.model.movePositionUp(position)

	def clickedMoveDownButton(self):
		if len(self.form.attributesView.selectedIndexes()) == 1:
			position = self.form.attributesView.selectedIndexes()[0].row()

			self.model.movePositionDown(position)
