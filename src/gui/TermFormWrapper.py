'''
Created on May 22, 2013

@author: Bartosz Alchimowicz
'''

from PyQt4 import QtCore, QtGui
from generated.ui.TermForm import Ui_TermForm
#from format import model
from utils import converter
from utils import validation

try:
		_fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
		_fromUtf8 = lambda s: s

class TermFormWrapper():
	def __init__(self, parent, afefuc, item = None):
		self.parent = parent

		self.dialog = QtGui.QDialog()
		self.form = Ui_TermForm()
		self.afefuc = afefuc
		self.item = item[1]
		self.item_orginal = item[0]

	def load(self):
		self.form.nameEdit.setText(_fromUtf8(self.item.name))
		self.form.definitionEdit.setPlainText(
				_fromUtf8(
						converter.itemsToText(self.item.definition, edit = True)
				)
		)

	def show(self):
		self.form.setupUi(self.dialog)

		self.load()

		QtCore.QObject.connect(self.form.boxButton, QtCore.SIGNAL(_fromUtf8("accepted()")), self.clickedOKButton)
		QtCore.QObject.connect(self.form.boxButton, QtCore.SIGNAL(_fromUtf8("rejected()")), self.clickedCancelButton)

		self.dialog.exec_()

	def clickedCancelButton(self):
		self.dialog.close()

	def clickedOKButton(self):
		try:
			self.item.name = unicode(self.form.nameEdit.text().toUtf8(), "utf-8")
			self.item.definition = converter.textToItems(
					self.afefuc['project'],
					unicode(self.form.definitionEdit.toPlainText().toUtf8(), "utf-8")
			)
		except ValueError:
			validation.errorMessage(self.dialog, "Invalid reference")
			return
		

		# validate

		errors = validation.glossary(self.afefuc['project'], self.item, self.item_orginal is None)

		if errors:
			validation._show(self.dialog, errors)
			return

		if self.item_orginal:
			self.parent.model.updateItem((self.item_orginal, self.item))
		else:
			self.parent.model.insertItem((self.item_orginal, self.item))

		self.dialog.close()
