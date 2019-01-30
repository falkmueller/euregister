#!/usr/bin/env python

import re
import sys
import os.path
import json

from whoosh.index import create_in, open_dir
from whoosh.fields import *
from whoosh import sorting

def get_schema():
    schema = Schema(id=ID(stored=True, unique=True))
    schema.add("*_s", TEXT(stored=True), glob=True)
    schema.add("*_b", BOOLEAN(stored=True), glob=True)
    schema.add("*_i", NUMERIC(int, stored=True), glob=True)
    schema.add("*_f", NUMERIC(float, stored=True), glob=True)
    schema.add("*_k", KEYWORD(stored=True), glob=True)
    
    return schema 

def create_index(index_folder):
    return create_in(index_folder, get_schema())

def get_index(index_folder):
    return open_dir(index_folder);
    
def search(query_str = u"*:*", page = 1, pagelen = 10,  index_folder = u"data/index"):
    #fields_of_interest_s:Customs
    from whoosh.qparser import QueryParser
    ix = get_index(index_folder)
    
    #query = QueryParser("head_office_country_s", ix.schema).parse(u"poland")
    query = QueryParser("*", ix.schema).parse(query_str)
    #query = QueryParser("id", ix.schema).parse(u"001814832718-07")
    results = ix.searcher().search_page(query, page, pagelen=pagelen)
    #results = list(ix.searcher().documents()) 
    
    response = {}
    response["count"] = len(results);
    response["entities"] = [];
    print "Results:"
    print response["count"]
    if len(results) > 0:
        for res in results:
            print res
            item = {};
            item["id"] =  res["id"];
            item["organisation_name"] =  res["organisation_name_s"];
            item["website_address"] = res["website_address_s"]
            item["country_code"] = res["country_code_k"]
            item["lat"] = res["lat_f"]
            item["lon"] = res["lon_f"]
            response["entities"].append(item)
    
    #facets
    facets = sorting.Facets()
    facets.add_field("country_code_k")
    results = ix.searcher().search(query, groupedby=facets)
    
    response["facets"] = {}
    response["facets"]["countries"] = {}
    countries = results.groups("country_code_k")
    
    
    with open( u"data/country_codes.json") as f:
            countryNames = json.load(f);

    for country_code in countries:
        response["facets"]["countries"][country_code] = {"count": len(countries[country_code]), "name": country_code} 
        if country_code.upper() in countryNames:
            response["facets"]["countries"][country_code]["name"] = countryNames[country_code.upper()]
        
    return response