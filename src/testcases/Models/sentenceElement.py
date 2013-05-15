#! /usr/bin/env python
# -*- coding: utf-8 -*-

from xml.dom import minidom


class sentenceElement(object):

    def __init__(self, element):
        
        self.nestedObjects = []
        self.value = None
        self.elementClass = None
        self.action = None
        self.objectType = None

        if element.nodeType == 1:
            
            self.elementClass = element.tagName
            
            if element.attributes:
            
                for i in range(element.attributes.length):
                    if element.attributes.item(i).name == 'action':
                        self.action = element.attributes.item(i).value
                    elif element.attributes.item(i).name == 'type':
                        self.objectType = element.attributes.item(i).value

            for subElement in element.childNodes:
                if subElement.nodeType == 3 and self.value is None:
                    self.value = subElement.nodeValue.strip()
                elif subElement.nodeType == 1:
                    self.nestedObjects.append(sentenceElement(subElement))

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
