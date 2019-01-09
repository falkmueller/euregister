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
import urllib
import requests
import time
import random

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
            
            if os.path.exists(json_folder + '/' + entity["identification_number"]  + '.json'):
                continue;

            with open(json_folder + '/' + entity["identification_number"]  + '.json', 'w') as fp:
                json.dump(entity, fp)
            #break;
                 
def add_geo_reference(json_folder = u"data/json"):
    i = 600;
    
    reference_exists = 0
    already_searched = 0
    
    for filename in os.listdir(json_folder):
        if not filename.endswith(".json"):
            continue;

        print filename;

        with open(os.path.join(json_folder, filename), 'r') as f:
            json_obj = json.load(f);

            
        
        #print json_obj["identification_number"]
        if json_obj.has_key("lat"):
            print "reference exists"
            reference_exists+=1;
            continue;
            
        if json_obj.has_key("no_geo_reference"):
            print "already searched"
            already_searched+=1;
            continue;
            
        i-=1;
        if i <= 0:
            break;
            
        print "get address " + json_obj["head_office_country"] + ", " + json_obj["head_office_post_code"] + ", " + json_obj["head_office_city"] + ", " + json_obj["head_office_address"]
        
        geoJson = get_geo_reference(json_obj["head_office_country"], json_obj["head_office_post_code"], json_obj["head_office_city"], json_obj["head_office_address"])
        
        if not geoJson:
            json_obj["no_geo_reference"] = True
            already_searched+=1;
            with open(os.path.join(json_folder, filename), 'w') as fp:
                json.dump(json_obj, fp)
            print "Adress not found"
            continue
        
        json_obj["lat"] = geoJson["lat"] 
        json_obj["lon"] = geoJson["lon"]
        json_obj["country_code"] = geoJson["address"]["country_code"]
        reference_exists+=1
        
        with open(os.path.join(json_folder, filename), 'w') as fp:
            json.dump(json_obj, fp)
        
        #print(geoJson);
        #break
        
    print reference_exists
    print already_searched
    
def get_geo_reference(country, postalcode, city, street):
    time.sleep(random.randint(1,2))
    url = u"https://nominatim.openstreetmap.org/search";
    query = "?addressdetails=1&limit=1&format=json&accept-language=de"
    
    if country:
        query += "&country="+urllib.quote_plus(country.encode('utf-8'));
        
    if postalcode:
        query += "&postalcode="+urllib.quote_plus(postalcode.encode('utf-8'));
        
    if city:
        query += "&city="+urllib.quote_plus(city.encode('utf-8'));
        
    if street:
        query += "&street="+urllib.quote_plus(street.encode('utf-8'));
    
    #print url + query;
    
    try:
        
        headers = {'referer': 'https://falk-m.de', 'Accept-Charset': 'UTF-8'}
        r = requests.post(url + query, headers=headers).json()
    
        if len(r) > 0:
            return r[0]
    except ValueError:
        return;

def add_geo_reference_google(json_folder = u"data/json"):
    i = 600;
    
    reference_exists = 0
    already_searched = 0
    
    for filename in os.listdir(json_folder):
        if not filename.endswith(".json"):
            continue;

        print filename;

        with open(os.path.join(json_folder, filename), 'r') as f:
            json_obj = json.load(f);

            
        
        #print json_obj["identification_number"]
        if json_obj.has_key("lat"):
            print "reference exists"
            reference_exists+=1;
            continue;
            
        if json_obj.has_key("no_geo_reference_google"):
            print "already searched"
            already_searched+=1;
            continue;
            
        i-=1;
        if i <= 0:
            break;
            
        print "get address " + json_obj["head_office_country"] + ", " + json_obj["head_office_post_code"] + ", " + json_obj["head_office_city"] + ", " + json_obj["head_office_address"]
        
        geoJson = get_geo_reference_google(json_obj["head_office_country"], json_obj["head_office_post_code"], json_obj["head_office_city"], json_obj["head_office_address"])
        
        if not geoJson:
            json_obj["no_geo_reference_google"] = True
            already_searched+=1;
            with open(os.path.join(json_folder, filename), 'w') as fp:
                json.dump(json_obj, fp)
            print "Adress not found"
            continue
        
        json_obj["lat"] = geoJson["geometry"]["location"]["lat"] 
        json_obj["lon"] = geoJson["geometry"]["location"]["lng"]
        
        for c in geoJson["address_components"]:
            if "country" in c["types"]:
                json_obj["country_code"] = c["short_name"]
        reference_exists+=1
        
        with open(os.path.join(json_folder, filename), 'w') as fp:
            json.dump(json_obj, fp)
        
        
        
    print reference_exists
    print already_searched    
    
def get_geo_reference_google(country, postalcode, city, street):
    #time.sleep(random.randint(1,2))
    url = u"https://maps.google.com/maps/api/geocode/json?key=AIzaSyAMSCJEwSTKbxZWbcAtHb4zdx4tlT3XG-8&address=";
    query = ""
    
    #"{$datas["plz"]} {$datas["ort"]}, {$datas["strasse"]} {$datas["hausnr"]}, {$land}";
    
    if postalcode:
        query += postalcode.encode('utf-8');
        
    if city:
        query += " "+city.encode('utf-8');
    
    if street:
        query += " "+street.encode('utf-8');
        
    if country:
        query += ", "+country.encode('utf-8');
        
     
    query = urllib.quote_plus(query)   
    #print url + query;
    
    try:
        
        headers = {'referer': 'https://falk-m.de', 'Accept-Charset': 'UTF-8'}
        r = requests.post(url + query, headers=headers).json()
    
        if len(r) > 0 and len(r["results"]) > 0:
            return r["results"][0]
    except ValueError:
        return;
    

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
        
