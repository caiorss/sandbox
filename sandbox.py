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

        self.__sandbox__  =  dict(_namespace_, __builtins__=None)
        self.__sandbox0__ = self.__sandbox__.copy()
        #print self.__sandbox__

    def eval(self, code):
        #import StringIO
        #fp = StringIO.StringIO()
        bytecode = compile(code,'<stdin>', 'exec')
        try:
            output = eval(bytecode, self.__sandbox__)
            #output=  eval(bytecode)
            print output
            #return output

        except Exception as err:
            print err
            #return err

    def execute(self, code):
        bytecode = compile(code,'<string>', 'exec')
        try:
            exec(bytecode, self.__sandbox__)
            return True
        except Exception as err:
            print err
            return False

    def executefile(self, filename):
        source = open(filename, 'r').read()
        return self.execute(source)

    def reset(self):
        self.__sandbox__ = self.__sandbox0__.copy()


