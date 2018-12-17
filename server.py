#!/usr/bin/env python

import sys
import os
import posixpath
import urllib
import SimpleHTTPServer #https://github.com/enthought/Python-2.7.3/blob/master/Lib/SimpleHTTPServer.py
import SocketServer
import json
from StringIO import StringIO
from lib import api

class RequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    
    error_message_format = """<html>\
            <head>
            <title>Error response ccc</title>
            </head>
            <body>
            <h1>Error response</h1>
            <p>Error code %(code)d.
            <p>Message: %(message)s.
            <p>Error code explanation: %(code)s = %(explain)s.
            </body>
            </html>"""
    
    # override path function to get all files from public folder
    def translate_path(self, path):
        path = path.split('?',1)[0]
        path = path.split('#',1)[0]
        path = posixpath.normpath(urllib.unquote(path))
        words = path.split('/')
        words.insert(0, "public")
        words = filter(None, words)
        path = os.getcwd()
        for word in words:
            drive, word = os.path.splitdrive(word)
            head, word = os.path.split(word)
            if word in (os.curdir, os.pardir): continue
            path = os.path.join(path, word)
        return path
    
    # override post function vor own api functions
    def do_POST(self):
        result = {}
        
        try:
            content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
            post_data = self.rfile.read(content_length) # <--- Gets the data itself
            request = json.loads(post_data)
            result = api.call(self.path, request)
            
            if result["success"]:
                self.send_response(200)
            else:
                self.send_response(400)
                
        except Exception as e:
            result = {}
            result["success"] = 0
            result["message"] = "Exception: " + str(e) 
            self.send_response(500)
            
        print(result)   
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        
        io = StringIO()
        json.dump(result, io)
        self.wfile.write(io.getvalue())


# ------------------------------------------------------------------------------
# Service routine
# ------------------------------------------------------------------------------

port = 8001
if len(sys.argv) > 1:
    try:
        p = int(sys.argv[1])
        port = p
    except ValueError:
        print "port value provided must be an integer"

Handler = RequestHandler
Handler.extensions_map.update({
    '.webapp': 'application/x-web-app-manifest+json',
});

# interrupt the program with Ctrl-C
print "serving on port {0}".format(port)
server = SocketServer.TCPServer(('0.0.0.0', port), Handler)
server.serve_forever()

