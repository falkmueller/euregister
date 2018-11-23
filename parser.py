#!/usr/bin/env python

#from xml.dom import minidom

#xml_file = "full_export_new.xml"
#xmldoc = minidom.parse(xml_file)
##resultList><interestRepresentative
##itemlist = xmldoc.getElementsByTagName('item') 
#print(len(xmldoc.childNodes[0].childNodes[1].childNodes))

import csv
import json
import re
import sys

def import_csv():   
    header = []

    with open('data/source/full_export_new.csv', 'rb') as csvfile:
        csvReader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in csvReader:
            if len(header) == 0:
                for col in row:
                    header.append(re.sub("[^a-z0-9]","_", col.lower().replace(":", "")).replace("__", "_").strip("_"))
                #header = row
                print ', '.join(header)
                continue;

            entity = {}

            for i in range(0, len(header) - 1):
                entity[header[i]] = row[i]

            #print ', '.join(row)
            #print entity
            print entity["identification_number"]

            with open('data/json/' + entity["identification_number"]  + '.json', 'w') as fp:
                json.dump(entity, fp)
            #break;

# CMD Command ##################################################################
if len(sys.argv) > 1:
    if sys.argv[1] == "import":
        import_csv();
    else:
        print "unknown function name";
else:
        print "first argument must function name";
        