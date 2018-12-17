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
import os.path
from lib import searcher

from whoosh.fields import *

def import_csv(csv_file = u"data/source/full_export_new.csv", json_folder = u"data/json"):   
    
    if len(sys.argv) > 2:
        csv_file = sys.argv[2]

    if not os.path.isfile(csv_file):
        print "file " + csv_file + " not found";
        return;

    if len(sys.argv) > 3:
        json_folder = sys.argv[3]

    if not os.path.exists(json_folder) or os.path.isfile(json_folder):
        print "folder " + json_folder + " not found";
        return;
    
    header = []
    with open(csv_file, 'rb') as csvfile:
        csvReader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in csvReader:
            if len(header) == 0:
                for col in row:
                    header.append(re.sub("[^a-z0-9]","_", col.lower().replace(":", "")).replace("__", "_").strip("_"))
                #header = row
                #print ', '.join(header)
                continue;

            entity = {}

            for i in range(0, len(header) - 1):
                entity[header[i]] = row[i]

            #print ', '.join(row)
            #print entity
            print entity["identification_number"]

            with open(json_folder + '/' + entity["identification_number"]  + '.json', 'w') as fp:
                json.dump(entity, fp)
            #break;
            
def create_index(index_folder = u"data/index", json_folder = u"data/json"):

    if len(sys.argv) > 2:
        index_folder = sys.argv[2]

    if not os.path.exists(index_folder) or os.path.isfile(index_folder):
        print "folder " + index_folder + " not found";
        return;

    if len(sys.argv) > 3:
        json_folder = sys.argv[3];

    if not os.path.exists(json_folder) or os.path.isfile(json_folder):
        print "folder " + json_folder + " not found";
        return;

    ix = searcher.create_index(index_folder)
    writer = ix.writer()

    for filename in os.listdir(json_folder):
        if not filename.endswith(".json"):
            continue;

        with open(os.path.join(json_folder, filename)) as f:
            json_obj = json.load(f);

        print json_obj["identification_number"]

        writer.add_document(
            id=json_obj["identification_number"],
            fields_of_interest_s=json_obj["fields_of_interest"],
            head_office_country_s=json_obj["head_office_country"],
            registration_date_s=json_obj["registration_date"],
            website_address_s=json_obj["website_address"]
        )

    writer.commit(optimize=True)
        