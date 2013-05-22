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
	target.title = source.title
	target.identifier = source.identifier
	target.main_actors = source.main_actors
	target.other_actors = source.other_actors
	target.goal_level = source.goal_level
	target.priority = source.priority
	target.triggers = source.triggers
	target.preconditions = source.preconditions
	target.postconditions = source.postconditions
	target.scenario = source.scenario
	target.testcases = source.testcases
	target.summary = source.summary
	target.remarks = source.remarks

	return target
