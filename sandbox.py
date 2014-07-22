#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Python environment to run user source given code safely

"""

class SandBox:

    def __init__(self, modules=[], builtins_allowed=[], objects={}):
        _namespace_ = {}

        for module in modules:
            _namespace_[module] = __import__(module)

        #builtins_allowed = ["range", "xrange"]
        for a in builtins_allowed:
            _namespace_[a] = getattr(__builtins__, a)

        for k, v in objects.iteritems():
            _namespace_[k] = v

        self.sandbox =dict(_namespace_, __builtins__=None)



        #self.sandbox['()'] = None
        #self.sandbox['__subclasses__'] = None
        self.cache = {}

        #print self.sandbox

    def eval(self, code):
        #import StringIO
        #fp = StringIO.StringIO()
        bytecode = compile(code,'<stdin>', 'exec')
        try:
            output = eval(bytecode, self.sandbox, self.cache)
            #output=  eval(bytecode)
            print output
            #return output

        except Exception as err:
            print err
            #return err

    def execute(self, code):
        # import re
        # variables = re.findall('\s*(.*)\s*=\s*', code)
        # print "variables = %s" % variables

        #bytecode = compile(code,'<string>', 'exec')
        bytecode = compile(code,'<string>', 'exec')

        exec(bytecode, self.sandbox)

import os
import sys
import pprint

modules=["random", "math", "numpy"]
builtins_allowed = ["range", "xrange", "dict"]
objects = {'listdir': os.listdir, 'platform': sys.platform, 'pprint':pprint.pprint}
s = SandBox(modules=modules, builtins_allowed=builtins_allowed, objects=objects)


#
# print [random.random() for r in range(10)]


