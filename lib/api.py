#!/usr/bin/env python

import searcher;
import os.path
import json

def call(path, request):  
    response = {}
    response["success"] = True
    response["request"] = request
    response["path"] = path
    
    if path == "/list":
        response["data"] = searcher.search(request["query"],request["page"], request["pagelen"]);
    elif path == "/facets":
        response["data"] = searcher.get_facets(request["query"]);
    elif path == "/detail":
        id = request["id"]
        json_folder = u"data/json"
        with open(os.path.join(json_folder, id + ".json")) as f:
            json_obj = json.load(f);
        response["data"] = json_obj;
    else:
        response["message"] = "path not found"
        response["success"] = False
    
    return response

