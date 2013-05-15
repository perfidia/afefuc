#! /usr/bin/env python
# -*- coding: utf-8 -*-

from xml.dom import minidom
from os import path
import re

import sentenceElement


class sentenceBuilder(object):

    def __init__(self, fileName):
        
        if path.isfile(fileName):
            DOMTree = minidom.parse(fileName)
            cNodes = DOMTree.childNodes

            self.xml = None

            for element in cNodes:
                if element.nodeType == 1 and element.tagName == 'start':
                    self.xml = sentenceElement.sentenceElement(element)
            if self.xml is None:
                raise Exception('No START element found in input file.')
        else:
            raise Exception('Input file doesn\'t exist')

    def getStructure(self):
        return self.xml

    def findWordAtBeginning(self, element, toCheck):
        actor = '^[A-Z][a-z]+'
        value = '^[\"].*'
        url = '^[\"].*' #znaleźć lepszy sposób na walidację url'a
        name = '^[\"].*'
        number = '^[0-9]+'

        if len(toCheck.strip(' ')) == 0:
            return False
        elif element.getElementClass() == 'actor' and re.match(actor, toCheck):  
            return True
        elif element.getElementClass() == 'value' and re.match(value, toCheck):  
            return True
        elif element.getElementClass() == 'url' and re.match(url, toCheck):  
            return True
        elif element.getElementClass() == 'name' and re.match(name, toCheck): 
            return True
        else:  
            return re.compile(r'^({0}).+'.format(toCheck), flags=re.IGNORECASE).search(element.getValue())

    def compareWords(self, element, toCheck):
        actor = '^[A-Z][a-z]+'
        value = '^[\"].*[\"]$'
        url = '^[\"].*[\"]$' #znaleźć lepszy sposób na walidację url'a
        name = '^[\"].*[\"]$'
        number = '^[0-9]+'

        if element.getValue() == toCheck:
            return True
        elif element.getValue() == '[actor]' and re.match(actor, toCheck):  
            return True
        elif element.getValue() == '[value]' and re.match(value, toCheck):  
            return True
        elif element.getValue() == '[url]' and re.match(url, toCheck):  
            return True
        elif element.getValue() == '[name]' and re.match(name, toCheck): 
            return True
        elif element.getValue() == '[number]' and re.match(number, toCheck): 
            return True
        else:  
            return False

    def getNext(self, sentence):
        wordsList = str(sentence).strip(' .').split(' ')
        output = [0, [], '']
        if wordsList[0] != '':
            for element in self.xml.getNestedElements():
                self.recCheck(element, wordsList, output, 0)
        else:
            for element in self.xml.getNestedElements():
                output[1].insert(len(output[1]), element)
        self.verifyResults(wordsList, output)
        output[2] = self.colorUp(wordsList, output[0])
        return output

    def recCheck(self, element, inputWords, output, depth):
        if depth >= len(inputWords):
            return
        if self.compareWords(element, inputWords[depth]):
            if output[0] < depth + 1:
                output[0] = depth + 1
                del output[1][:]
                for subElement in element.getNestedElements():
                    output[1].insert(len(output[1]), subElement)
            for subElement in element.getNestedElements():
                self.recCheck(subElement, inputWords, output, depth + 1)
        return output

    def verifyResults(self, wordsList, results):
        if results[0] < len(wordsList)-1:
            del results[1][:]
        elif results[0] == len(wordsList)-1 and wordsList[len(wordsList)-1].strip(' ') != '':
            tmpResult = []
            for element in results[1]:
                if self.findWordAtBeginning(element, wordsList[results[0]]):
                    if self.checkIfNotExists(element, tmpResult):
                        tmpResult.insert(len(tmpResult), element)
            if len(wordsList) > 0:
                del results[1][:]
                results.insert(1, tmpResult)
        else:
            tmpResult = []
            for element in results[1]:
                if self.checkIfNotExists(element, tmpResult):
                    tmpResult.insert(len(tmpResult), element)
            del results[1][:]
            results.insert(1, tmpResult)

    def checkIfNotExists(self, element, touple):
        for e in touple:
            if element.getValue() == e.getValue():
                return False
        return True

    #pobranie typów obiektów
    def getTypesStructure(self):
        pass

    def colorUp(self, wordsList, depth):
        output = ''
        if depth > 0:
            result = []
            for e in wordsList[:depth]:
                result.append(e)
                result.append(' ')
            output += '<font color="green">' + ' '.join(result) + '</font>'
        if depth < len(wordsList):
            output += '<font color="red">' + ' '.join(wordsList[depth:]) + '</font>'
        return output
