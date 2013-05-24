'''
Created on May 9, 2013

@author: Bartosz Alchimowicz
'''

import copy
import clone

import format.model

def actor(target, source):
	target.name = source.name
	target.identifier = source.identifier
	target.type = source.type
	target.communication = source.communication
	target.description = source.description
	target.properties = source.properties

	return target

def business_object(target, source):
	target.name = source.name
	target.identifier = source.identifier
	target.description = source.description
	target.attributes = source.attributes
	target.properties = source.properties

	return target

def usecase(target, source):
	refs = source.refs

	items = []

	# reuse structure in order not to fix all references

	for step in source.scenario.items:
		if refs.has_key(step):
			items.append(refs[step])

			del refs[step]
		else:
			items.append(format.model.Step())

#	print source.scenario.items
#	print target.scenario.items
	print items


	target.scenario.items = items

	# copy content
	clone.usecase_content(target, source, None)

	target.setParent()

	print target.scenario.items

	return target
