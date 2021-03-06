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
import hashlib

from datetime import datetime
from whoosh.fields import *

def import_csv(csv_file = u"data/source/full_export_new.csv", json_folder = u"data/json"):   
    
    if not os.path.isfile(csv_file):
        print "file " + csv_file + " not found";
        return;

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
            #if not json_obj.has_key("country_code"):
            #    print filename + " " + json_obj["head_office_country"]
            print "reference exists"
            reference_exists+=1;
            continue;
            
        if json_obj.has_key("no_geo_reference_google"):
            print filename + " get address " + json_obj["head_office_country"] + ", " + json_obj["head_office_post_code"] + ", " + json_obj["head_office_city"] + ", " + json_obj["head_office_address"]
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

    if not os.path.exists(index_folder) or os.path.isfile(index_folder):
        print "folder " + index_folder + " not found";
        return;

    if not os.path.exists(json_folder) or os.path.isfile(json_folder):
        print "folder " + json_folder + " not found";
        return;

    ix = searcher.create_index(index_folder)
    writer = ix.writer()
    
    with open( u"data/country_codes.json") as f:
            countryNames = json.load(f);

    dicts = {'sections': {},'countries': {}, 'count': 0}
    
    for filename in os.listdir(json_folder):
        if not filename.endswith(".json"):
            continue;

        with open(os.path.join(json_folder, filename)) as f:
            json_obj = json.load(f);

        print json_obj["identification_number"]
        
        section_hash = hashlib.md5(json_obj["section"]).hexdigest().decode("utf-8")[:6]
        if not section_hash in dicts["sections"]:
            dicts["sections"][section_hash] = {'name': json_obj["section"], 'subsections': {}}
        
        subsection_hash = section_hash[0:3] + hashlib.md5(json_obj["subsection"]).hexdigest().decode("utf-8")[:6]
        
        if not subsection_hash in dicts["sections"][section_hash]['subsections']:
            dicts["sections"][section_hash]['subsections'][subsection_hash] = {'name': json_obj["subsection"]}
        
        if json_obj["country_code"].upper() in countryNames:
            dicts["countries"][json_obj["country_code"].lower()] = countryNames[json_obj["country_code"].upper()]
        else:
            dicts["countries"][json_obj["country_code"].lower()] = json_obj["country_code"]
        
        writer.add_document(
            id=json_obj["identification_number"],
            organisation_name_s=json_obj["organisation_name"],
            fields_of_interest_s=json_obj["fields_of_interest"],
            head_office_country_s=json_obj["head_office_country"],
            registration_date_s=json_obj["registration_date"],
            website_address_s=json_obj["website_address"],
            country_code_k=json_obj["country_code"].lower(),
            section_k = section_hash,
            subsection_k = subsection_hash,
            lat_f=json_obj["lat"],
            lon_f=json_obj["lon"],
            number_of_persons_involved_i=json_obj["number_of_persons_involved"],
            member_organisations_s = json_obj["member_organisations"],
            goals__remit_s = json_obj["goals__remit"],
            registration_date_d = datetime.datetime.strptime(json_obj["registration_date"], '%d/%m/%Y'),
            registration_month_k = datetime.datetime.strptime(json_obj["registration_date"], '%d/%m/%Y').strftime('%Y-%m').decode("utf-8")
        )
        
        dicts["count"] += 1;

    writer.commit(optimize=True)
    
    with open('public/js/dicts.js', 'w') as fp:
        fp.write("var dicts = " + json.dumps(dicts))
        
