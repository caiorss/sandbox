#!/usr/bin/env python
# -*- coding: utf-8 -*-


break1 =  """
#print file
#__import__("os")
print os.listdir("/")
"""

break2 = """

obj_class  = [].__class__.__bases__[0]
subclasses = dict((e.__name__, e) for e in obj_class.__subclasses__())

#s = subclasses['socket']

#for k, v in subclasses.iteritems():
#    print k,'\t',v

f = subclasses['file']
f('textcrack.txt', 'w').write('I cracked your sandbox')

"""

break3 = """
def evil_function():
    print "the evil"

def foo():
    print "I am secure"

foo.__setattr__("func_code", evil_function.func_code)

foo()

"""

try:
    print "\n\nTrying to break sandbox"
    print "code\n"
    print break1
    s.execute(break1)
    print "\n-----------------------"
    print "SANDBOX BROKEN!!"
except Exception as err:
    print "*************************"
    print err
    print "\n-----------------------"
    print "Passed the test"


try:
    print "\n\nTrying to break sandbox"
    print "code\n"
    print break2
    s.execute(break2)
    print "\n-----------------------"
    print "SANDBOX BROKEN!!"
except Exception as err:
    print "*************************"
    print err
    print "\n-----------------------"
    print "Passed the test"


try:
    print "\n\nTrying to break sandbox"
    print "code\n"
    print break3
    s.execute(break3)
    print "\n-----------------------"
    print "SANDBOX BROKEN!!"
except Exception as err:
    print "*************************"
    print err
    print "\n-----------------------"
    print "Passed the test"

