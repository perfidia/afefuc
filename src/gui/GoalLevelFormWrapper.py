'''
Created on Apr 25, 2013

@author: Bartosz Alchimowicz
'''

from PyQt4 import QtCore, QtGui
from ui.LineEditForm import Ui_LineEditForm
from format import model

try:
		_fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
		_fromUtf8 = lambda s: s

class GoalLevelFormWrapper():
	def __init__(self, parent, afefuc, item = None):
		self.parent = parent

		self.dialog = QtGui.QDialog()
		self.form = Ui_LineEditForm()
		self.afefuc = afefuc
		self.item = item[1]
		self.item_orginal = item[0]

	def __fill(self):
		self.form.nameEdit.setText(_fromUtf8(self.item.name))

	def show(self):
		self.form.setupUi(self.dialog)

		self.__fill()

		QtCore.QObject.connect(self.form.boxButton, QtCore.SIGNAL(_fromUtf8("clicked(QAbstractButton*)")), self.clickedBoxButton)

		self.dialog.exec_()

	def clickedCancelButton(self):
		self.dialog.close()

	def clickedOKButton(self):
		self.item.name = unicode(self.form.nameEdit.text().toUtf8(), "utf-8")

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
