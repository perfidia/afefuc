'''
Created on May 4, 2013

@author: Bartosz Alchimowicz
'''

import re

import format.model

def textToItems(project, text, replace = None):
	def itemFromText(project, text, replace = None):
		t = re.match(r"@(actor):(\w+)", text)

		if t:
			actor = project.getActorByIdentifier(t.groups()[1])

			return actor.get_ref()

		t = re.match(r"@(bo):(\w+)", text)

		if t:
			bo = project.getBusinessObjectByIdentifier(t.groups()[1])

			return bo.get_ref()

		t = re.match(r"@(eouc)", text)

		if t:
			return format.model.EoUCCommand()

		t = re.match(r"@(goto):((\w+.)*\w+)", text)

		if t:
			tmp = t.groups()[1].split(".")

			uc = project.getUseCaseByIdentifier(tmp[0], replace)

			if len(tmp) == 1:
				item = uc
			elif len(tmp) == 2:
				i = int(tmp[1]) - 1
				item = uc.scenario.items[i]
			elif len(tmp) == 3:
				i = int(tmp[1]) - 1
				j = ord(tmp[2]) - 65

				item = uc.scenario.items[i].events[j]
			elif len(tmp) == 4:
				i = int(tmp[1]) - 1
				j = ord(tmp[2]) - 65
				k = int(tmp[3]) - 1

				item = uc.scenario.items[i].events[j].scenario.items[k]
			else:
				raise ValueError()

			return format.model.GoToCommand(item)

		return format.model.TextItem(text)

	assert isinstance(project, format.model.Project)
	assert isinstance(text, basestring)

	tmp = text.split(" ")
	symbols = ".,"

	items = []
	items2 = []

	for i in tmp:
		if len(i) > 0:
			if i[0] in symbols:
				items.append(i[0])

				if len(i) > 1:
					items.append(i[1:])

				continue

			if i[-1] in symbols:
				items.append(i[:-1])

				if len(i) > 1:
					items.append(i[-1])

				continue

			items.append(i)

	for i in items:
		n = itemFromText(project, i, replace)

		if len(items2) > 0:
			if isinstance(n, format.model.TextItem) and isinstance(items2[-1], format.model.TextItem):
				if len(n.text) == 1 and n.text in symbols:
					items2[-1].text += n.text
				else:
					items2[-1].text += " " + n.text
			else:
				items2.append(n)
		else:
			items2.append(n)

	return items2

def itemsToText(items, edit = False):
	assert isinstance(items, list)

	retval = []
	lastIdx = len(items) - 1

	for i, item in enumerate(items):
		if isinstance(item, format.model.Item):
			retval.append(item.toText(edit))
		elif isinstance(item, format.model.Referencable):
			retval.append(item.toIdentifierText(edit))
		else:
			assert 1 == 2 and "unknown type"

		if i < lastIdx:
			if isinstance(items[i + 1], format.model.TextItem) and items[i + 1].text in ".,":
				pass
			else:
				retval.append(" ")

	return "".join(retval)
