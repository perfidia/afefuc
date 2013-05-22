This script converts .mm files (current format for FreeMind) to XML format
==========================================================================

How to use:
-----------

./mm2xml.py [input file] [output file] 

Output XML file structure:
--------------------------

+ main element -> [start]
++ children elements:
++ actor
++ text
++ action -> has attributes:
+++ action 
++ value 
++ name 
++ url 
++ object -> has attributes:
+++ type 
++ number

