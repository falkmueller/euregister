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
    schema.add("*_d", DATETIME(stored=True), glob=True)
    
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
            item["www"] = res["website_address_s"]
            item["country_code"] = res["country_code_k"]
            item["lat"] = res["lat_f"]
            item["lon"] = res["lon_f"]
            item["number_of_persons"] = res["number_of_persons_involved_i"]
            #item["registration_date"] = res["registration_date_d"].strftime('%Y-%m-%d')
            response["entities"].append(item)
            
    return response

def get_facets(query_str = u"*:*",  index_folder = u"data/index"):
    #fields_of_interest_s:Customs
    from whoosh.qparser import QueryParser
    ix = get_index(index_folder)
    
    query = QueryParser("*", ix.schema).parse(query_str)
    response = {}
    #facets
    facets = sorting.Facets() 
    facets.add_field("country_code_k")
    facets.add_field("section_k")
    facets.add_field("subsection_k")
    facets.add_field("registration_month_k")
    facets.add_facet("nop",  sorting.RangeFacet("number_of_persons_involved_i", 0, 1000, 5))
    results = ix.searcher().search(query, groupedby=facets)
    
    response["countries"] = {}
    facet_results = results.groups("country_code_k")
    for code in facet_results:
        response["countries"][code] = len(facet_results[code])

    response["sections"] = {}
    facet_results = results.groups("section_k")
    for code in facet_results:
        response["sections"][code] = len(facet_results[code])
        
    response["subsections"] = {}
    facet_results = results.groups("subsection_k")
    for code in facet_results:
        response["subsections"][code] = len(facet_results[code])
        
    response["number_of_persons"] = {}
    facet_results = results.groups("nop");
    for code in facet_results:
        response["number_of_persons"][str(code[0]) + "-" + str(code[1])] = len(facet_results[code])
  
    response["registration_month"] = {}
    facet_results = results.groups("registration_month_k")
    for code in facet_results:
        response["registration_month"][code] = len(facet_results[code])
        
    return response


