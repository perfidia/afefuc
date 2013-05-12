'''
Created on May 9, 2013

@author: Bartosz Alchimowicz
'''

import copy

import format.model

def items(items, source, target, project):
	retval = []

	for item in items:
		if isinstance(item, format.model.TextItem):
			retval.append(copy.copy(item))
		elif isinstance(item, format.model.Reference):
			if item.item == source:
				retval.append(target.get_ref())
			else:
				retval.append(item.item.get_ref())
		else:
			print type(item)
			assert 2 == 3

	return retval

def priority(source, project):
	target = format.model.Priority()

	target.name = source.name

	return target

def goal_level(source, project):
	target = format.model.GoalLevel()

	target.name = source.name

	return target

def actor(source, project):
	target = format.model.Actor()

	target.name = source.name
	target.identifier = source.identifier
	target.type = source.type
	target.description = items(source.description, source, target, project)
	target.properties = copy.deepcopy(source.properties)

	return target

def attribute(source, project):
	target = format.model.Attribute()

	target.name = source.name
	target.type = source.type
	target.description = items(source.description, source, target, project)

	return target

def business_rule(source, project):
	target = format.model.BusinessRule()

	target.identifier = source.identifier
	target.description = items(source.description, source, target, project)
	target.type = source.type
	target.dynamism = source.dynamism
	target.source = items(source.source, source, target, project)

	return target

def business_object(source, project):
	target = format.model.BusinessObject()

	target.name = items(source.name, source, target, project)
	target.identifier = source.identifier
	target.description = items(source.description, source, target, project)
	target.attributes = [attribute(a, project) for a in source.attributes]
	target.properties = copy.deepcopy(source.properties)

	return target

def use_case(source, project):
	def items(items, source, target, project):
		assert isinstance(items, list)

		retval = []

		for item in items:
			if isinstance(item, format.model.TextItem):
				retval.append(copy.copy(item))
			elif isinstance(item, format.model.Reference):
				if type(item.item) in [format.model.BusinessObject, format.model.Actor]:
					retval.append(item.item.get_ref())
				else:
					assert 1 == 2
			elif isinstance(item, format.model.EoUCCommand):
				retval.append(format.model.EoUCCommand())
			elif isinstance(item, format.model.GoToCommand):
				if isinstance(item.item, format.model.UseCase):
					if item.item == source:
						retval.append(format.model.GoToCommand(target))
					else:
						assert 0 == 2
				elif isinstance(item.item, format.model.Step):
					if isinstance(item.item.parent, format.model.UseCase):
						if item.item.parent == source:
							i, j = item.item.getPath()
							retval.append(format.model.GoToCommand(target.scenario.items[j]))
						else:
							retval.append(format.model.GoToCommand(item.item))
					elif isinstance(item.item.parent, format.model.Event):
						if item.item.parent.parent.parent == source:
							i, j, k, l = item.item.getPath()

							retval.append(
									format.model.GoToCommand(
											target.scenario.items[j].events[k].scenario.items[l]
									)
							)
						else:
							assert 1 == 4
					else:
						print type(item.item.parent)
						assert 7 ==1
				else:
					print type(item.item)
					assert 7 == 2
			else:
				print type(item)
				assert 2 == 3

		return retval

	def structure(source, target):
		for s in source.scenario.items:
			step = format.model.Step()

			for e in s.events:
				if isinstance(e, format.model.AlternationEvent):
					event = format.model.AlternationEvent()
				elif isinstance(e, format.model.ExtensionEvent):
					event = format.model.ExtensionEvent()
				elif isinstance(e, format.model.ExceptionEvent):
					event = format.model.ExceptionEvent()
				else:
					event = format.model.AlternationEvent() # TODO: to remove

				for ss in e.scenario.items:
					event.scenario.items.append(format.model.Step())

				step.events.append(event)

			target.scenario.items.append(step)

	def content(source, target, project):
		target.identifier = source.identifier
		target.goal_level = source.goal_level.item.get_ref()
		target.priority = source.priority.item.get_ref()
		target.main_actors = [r.item.get_ref() for r in source.main_actors]
		target.other_actors = [r.item.get_ref() for r in source.other_actors]

		target.title = items(source.title, source, target, project)

		# scenario
		for step_id, step_co in enumerate(source.scenario.items):
			target.scenario.items[step_id].items = items(step_co.items, source, target, project)

			for event_id, event_co in enumerate(step_co.events):
				target.scenario.items[step_id].events[event_id].title =\
						items(event_co.title, source, target, project)

				for substep_id, substep_co in enumerate(event_co.scenario.items):
					target.scenario.items[step_id].events[event_id].scenario.items[substep_id].items = \
							items(substep_co.items, source, target, project)

		# self.triggers = copy.deepcopy(instance.triggers)
		# self.preconditions = copy.deepcopy(instance.preconditions)
		# self.postconditions = copy.deepcopy(instance.postconditions)

		#self.testcases = copy.deepcopy(instance.testcases)

	target = format.model.UseCase()

	structure(source, target)
	content(source, target, project)

	return target

def test_case(source, project):
	target = format.model.TestCase()

	return target
