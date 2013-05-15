#! /usr/bin/env python
# -*- coding: utf-8 -*-

from xml.dom import minidom

class xmlElement(object):

    def __init__(self, element):
        
        self.nestedObjects = []
        self.value = None;
        self.elementClass = None;
        self.action = None;
        self.objectType = None;

        if element.attributes and element.tagName == 'node':
            
            for i in range(element.attributes.length):
                if element.attributes.item(i).name == 'TEXT':
                    self.value = element.attributes.item(i).value

            if self.value == None:
                raise Exception('There is an error in your input file - no TEXT attribute for element named NODE specified.')

            for subElement in element.childNodes:
                if subElement.nodeType == 1 and subElement.tagName == 'attribute' and subElement.attributes:
                    name = None;
                    value = None;

                    for i in range(subElement.attributes.length):
                        if subElement.attributes.item(i).name == 'NAME':
                            name = subElement.attributes.item(i).value
                        elif subElement.attributes.item(i).name == 'VALUE':
                            value = subElement.attributes.item(i).value
                            if name == 'class':
                                self.elementClass = value
                            elif name == 'action':
                                self.action = value
                            elif name == 'type':
                                self.objectType = value
                            else:
                                raise Exception('There is an error in your input file - no NAME attribute for element named ATTRIBUTE specified.')
                    if value == None:
                        raise Exception('There is an error in your input file - no VALUE attribute for element named ATTRIBUTE specified.')
                    name = None;
                    value = None;

                if subElement.nodeType == 1 and subElement.tagName == 'node' and subElement.attributes:
                    self.nestedObjects.append(xmlElement(subElement))

    def getNestedElementsNumber(self):
        return len(self.nestedObjects)

    def getNestedElements(self):
        return self.nestedObjects

    def getValue(self):
        return self.value

    def getElementClass(self):
        return self.elementClass

    def getAction(self):
        return self.action

    def getObjectType(self):
        return self.objectType

    def toXML(self, intendation = 0):
        output = ''
        if self.elementClass != None:
            output = ' '*intendation + '<' + self.elementClass 
            if self.action != None:
                output += ' action="' + self.action + '"'
            if self.objectType != None:
                output += ' type="' + self.objectType + '"'
            if self.value != None:
                output += '>' + self.value
            if len(self.nestedObjects) > 0:
                for nestedElement in self.nestedObjects:
                    output += '\n' + nestedElement.toXML(intendation+1)
                output += '\n' + ' '*intendation + '</' + self.elementClass + '>'
            else:
                output += '</' + self.elementClass + '>'
        return output
