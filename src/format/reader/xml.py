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
				retval.main_actors = actors(project, n)
			elif n.tag == 'other-actors':
				retval.other_actors = actors(project, n)
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
				events(project, n)
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
				retval.attributes = attributes(project, n)
			elif n.tag == 'properties':
				pass
			else:
				print n.tag
				raise ValueError("Unsupported format file")

		return retval

	def attributes(project, node):
		retval = []

		for n in node.getchildren():
			retval.append(attribute(project, n))

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

		retval = model.Event()

		add_ref(node.attrib['id'], retval)

		for n in node.getchildren():
			if n.tag == 'title':
				retval.title = items(project, n)
			elif n.tag == 'event-type':
				retval.event_type = n.text
			elif n.tag == 'scenario':
				retval.scenario = scenario(project, n)
			else:
				print n.tag
				raise ValueError("Unsupported format file")

		step = get_ref(node.attrib['step'], model.Reference).item

		step.events.append(retval)

		# NO RETURN

	def events(project, node):
		for n in node.getchildren():
			event(project, n)

		# NO RETURN

	def priorities(project, node):
		retval = []

		for n in node.getchildren():
			retval.append(priority(project, n))

		return retval

	def goal_levels(project, node):
		retval = []

		for n in node.getchildren():
			retval.append(goal_level(project, n))

		return retval

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

	def actors(project, node):
		retval = []

		for n in node.getchildren():
			retval.append(actor(project, n))

		return retval

	def usecases(project, node):
		retval = []

		for n in node.getchildren():
			retval.append(usecase(project, n))

		return retval

	def business_objects(project, node):
		retval = []

		for n in node.getchildren():
			retval.append(business_object(project, n))

		return retval

	def ucspec(project, node):
		retval = model.UCSpec()

		for n in node.getchildren():
			if n.tag == 'priorities':
				retval.priorities = priorities(project, n)
			elif n.tag == 'goal-levels':
				retval.goal_levels = goal_levels(project, n)
			elif n.tag == 'usecases':
				retval.usecases = usecases(project, n)
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
				retval.actors = actors(retval, n)
			elif n.tag == 'business-objects':
				retval.business_objects = business_objects(retval, n)
			elif n.tag == 'business-rules':
				pass
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
