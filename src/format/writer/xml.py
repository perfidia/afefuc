'''
Created on Dec 24, 2012

@author: perf
'''

import StringIO
from types import MethodType
from lxml import etree as ET

from format import model as orginal
from utils.utils import Dict2XML
from utils import converter

def GoalLevel_att_to_xml(self, parent):
	goal_level = ET.SubElement(parent, "goal-level")
	goal_level.text = self.name

	if self.referenced == True:
		goal_level.set("id", str(id(self)))

	return goal_level

def Priority_att_to_xml(self, parent):
	priority = ET.SubElement(parent, "priority")
	priority.text = self.name

	if self.referenced == True:
		priority.set("id", str(id(self)))

	return priority

def Project_att_to_xml(self, parent = None):
	if parent:
		node = ET.SubElement(parent, "project")
	else:
		node = ET.Element("project")

	node.set("format", "1")

	name = ET.SubElement(node, "name")
	name.text = self.name

	version = ET.SubElement(node, "version")
	version.text = self.version

	language = ET.SubElement(node, "language")
	language.text = self.language

	actors = ET.SubElement(node, "actors")

	for a in self.actors:
		a.to_xml(actors)

	business_objects = ET.SubElement(node, "business-objects")

	for bo in self.business_objects:
		bo.to_xml(business_objects)

	business_rules = ET.SubElement(node, "business-rules")

	for br in self.business_rules:
		br.to_xml(business_rules)

	self.ucspec.to_xml(node)

	testcases = ET.SubElement(node, "testcases")

	for u in self.ucspec.usecases:
		if u.testcases:
			u.testcases.to_xml(testcases, u)

	tree = ET.ElementTree(node)
	output = StringIO.StringIO()
	tree.write(output, pretty_print = True, encoding = "UTF-8")

	retval = output.getvalue()

	return retval

def UCSpec_att_to_xml(self, parent):
	node = ET.SubElement(parent, "ucspec")

	priorities = ET.SubElement(node, "priorities")

	for p in self.priorities:
		p.to_xml(priorities)

	goal_levels = ET.SubElement(node, "goal-levels")

	for g in self.goal_levels:
		g.to_xml(goal_levels)

	usecases = ET.SubElement(node, "usecases")

	for u in self.usecases:
		u.to_xml(usecases)

	return node

def UseCase_att_to_xml(self, parent):
	usecase = ET.SubElement(parent, "usecase")

	if self.referenced == True:
		usecase.set("id", str(id(self)))

	identifier = ET.SubElement(usecase, "id")
	identifier.text = self.identifier

	title = ET.SubElement(usecase, "title")
	for a in self.title:
		a.to_xml(title)

	#goal_level = ET.SubElement(usecase, "goal-level")
	if self.goal_level:
		self.goal_level.to_xml(usecase)

	#priority = ET.SubElement(usecase, "priority")
	if self.priority:
		self.priority.to_xml(usecase)

	main_actors = ET.SubElement(usecase, "main-actors")
	for a in self.main_actors:
		a.to_xml(main_actors)

	other_actors = ET.SubElement(usecase, "other-actors")
	for a in self.other_actors:
		a.to_xml(other_actors)

#	triggers = ET.SubElement(usecase, "triggers")
#	for t in self.triggers:
#		t.to_xml(triggers)
#
#	preconditions = ET.SubElement(usecase, "pre-conditions")
#	for t in self.preconditions:
#		t.to_xml(preconditions)
#
#	postconditions = ET.SubElement(usecase, "post-conditions")
#	for t in self.postconditions:
#		t.to_xml(postconditions)

	scenario = self.scenario.to_xml(usecase)

	events = ET.SubElement(usecase, "events")
	for item in self.scenario.items:
		if isinstance(item, orginal.Step):
			if len(item.events) > 0:
				for event in item.events:
					event.to_xml(events, item)

	return usecase

def Scenario_att_to_xml(self, parent):
	scenario = ET.SubElement(parent, "scenario")

	for s in self.items:
		s.to_xml(scenario)

	return scenario

def Step_att_to_xml(self, parent):
	step = ET.SubElement(parent, "step")

	self.get_ref()

	if self.referenced == True:
		step.set("id", str(id(self)))

	#if self.scenario == None:
	for i in self.items:
		i.to_xml(step)
	#else:
	#	scenario = self.scenario.to_xml()

	return step

def Reference_att_to_xml(self, parent):
	tmp = {
		orginal.Actor: "actor",
		orginal.BusinessObject: "business-object",
		orginal.GoalLevel: "goal-level",
		orginal.Priority: "priority",
		orginal.Step: "step",
	}.get(type(self.item))

	assert tmp is not None

	ref = ET.SubElement(parent, tmp)
	ref.set("ref", str(id(self.item)))

	if self.properties:
		properties = ET.SubElement(ref, "properties")

		Dict2XML(self.properties, properties)

	debug = True

	if debug:
		# TODO: refactor
		if isinstance(self.item, orginal.Actor):
			tmp = self.item.name
		elif isinstance(self.item, orginal.BusinessObject):
			tmp = converter.itemsToText(self.item.name)
		elif isinstance(self.item, orginal.GoalLevel):
			tmp = self.item.name
		elif isinstance(self.item, orginal.Priority):
			tmp = self.item.name
		elif isinstance(self.item, orginal.Step):
			tmp = converter.itemsToText(self.item.items)
		else:
			print type(self.item)
			assert 1 == 2

		ref.set("tmp", tmp)

	return ref

def TextItem_att_to_xml(self, parent):
	text = ET.SubElement(parent, "text")
	text.text = self.text

def Event_att_to_xml(self, parent, step):
	event = ET.SubElement(parent, "event")

	event.set("type", self.event_type)
	event.set("id", str(id(self)))
	event.set("step", str(id(step)))

	title = ET.SubElement(event, "title")

	for s in self.title:
		s.to_xml(title)

	self.scenario.to_xml(event)

	return event

def Actor_att_to_xml(self, parent):
	actor = ET.SubElement(parent, "actor")

	if self.referenced == True:
		actor.set("id", str(id(self)))

	identifier = ET.SubElement(actor, "id")
	identifier.text = self.identifier

	name = ET.SubElement(actor, "name")
	name.text = self.name

	name = ET.SubElement(actor, "type")
	name.text = self.type

	description = ET.SubElement(actor, "description")

	for u in self.description:
		u.to_xml(description)

	if self.properties:
		properties = ET.SubElement(actor, "properties")
		Dict2XML(self.properties, properties)

	return actor

def GoToCommand_att_to_xml(self, parent):
	goto = ET.SubElement(parent, "goto")

	goto.set("ref", str(id(self.item)))

	return goto

def EoUCCommand_att_to_xml(self, parent):
	node = ET.SubElement(parent, "eouc")

	return node

def BusinesObject_att_to_xml(self, parent):
	node = ET.SubElement(parent, "business-object")

	if self.referenced == True:
		node.set("id", str(id(self)))

	name = ET.SubElement(node, "name")
	for u in self.name:
		u.to_xml(name)

	identifier = ET.SubElement(node, "id")
	identifier.text = self.identifier

	description = ET.SubElement(node, "description")

	for u in self.description:
		u.to_xml(description)

	attributes = ET.SubElement(node, "attributes")

	for u in self.attributes:
		u.to_xml(attributes)

	return node

def Attribute_att_to_xml(self, parent):
	node = ET.SubElement(parent, "attribute")

	name = ET.SubElement(node, "name")
	name.text = self.name

	type = ET.SubElement(node, "type")
	type.text = self.type

	description = ET.SubElement(node, "description")

	for u in self.description:
		u.to_xml(description)

	return node

def BusinesRule_att_to_xml(self, parent):
	node = ET.SubElement(parent, "business-rule")

	identifier = ET.SubElement(node, "id")
	identifier.text = self.identifier

	description = ET.SubElement(node, "description")
	for u in self.description:
		u.to_xml(description)

	return node

def Condition_att_to_xml(self, parent):
	node = ET.SubElement(parent, self.condition_type)

	for i in self.items:
		i.to_xml(node)

	return node

def TestCases_att_to_xml(self, parent, usecase):
	node = ET.SubElement(parent, 'usecase')
	node.set("ref", str(id(usecase)))

	#node = ET.SubElement(node, 'paths')

	for tc in self.tests:
		tc.to_xml(node)

	return node

def TestCase_att_to_xml(self, parent):
	node = ET.SubElement(parent, 'testcase')

	node = ET.SubElement(node, 'path')

	for s in self.path:
		ref = s.get_ref()
		ref.to_xml(node)

	return node

attachments = {
	orginal.Project:        Project_att_to_xml,
	orginal.GoalLevel:      GoalLevel_att_to_xml,
	orginal.Priority:       Priority_att_to_xml,
	orginal.UCSpec:         UCSpec_att_to_xml,
	orginal.UseCase:        UseCase_att_to_xml,
	orginal.Scenario:       Scenario_att_to_xml,
	orginal.Step:           Step_att_to_xml,
	orginal.Reference:      Reference_att_to_xml,
	orginal.TextItem:       TextItem_att_to_xml,
	orginal.Event:          Event_att_to_xml,
	orginal.Actor:          Actor_att_to_xml,
	orginal.GoToCommand:    GoToCommand_att_to_xml,
	orginal.EoUCCommand:    EoUCCommand_att_to_xml,
	orginal.BusinessObject: BusinesObject_att_to_xml,
	orginal.Attribute: 		Attribute_att_to_xml,
	orginal.BusinessRule:   BusinesRule_att_to_xml,
	orginal.Trigger:        Condition_att_to_xml,
	orginal.PreCondition:   Condition_att_to_xml,
	orginal.PostCondition:  Condition_att_to_xml,
	orginal.TestCases:      TestCases_att_to_xml,
	orginal.TestCase:       TestCase_att_to_xml,
}

def attach():
	for clazz in attachments:
		method = attachments[clazz]
		clazz.to_xml = MethodType(method, None, clazz)

def detach():
	for clazz in attachments:
		del clazz.to_xml
