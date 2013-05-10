'''
Created on May 9, 2013

@author: Bartosz Alchimowicz
'''

import copy

import format.model

def actor(target, source):
	target.name = source.name
	target.identifier = source.identifier
	target.type = source.type
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
