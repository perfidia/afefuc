'''
Created on 19 Jun 2013

@author: Bartosz Alchimowicz
'''

from PyQt4 import QtGui, QtCore

#def identifier(parent):
#	return QtGui.QRegExpValidator(QtCore.QRegExp("[A-Z]+[A-Z_]*[0-9]*"), parent);

def _show(parent, errors):
	msg = ["The following errors were detected:"]

	for e in errors.items():
		msg.append("\n")
		msg.append("* %s" % e[0])
		msg.append(":\n")
		msg.append("\n".join(e[1]))

	QtGui.QMessageBox.about(parent, "Errors", "".join(msg))

def _is_empty(text):
	if len(text): return False

	return True

def priority(project, item):
	errors = {}

	if _is_empty(item.name):
		errors['Name'] = {"This field cannot be empty"}

	#if _is_unique(item.name, list_of_elements_to_check):
	#	errors['Name'] = {"The following name is not unique"}

	return errors

def goal_level(project, item):
	errors = {}

	if _is_empty(item.name):
		errors['Name'] = {"This field cannot be empty"}

	# is name unique

	return errors

def business_object(project, item):
	errors = {}

	if _is_empty(item.name):
		errors['Name'] = {"This field cannot be empty"}

	# is unique

	if _is_empty(item.identifier):
		errors['ID'] = {"This field cannot be empty"}

	# is unique

	# check attributes

	return errors

def business_rule(project, item):
	errors = {}

	if _is_empty(item.identifier):
		errors['ID'] = {"This field cannot be empty"}

	return errors

def actor(project, item):
	errors = {}

	if _is_empty(item.name):
		errors['Name'] = {"This field cannot be empty"}

	if _is_empty(item.identifier):
		errors['ID'] = {"This field cannot be empty"}

	return errors

def usecase(project, item):
	errors = {}

	if _is_empty(item.name):
		errors['Name'] = {"This field cannot be empty"}

	# is uniqie

	if _is_empty(item.identifier):
		errors['ID'] = {"This field cannot be empty"}

	# is unique

	# all uc should end with @eouc
	# all events shoud end with @eouc or @goto
	# references in uc should exist
	# conditions should be non empty
	# there should be at least one main actor

	return errors

def glossary(project, item):
	errors = {}

	if _is_empty(item.name):
		errors['Name'] = {"This field cannot be empty"}

	# is unique

	if _is_empty(item.definition):
		errors['Definition'] = {"This field cannot be empty"}

	# is unique

	return errors
