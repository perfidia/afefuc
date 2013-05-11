'''
Created on Apr 25, 2013

@author: Bartosz Alchimowicz
'''

from PyQt4 import QtCore, QtGui
from ui.ActorForm import Ui_ActorForm
#from format import model
from utils import converter

try:
		_fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
		_fromUtf8 = lambda s: s

class ActorFormWrapper():
	def __init__(self, parent, afefuc, item = None):
		self.parent = parent

		self.dialog = QtGui.QDialog()
		self.form = Ui_ActorForm()
		self.afefuc = afefuc
		self.item = item[1]
		self.item_orginal = item[0]

	def load(self):
		self.form.nameEdit.setText(_fromUtf8(self.item.name))
		self.form.idEdit.setText(_fromUtf8(self.item.identifier))

		self.form.descriptionEdit.setPlainText(
				_fromUtf8(
						converter.itemsToText(self.item.description, edit = True)
				)
		)

		index = self.form.typeComboBox.findText(_fromUtf8(self.item.type))
		if index != -1:
			self.form.typeComboBox.setCurrentIndex(index)

	def show(self):
		self.form.setupUi(self.dialog)

		self.form.typeComboBox.addItems(["Human", "System"])

		self.laod()

		QtCore.QObject.connect(self.form.boxButton, QtCore.SIGNAL(_fromUtf8("accepted()")), self.clickedOKButton)
		QtCore.QObject.connect(self.form.boxButton, QtCore.SIGNAL(_fromUtf8("rejected()")), self.clickedCancelButton)

		self.dialog.exec_()

	def clickedCancelButton(self):
		self.dialog.close()

	def clickedOKButton(self):
		self.item.name = unicode(self.form.nameEdit.text().toUtf8(), "utf-8")
		self.item.identifier = unicode(self.form.idEdit.text().toUtf8(), "utf-8")
		self.item.description = converter.textToItems(
				self.afefuc['project'],
				unicode(self.form.descriptionEdit.toPlainText().toUtf8(), "utf-8")
		)

		self.item.type = unicode(self.form.typeComboBox.currentText().toUtf8(), "utf-8")

		if self.item_orginal:
			self.parent.model.updateItem((self.item_orginal, self.item))
		else:
			self.parent.model.insertItem((self.item_orginal, self.item))

		self.dialog.close()
