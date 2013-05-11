#!/usr/bin/env python

'''
Created on Apr 25, 2013

@author: Bartosz Alchimowicz
'''

import sys

sys.path.append('../src-ui')

from PyQt4 import QtCore, QtGui
from ui.UseCaseForm import Ui_UseCaseForm

try:
		_fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
		_fromUtf8 = lambda s: s

import main

class Delegate(QtGui.QItemDelegate):
	def createEditor(self, parent, option, index):

		if index.column() == 0:
			editor = QtGui.QSpinBox(parent)
			editor.setMinimum(0)
			editor.setMaximum(100)
		else:
			editor = QtGui.QPushButton(_fromUtf8("nazwa"), parent)

		return editor

	def setEditorData(self, editor, index):
		value = index.model().data(index, QtCore.Qt.EditRole).toInt()

		editor.setValue(value[0])

	def setModelData(self, editor, model, index):
		editor.interpretText()
		value = editor.value()
		model.setData(index, value, QtCore.Qt.EditRole)

	def updateEditorGeometry(self, editor, option, index ):
		editor.setGeometry(option.rect)

	def paint(self, painter, option, index):
#		if index.column() == 0:
#			btn->setGeometry(option.rect);
#			btn->setText(index.data().toString());
#			if (option.state == QStyle::State_Selected)
#										painter->fillRect(option.rect, option.palette.highlight());
#			QPixmap map = QPixmap::grabWidget(btn);
#			painter->drawPixmap(option.rect.x(),option.rect.y(),map);
#		else:
#			self.paint(painter, option, index);
		super(Delegate, self).paint(painter, option, index)



class UseCaseFormWrapper():
	def __init__(self, parent, afefuc, item = None):
		self.parent = parent

		self.dialog = QtGui.QDialog()
		self.form = Ui_UseCaseForm()
		self.afefuc = afefuc
		self.item = item

		self.mydelegate = Delegate(self.dialog)

	def load(self):
		pass
#		if self.item is not None:
#			print "load"
#			self.form.titleEdit.setText(_fromUtf8(" ".join([str(i) for i in self.afefuc['project'].ucspec.usecases[self.item].title])))
#			self.form.idEdit.setText(_fromUtf8(self.afefuc['project'].ucspec.usecases[self.item].identifier))

	def show(self):
		self.form.setupUi(self.dialog)

		self.load()

		QtCore.QObject.connect(self.form.buttonBox, QtCore.SIGNAL(_fromUtf8("clicked(QAbstractButton*)")), self.buttonBox_clicked)

		model = QtGui.QStandardItemModel(4, 2, self.dialog)

		for i in range(0, 4):
			for j in range(0, 2):
				print "a"
				index = model.index(i, j, QtCore.QModelIndex())
				model.setData(index, i)

		self.form.items.setModel(model)
		self.form.items.setItemDelegate(self.mydelegate)

		self.dialog.exec_()

	def cancelBtn_clicked(self):
		self.dialog.close()

	def okBtn_clicked(self):
		print "ActorFormWrapper.okBtn_clicked"

#		actor = model.Actor(str(self.form.nameEdit.text()),
#				str(self.form.idEdit.text()),
#				self.form.descriptionEdit.toPlainText())
#
#		self.parent.model.insertItem(actor)

		self.dialog.close()

	def buttonBox_clicked(self, btn):
		print "ActorFormWrapper.addBtn_clicked", ">%s<" % btn.text().toAscii()

		{
			'&Cancel': self.cancelBtn_clicked,
			'&OK': self.okBtn_clicked,
		}.get(str(btn.text()))()


if __name__ == "__main__":
	app = QtGui.QApplication(sys.argv)

	afefuc = {'project': main.project}

	myapp = UseCaseFormWrapper(app, afefuc, item = 0)
	myapp.show()
	sys.exit(app.exec_())
