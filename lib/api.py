#!/usr/bin/env python

import searcher;

def call(path, request):  
    response = {}
    response["success"] = True
    response["request"] = request
    response["path"] = path
    
    if path == "/list":
        response["data"] = searcher.search(request["query"],request["page"], request["pagelen"]);
    elif path == "/facets":
        response["data"] = searcher.get_facets(request["query"]);
    else:
        response["message"] = "path not found"
        response["success"] = False
    
    return response

