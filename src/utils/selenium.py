#! /usr/bin/env python
#-*- coding: utf-8 -*-

'''
To install the Python client library:
	pip install -U selenium

We use unittest which is a part of Python STD library

To run generated tests simply type:
	fileName.py
'''

from os import path
import codecs

class selenium:

	def __init__(self, sb):
		self.sb = sb

	def generateCode(self, tc):
		fileName = tc.title
		actions = tc.path
		outputPath = './' + fileName + '.py'

		if path.isfile(outputPath):
			if path.exists(outputPath):
				raise Exception('File already exists!')
			else:
				try:
					outputFile = codecs.open(outputPath, 'w', 'utf-8')

					self.generateHeader(outputFile)
					self.generateActions(actions, outputFile, fileName)
					self.generateFooter(outputFile)

					outputFile.close()
				except IOError as e:
					raise Exception('I/O error({0}): {1}'.format(e.errno, e.strerror))

	def parseActions(self, sentence):
		action = ['', '', '']

		o = self.sb.getElements(sentence)
		for e in o:
			if e.getElementClass() == 'action':
				action[0] = e.getAction()
			elif e.getElementClass() in ['name', 'url']:
				action[1] = e.getValue()
			elif e.getElementClass() in ['value', 'number']:
				action[2] = e.getValue()

		return action

	def generateHeader(self, file, fileName):
		file.write('from selenium import webdriver\nimport unittest\nimport sys\n\n')
		file.write('class ' + fileName + '(unittest.TestCase):\n\n')
		file.write('\tdef setUp(self):\n\t\tself.driver = webdriver.Remote(desired_capabilities={"browserName": "firefox","platform": "LINUX"})\n\n')

	def generateFooter(self, file):
		file.write('\tdef tearDown(self):\n\t\tself.driver.quit()\n\nif __name__ == "__main__":\n\tunittest.main()')

	def generateActions(self, actions, file):
		file.write('\tdef test(self):\n')

		actionsBuffer = []

		for action in actions:
			output = self.sb.getElements(action.tcstep)

			actionsBuffer.insert(len(actionsBuffer), output)

			if output[0] == 'redo':
				if output[2] == '':
					raise Exception('Invalid number of parameters.')
				else:
					if output[2] < len(actionsBuffer)-1:
						output = actionsBuffer[output[2]]
					else:
						raise Exception('Invalid value of parameter.')	

			if output[0] == 'open':
				if output[1] == '':
					raise Exception('Invalid number of parameters.')
				else:
					file.write('\t\tdriver.get("' + output[1] + '")\n\n')
			elif output[0] == 'click':
				if output[1] == '':
					raise Exception('Invalid number of parameters.')
				else:
					file.write('\t\telement = driver.find_element_by_id("' + output[1] + '"")\n')
					file.write('\t\telement = driver.click()\n\n')
			elif output[0] == 'type':
				if output[1] == '' or output[2]:
					raise Exception('Invalid number of parameters.')
				else:
					file.write('\t\telement = driver.find_element_by_id("' + output[1] + '"")\n')
					file.write('\t\telement = driver.send_keys("' + output[2] + '")\n\n')
			elif output[0] == 'checkTextPresent':
				#pass
			elif output[0] == 'openWindow':
				if output[1] == '':
					raise Exception('Invalid number of parameters.')
				else:
					file.write('\t\tdriver.get("' + output[1] + '")\n\n')
			elif output[0] == 'checkPagePresent':
				#pass
			else:
				raise Exception('Invalid action.')


# allPageCode = driver.getPageSource()
# allPageCode.contains(" ")