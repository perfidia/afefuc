#!/usr/bin/env python

'''
Created on Apr 25, 2013

@author: Bartosz Alchimowicz
'''

import sys

sys.path.append('../src-ui')

from PyQt4 import QtCore, QtGui

from gui.MainWindowWrapper import MainWindowWrapper

if __name__ == "__main__":
	app = QtGui.QApplication(sys.argv)
	myapp = MainWindowWrapper()
	myapp.show()
	sys.exit(app.exec_())
