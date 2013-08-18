#! /usr/bin/env python
#-*- coding: utf-8 -*-

'''
To install the Python client library:
	pip install -U selenium

We use unittest which is a part of Python STD library

To run generated tests simply type:
	fileName.py

To run tests you need Selenium RC - download from:
	http://docs.seleniumhq.org/download/
'''

from os import path
from os import remove
import re
import codecs

class selenium:

	def __init__(self, sb):
		self.sb = sb
		self.browser = None
		self.system = None

	def generateCode(self, tc, browser, system, directory):
		fileName = self.makeFileName(tc.title)
		actions = tc.path
		self.browser = browser.toLower()
		self.system = system.toUpper()
		outputDir = directory + '/'
		outputPath = outputDir + fileName + '.py'

		if path.isdir(outputDir):
			if path.exists(outputPath):
				raise Exception('File already exists!')
			else:
				try:
					outputFile = codecs.open(outputPath, 'w', 'utf-8')

					self.generateHeader(outputFile, fileName)
					self.generateActions(actions, outputFile)
					self.generateFooter(outputFile)

					outputFile.close()
					print ' + ' + fileName
				except IOError as e:
					raise Exception('I/O error({0}): {1}'.format(e.errno, e.strerror))
				except Exception as e:
					print ' - Unexpected error occured in TC: ' + tc.title
					print ' - Error message: ' + e.message
					remove(outputPath)
		else:
			raise Exception('Wrong path, or file name')

	def makeFileName(self, input):
		dic = {'ś':'s', 'ć':'c', 'ą':'a', 'ę':'e', 'ż':'z', 'ź':'z', 'ó':'o', 'ł':'l', 'ń':'n'}
		
		for i in dic:
			i = i.decode('utf-8')
			input = input.replace(i, dic[i.encode('utf-8')])

		input = re.sub(ur'[^a-zA-Z0-9 ]+', '', input)
		words = input.title().split(' ')
		output = ''.join(words)
		return output

	def parseActions(self, sentence):
		action = ['', '', '']

		o = self.sb.getElements(sentence)
		for e in o:
			if e.getElementClass() == 'action':
				action[0] = e.getAction()
			elif e.getElementClass() in ['name', 'url']:
				if e.getElementClass() == 'url':
					if re.match(r'^http://', e.getParsedValue()) == None:
						url = e.getParsedValue()
						action[1] = '"http://' + url[1:]
					else:
						action[1] = e.getParsedValue()
				else:
					action[1] = e.getParsedValue()
			elif e.getElementClass() in ['value', 'number']:
				action[2] = e.getParsedValue()

		return action

	def generateHeader(self, file, fileName):
		file.write('#! /usr/bin/env python\n')
		file.write('#-*- coding: utf-8 -*-\n\n')

		file.write('from selenium import webdriver\nimport unittest\nimport sys\n\n')
		file.write('class ' + fileName + '(unittest.TestCase):\n\n')
		file.write('\tdef setUp(self):\n\t\tself.driver = webdriver.Remote(desired_capabilities={"browserName": "' + self.browser + '","platform": "' + self.system + '"})\n')
		file.write('\t\tself.driver.implicitly_wait(3)\n\n')

	def generateFooter(self, file):
		file.write('\tdef tearDown(self):\n\t\tself.driver.quit()\n\nif __name__ == "__main__":\n\tunittest.main()')

	def generateActions(self, actions, file):
		file.write('\tdef test(self):\n')

		actionsBuffer = []
		i = 0;

		for action in actions:

			output = None

			if action.tcstep and len(action.tcstep) > 0:
				output = self.parseActions(action.tcstep)
				actionsBuffer.insert(len(actionsBuffer), output)
				i = i + 1
			else:
				actionsBuffer.insert(len(actionsBuffer), output)
				continue

			if output[0] == 'redo':
				if output[2] == '':
					raise Exception('Invalid number of parameters for action: redo')
				else:
					if int(output[2]) < len(actionsBuffer)-1 and int(output[2]) > 0:
						output = actionsBuffer[int(output[2])-1]
					else:
						raise Exception('Invalid value of parameter for action: redo')	
			if output[0] == 'open':
				if output[1] == '':
					raise Exception('Invalid number of parameters for action: open')
				else:
					file.write('\t\tself.driver.get(' + output[1] + ')\n\n')
			elif output[0] == 'click':
				if output[1] == '':
					raise Exception('Invalid number of parameters for action: click')
				else:
					file.write('\t\telement = self.driver.find_element_by_id(' + output[1] + ')\n')
					file.write('\t\telement.click()\n\n')
			elif output[0] == 'type':
				if output[1] == '' or output[2] == '':
					raise Exception('Invalid number of parameters for action: type')
				else:
					file.write('\t\telement = self.driver.find_element_by_id(' + output[1] + ')\n')
					file.write('\t\telement.send_keys(' + output[2] + ')\n\n')
			elif output[0] == 'checkTextPresent':
				if output[2] == '':
					raise Exception('Invalid number of parameters for action: checkTextPresent')
				else:
					if output[1] == '':
						# all page
						file.write('\t\tallPageCode = self.driver.getPageSource()\n\n')
						file.write('\t\tself.assertTrue(allPageCode.contains(' + output[2] + '))\n\n')
					else:
						# specified element
						file.write('\t\telement = self.driver.find_element_by_id(' + output[2] + ').text\n\n')
						file.write('\t\tself.assertTrue(element.contains(' + output[2] + '))\n\n')
			elif output[0] == 'openWindow':
				if output[1] == '':
					raise Exception('Invalid number of parameters for action: openWindow')
				else:
					file.write('\t\tself.driver.get(' + output[1] + ')\n\n')
			elif output[0] == 'checkPagePresent':
				if output[1] == '':
					raise Exception('Invalid number of parameters for action: checkPagePresent')
				else:
					file.write('\t\tself.assertEqual(' + self.driver.current_url + ', ' + output[1] + ')\n\n')
			else:
				raise Exception('Invalid action.')

		if i == 0:
			file.write('\t\tpass\n\n')