#!/usr/bin/python
#-*-coding: utf-8 -*-
import sys
from PyQt4 import QtCore, QtGui

from gui.UseCaseFormWrapper import UseCaseFormWrapper
from gui.BusinessObjectFormWrapper import BusinessObjectFormWrapper

import main, re
from format import model

try:
		_fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
		_fromUtf8 = lambda s: s

if __name__ == "__main__":
	app = QtGui.QApplication(sys.argv)
	#app.setStyle(QtGui.QStyleFactory.create("Plastique"))

	afefuc = {'project': main.project}

	item = model.UseCase([model.TextItem("")])
	item = afefuc['project'].ucspec.usecases[0]
	tableView = UseCaseFormWrapper(app, afefuc, (None, item))

	#item = afefuc['project'].business_objects[0]
	#tableView = BusinessObjectFormWrapper(app, afefuc, (None, item))

	#tableView.setGeometry(250, 300, 800, 300)
	tableView.show()

	sys.exit(app.exec_())
