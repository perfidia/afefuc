'''
Created on May 9, 2013

@author: Bartosz Alchimowicz
'''

from lxml import etree
from StringIO import StringIO
from format import model

def read(filename = None):
	ref = {}
	fix = []

	def add_ref(id, item):
		if not ref.has_key(id):
			ref[id] = item

		return item

	def get_ref(id, obj):
		retval = obj()

		if ref.has_key(id):
			retval.item = ref[id]

			return retval

		retval.item = id
		fix.append(retval)

		return retval

	def fix_ref():
		for i in fix:
			i.item = ref[i.item]

	def text(project, node):
		retval = model.TextItem(node.text)

		return retval

	def items(project, node):
		retval = []

		for n in node.getchildren():
			if n.tag == 'text':
				retval.append(text(project, n))
			elif n.tag == 'text':
				retval.append(text(project, n))
			elif n.tag == 'business-object':
				retval.append(business_object(project, n))
			elif n.tag == 'actor':
				retval.append(actor(project, n))
			elif n.tag == 'eouc':
				retval.append(model.EoUCCommand())
			elif n.tag == 'goto':
				retval.append(get_ref(n.attrib['ref'], model.GoToCommand))
			else:
				print n.tag
				assert 1 == 2

		return retval

	def actor(project, node):
		if node.attrib.has_key('ref'):
			return get_ref(node.attrib['ref'], model.Reference)

		retval = model.Actor()

		add_ref(node.attrib['id'], retval)

		for n in node.getchildren():
			if n.tag == 'name':
				retval.name = n.text
			elif n.tag == 'id':
				retval.identifier = n.text
			elif n.tag == 'type':
				retval.type = n.text
			elif n.tag == 'description':
				retval.description = items(project, n)
			elif n.tag == 'properties':
				pass
			else:
				print n.tag
				raise ValueError("Unsupported format file")

		return retval

	def usecase(project, node):
		retval = model.UseCase()

		add_ref(node.attrib['id'], retval)

		for n in node.getchildren():
			if n.tag == 'title':
				retval.title = items(project, n)
			elif n.tag == 'id':
				retval.identifier = n.text
			elif n.tag == 'main-actors':
				retval.main_actors = generic_list_iterator(retval, n, actor)
			elif n.tag == 'other-actors':
				retval.other_actors = generic_list_iterator(retval, n, actor)
			elif n.tag == 'goal-level':
				retval.goal_level = goal_level(project, n)
			elif n.tag == 'priority':
				retval.priority = priority(project, n)
			elif n.tag == 'triggers':
				pass
			elif n.tag == 'preconditions':
				pass
			elif n.tag == 'postconditions':
				pass
			elif n.tag == 'scenario':
				retval.scenario = scenario(project, n)
			elif n.tag == 'testcases':
				pass
			elif n.tag == 'events':
				generic_list_iterator(retval, n, event)
				# ignore returned value
			else:
				print n.tag
				raise ValueError("Unsupported format file")

		return retval

	def attribute(project, node):
		retval = model.Attribute()

		for n in node.getchildren():
			if n.tag == 'name':
				retval.name = n.text
			elif n.tag == 'type':
				retval.type = n.text
			elif n.tag == 'description':
				retval.description = items(project, n)
			else:
				print n.tag
				raise ValueError("Unsupported format file")

		return retval

	def business_object(project, node):
		if node.attrib.has_key('ref'):
			return get_ref(node.attrib['ref'], model.Reference)

		retval = model.BusinessObject()

		add_ref(node.attrib['id'], retval)

		for n in node.getchildren():
			if n.tag == 'name':
				retval.name = items(project, n)
			elif n.tag == 'id':
				retval.identifier = n.text
			elif n.tag == 'description':
				retval.description = items(project, n)
			elif n.tag == 'attributes':
				retval.attributes = generic_list_iterator(retval, n, attribute)
			elif n.tag == 'properties':
				pass
			else:
				print n.tag
				raise ValueError("Unsupported format file")

		return retval

	def business_rule(project, node):
		if node.attrib.has_key('ref'):
			return get_ref(node.attrib['ref'], model.Reference)

		retval = model.BusinessRule()

		add_ref(node.attrib['id'], retval)

		for n in node.getchildren():
			if n.tag == 'id':
				retval.identifier = n.text
			elif n.tag == 'description':
				retval.description = items(project, n)
			elif n.tag == 'type':
				retval.type = n.text
			elif n.tag == 'dynamism':
				retval.dynamism = n.text
			elif n.tag == 'source':
				retval.source = retval.source = items(project, n)
			else:
				print n.tag
				raise ValueError("Unsupported format file")

		return retval

	def priority(project, node):
		if node.attrib.has_key('ref'):
			return get_ref(node.attrib['ref'], model.Reference)

		retval = model.Priority(node.text)

		add_ref(node.attrib['id'], retval)

		return retval

	def goal_level(project, node):
		if node.attrib.has_key('ref'):
			return get_ref(node.attrib['ref'], model.Reference)

		retval = model.GoalLevel(node.text)

		add_ref(node.attrib['id'], retval)

		return retval

	def event(project, node):
		if node.attrib.has_key('ref'):
			return get_ref(node.attrib['ref'], model.Reference)

		retval = {
			model.EventType.ALTERNATION: model.AlternationEvent,
			model.EventType.EXTENSION:   model.ExtensionEvent,
			model.EventType.EXCEPTION:   model.ExceptionEvent
		}.get(node.attrib['type'])()

		for n in node.getchildren():
			if n.tag == 'title':
				retval.title = items(project, n)
			elif n.tag == 'scenario':
				retval.scenario = scenario(project, n)
			else:
				print n.tag
				raise ValueError("Unsupported format file")

		add_ref(node.attrib['id'], retval)

		step = get_ref(node.attrib['step'], model.Reference).item

		step.events.append(retval)

		# NO RETURN

	def step(project, node):
		if node.attrib.has_key('ref'):
			return get_ref(node.attrib['ref'], model.Reference)

		retval = model.Step()

		add_ref(node.attrib['id'], retval)

		retval.items = items(project, node)

		return retval

	def scenario(project, node):
		retval = model.Scenario()

		for n in node.getchildren():
			retval.items.append(step(project, n)) ################ items!!

		return retval

	def generic_list_iterator(project, node, func):
		retval = []

		for n in node.getchildren():
			retval.append(func(project, n))

		return retval

	def ucspec(project, node):
		retval = model.UCSpec()

		for n in node.getchildren():
			if n.tag == 'priorities':
				retval.priorities = generic_list_iterator(retval, n, priority)
			elif n.tag == 'goal-levels':
				retval.goal_levels = generic_list_iterator(retval, n, goal_level)
			elif n.tag == 'usecases':
				retval.usecases = generic_list_iterator(retval, n, usecase)
			else:
				print n.tag
				assert 1 == 2

		return retval

	def project(node):
		if node.tag != 'project':
			raise ValueError('Tag screen-spec not found')

		retval = model.Project()

		if node.attrib['format'] != "1":
			raise ValueError("Unsupported format file")

		for n in node.getchildren():
			if n.tag == 'name':
				retval.name = n.text
			elif n.tag == 'version':
				retval.version = n.text
			elif n.tag == 'language':
				retval.language = n.text
			elif n.tag == 'actors':
				retval.actors = generic_list_iterator(retval, n, actor)
			elif n.tag == 'business-objects':
				retval.business_objects = generic_list_iterator(retval, n, business_object)
			elif n.tag == 'business-rules':
				retval.business_rules = generic_list_iterator(retval, n, business_rule)
			elif n.tag == 'ucspec':
				retval.ucspec = ucspec(retval, n)
			elif n.tag == 'testcases':
				pass
			else:
				print n.tag
				raise ValueError("Unsupported format file")

		return retval

	assert filename is not None

	fd = open(filename)
	data = fd.read()
	fd.close()

	root = etree.fromstring(data)

	retval = project(root)
	retval.setParents()

	fix_ref()

	return retval
