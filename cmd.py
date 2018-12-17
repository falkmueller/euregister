#!/usr/bin/env python

import importlib
import sys;

if len(sys.argv) > 1:
    function_string = sys.argv[1]
    mod_name, func_name = function_string.rsplit('.',1)
    mod = importlib.import_module(mod_name)
    func = getattr(mod, func_name)
    func()
#    module = __import__("parser")
#    func = getattr(module, sys.argv[2])
#    func()

    #getattr(globals()[sys.argv[1]], sys.argv[2])()
else:
        print "first argument must function name";
        