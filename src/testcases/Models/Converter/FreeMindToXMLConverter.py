#! /usr/bin/env python
# -*- coding: utf-8 -*-

from os import path
from sys import argv, exit
from xml.dom import minidom
from xmlElement import xmlElement

if len(argv) == 3:
    inputFileName = argv[1]
    outputFileName = argv[2]
else:
    raise Exception('Wrong arguments. Try: ./XMLConverter.py [input file] [output file]')

if path.isfile(inputFileName):
    DOMTree = minidom.parse(inputFileName)
    cNodes = DOMTree.childNodes[0].childNodes

    xml = None;

    for element in cNodes:
        if element.nodeType == 1 and element.tagName == 'node' and element.getAttribute('TEXT') == '[start]':
            xml = xmlElement(element)
    if xml == None:
        raise Exception('No START element found in input file.')

    output = xml.toXML()

    try:
        outputFile = open(outputFileName, 'w')
        outputFile.write(output)
        outputFile.close()
    except IOError as e:
        raise Exception('I/O error({0}): {1}'.format(e.errno, e.strerror))
else:
    raise Exception('Input file doesn\'t exist')

