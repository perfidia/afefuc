'''
Created on 19 Jun 2013

@author: Bartosz Alchimowicz
'''

from PyQt4 import QtGui, QtCore
import re
#def identifier(parent):
#	return QtGui.QRegExpValidator(QtCore.QRegExp("[A-Z]+[A-Z_]*[0-9]*"), parent);

name_pattern = re.compile(r"[A-Z]+[a-z0-9_]*")

def _show(parent, errors):
	msg = ["The following errors were detected:"]

	for e in errors.items():
		msg.append("\n")
		msg.append("* %s" % e[0])
		msg.append(":\n")
		msg.append("\n".join(e[1]))

	QtGui.QMessageBox.about(parent, "Errors", "".join(msg))

def _is_unique(item, itemsList):
	if itemsList.count(item) > 1:
		return False
	
	return True

def _count_field(test_item, items_list, field_name):
	
	count = 0;
	for item in items_list:
		if getattr(item, field_name) == getattr(test_item, field_name):
			count += 1
	
	return count

def _is_empty(text):
	if len(text): return False

	return True

def _is_identifier(text):

	if not re.match(r"[A-Z]+[A-Z_]*[0-9]*", text):
		return False

	return True

def _is_name(text):

	#import pdb
	#pdb.set_trace()
	if not name_pattern.match(text):
# 	if not re.match(r"[A-Z]+[a-z0-9_]*", text):
		return False

	return True

def priority(project, item):
	errors = {}

	if(_is_name(item.name) == False):
		errors['Name'] = {"This field is not a valid name"}

	if _is_empty(item.name):
		errors['Name'] = {"This field cannot be empty"}

	if _count_field(item, project.ucspec.priorities, "name") > 0:
		errors['Name'] = {"The following name is not unique"}

	return errors

def goal_level(project, item):
	errors = {}

	if(_is_name(item.name) == False):
		errors['Name'] = {"This field is not a valid name"}

	if _is_empty(item.name):
		errors['Name'] = {"This field cannot be empty"}

	if _count_field(item, project.ucspec.goal_levels, "name") > 0:
		errors['Name'] = {"The following name is not unique"}

	return errors

def business_object(project, item):
	errors = {}

	if(_is_name(item.name[0].toText()) == False):
		errors['Name'] = {"This field is not a valid name"}

	if _is_empty(item.name):
		errors['Name'] = {"This field cannot be empty"}

	if _count_field(item, project.business_objects, "name") > 0:
		errors['Name'] = {"The following name is not unique"}

	if(_is_identifier(item.identifier) == False):
		errors['ID'] = {"This field is not a valid identifier"}

	if _is_empty(item.identifier):
		errors['ID'] = {"This field cannot be empty"}

	if _count_field(item, project.business_objects, "identifier") > 0:
		errors['ID'] = {"The following identifier is not unique"}

	for a in item.attributes:
		if(_is_name(a.name) == False):
			errors['Attribute name'] = {"Attribute has not a valid name"}
		
		if(_is_empty(a.name) == True):
			errors['Attribute description'] = {"Attribute descripton couldn't be empty"}

	return errors

def business_rule(project, item):
	errors = {}

	if(_is_identifier(item.identifier) == False):
		errors['ID'] = {"This field is not a valid identifier"}

	if _is_empty(item.identifier):
		errors['ID'] = {"This field cannot be empty"}

	return errors

def actor(project, item):
	errors = {}
	
	if(_is_name(item.name) == False):
		errors['Name'] = {"This field is not a valid name"}
		
	if _is_empty(item.name):
		errors['Name'] = {"This field cannot be empty"}
		
	if(_is_identifier(item.identifier) == False):
		errors['ID'] = {"This field is not a valid identifier"}
		
	if _is_empty(item.identifier):
		errors['ID'] = {"This field cannot be empty"}
		
	if _count_field(item, project.actors, "name") > 0:
		errors['Name'] = {"The following name is not unique"}
	
	if _count_field(item, project.actors, "identifier") > 0:
		errors['ID'] = {"The following identifier is not unique"}

	return errors

def usecase(project, item):
	errors = {}
	
	if _is_empty(item.title):
		errors['Title'] = {"This field cannot be empty"}

	if _count_field(item, project.ucspec.usecases, 'title') > 0:
		errors['Title'] = {"Title should be unique"}

	if(_is_identifier(item.identifier) == False):
		errors['ID'] = {"This field is not a valid identifier"}

	if _is_empty(item.identifier):
		errors['ID'] = {"This field cannot be empty"}

	if _count_field(item, project.ucspec.usecases, 'identifier') > 0:
		errors['ID'] = {"Identifier should be unique"}
	
	# there should be at least one main actor and one other
	if len(item.main_actors) == 0:
		errors['main_actors'] = {"There should be at least one main actor"}
	if len(item.other_actors) == 0:
		errors['main_actors'] = {"There should be at least one other actor"}
	if len(item.preconditions) == 0:
		errors['preconditions'] = {"There should be at least one precondition"} # conditions should be non empty
	if len(item.postconditions) == 0:
		errors['postconditions'] = {"There should be at least one postcondition"}
		
	
	#import pdb
	#pdb.set_trace()
	
	# all uc should end with @eouc
	# all events should end with @eouc or @goto
	# step in uc cannot be empty
	# references in uc should exist
	
	
	
	
	#for step in item.scenario.events:
		
		

	return errors

def glossary(project, item):
	errors = {}

	if(_is_name(item.name) == False):
		errors['Name'] = {"This field is not a valid name"}

	if _is_empty(item.name):
		errors['Name'] = {"This field cannot be empty"}

	if _count_field(item, project.glossary, 'name') > 0:
		errors['Name'] = {"Name should be unique"}
		
	if _count_field(item, project.glossary, 'definition') > 0:
		errors['Definition'] = {"Definition should be unique"};


	return errors
