#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#
#   http://nedbatchelder.com/blog/201206/eval_really_is_dangerous.html
#
#
#

import os
import sys
import pprint

from sandbox import SandBox
modules=["random", "math", "numpy"]
#builtins_allowed = ["range", "xrange"]
objects = {'listdir': os.listdir, 'platform': sys.platform, 'pprint':pprint.pprint, 'dict': dict,
           'chr':chr, 'ord':ord, 'dir':dir}
#s = SandBox(modules=modules, builtins_allowed=builtins_allowed, objects=objects)

s = SandBox(modules=modules, builtins_allowed=[], objects=objects)
s.disable_underscore()

def printc(*args):
    """
    Print text in colored format

    Color tags:
    {r} - red
    {y} - yellow
    {g} - green
    {0} - black
    {m} - magneta
    {w} - white
    {b} - Blue

    {b0} - background black
    {br} - background white
    {by} - background yello

    {bold} - Bold text
    {line} - Underline

    """
    import re
    txt = "".join(args) + "{w}"

    txt = re.sub(r'{\0}', r"\033[0;30m", txt)  # BLACK
    txt = re.sub(r'{b}', r"\033[0;34m", txt)  # BLUE
    txt = re.sub(r'{w}', r"\033[0;37m", txt)  # WHITE
    txt = re.sub(r'{g}', r"\033[0;32m", txt) # GREEN
    txt = re.sub(r'{c}', r"\033[0;36m", txt)  # CYAN
    txt = re.sub(r'{r}', r"\033[0;31m", txt)  # RED
    txt = re.sub(r'{y}', r"\033[0;33m", txt)  # YELLOW
    txt = re.sub(r'{m}', r"\033[0;35m", txt)  # MAGNETA

    # BACKGROUNDS
    txt = re.sub(r'{b0}', r"\033[0;40m", txt)  # BLACK
    txt = re.sub(r'{bb}', r"\033[0;44m", txt)  # BLUE
    txt = re.sub(r'{bw}', r"\033[0;41m", txt)  # WHITE
    txt = re.sub(r'{bg}', r"\033[0;42m", txt)  # GREEN
    txt = re.sub(r'{bc}', r"\033[0;46m", txt)  # CYAN
    txt = re.sub(r'{br}', r"\033[0;41m", txt)  # RED
    txt = re.sub(r'{by}', r"\033[0;43m", txt)  # YELLOW
    txt = re.sub(r'{bm}', r"\033[0;45m", txt)  # MAGNETA

    txt = re.sub(r'{bold}', r"\033[1m", txt)    # Bold
    txt = re.sub(r'{line}', r"\033[4m", txt)    # Bold

    print txt

def test_sandbox(exploit_code):

    print "\n\nTrying to execute"
    printc('{y}', exploit_code)
    test = s.execute(exploit_code)

    if test:
        printc("{r}Test not Passed - NOT!")
    else:
        #printc("Error: {c}", str(err))
        printc("{g}{bold}Test Passed - OK!")


break0 = """
eval("()._" + "_class_" + "_._" + "_bases_" + "_[0]")
"""

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
f('textcrack.txt', 'w').write('I cracked your __sandbox__')

"""

break3 = """
def evil_function():
    print "the evil"

def foo():
    print "I am secure"

foo.__setattr__("func_code", evil_function.func_code)

foo()

"""

break4 = """
# coding: rot_13
# "import evil_module" encoded in ROT13
vzcbeg rivy_zbqhyr
"""

break5 = """
().__class__.__bases__[0].__subclasses__()[40]("./key").read()
"""

break6 = """
[
    c for c in ().__class__.__base__.__subclasses__()
    if c.__name__ == 'catch_warnings'
][0]()._module.__builtins__

print dir(__builtins__)
#__import__("os")
"""

# https://blog.inexplicity.de/plaidctf-2013-pyjail-writeup-part-i-breaking-the-sandbox.html
break7 = """
def get_func_globals(c):
    subs = _list(get_subs(c))
    gs = _list()
    for sub in subs:
        if _hasattr(sub, '__dict__'):
            for k,v in sub.__dict__.items():
                if _hasattr(v, 'func_globals'):
                    if not _hasattr(v.func_globals, "keys"):
                        continue
                    for fk in v.func_globals.keys():
                        if v.func_globals[fk]:
                            print "%s is not None in %s -> %s" % (fk, k, sub.__name__)
                            if v.func_globals[fk] not in gs:
                                gs.append(v.func_globals[fk])
        if _hasattr(sub, 'func_globals'):
            if not _hasattr(sub.func_globals, "keys"):
                continue
            for fk in sub.func_globals.keys():
                if sub.func_globals[fk]:
                    print "%s is not None in %s" % (fk, sub.__name__)
                    if sub.func_globals[fk] not in gs:
                        gs.append(sub.func_globals[fk])
    print "Globals: %s" % gs
    return gs

def check_globs(globs):
    ret = _list()
    for glob in globs:
        if not _hasattr(glob, '__dict__'):
            continue
        for k,v in glob.__dict__.items():
            if k in ['__doc__']:
                continue
            if "os" in _str(v):
                print "%s: %s -> %s" %(glob, k,v)
            ret.append(v)
    return ret

"""

# http://nedbatchelder.com/blog/201206/eval_really_is_dangerous.html
break_segmentatation_fault = """
(lambda fc=(
    lambda n: [
        c for c in
            ().__class__.__bases__[0].__subclasses__()
            if c.__name__ == n
        ][0]
    ):
    fc("function")(
        fc("code")(
            0,0,0,0,"KABOOM",(),(),(),"","",0,""
        ),{}
    )()
)()
"""

break_segmentation_fault2 = """
(lambda fc=(lambda n: [c for c in ().__class__.__bases__[0].__subclasses__() if c.__name__ == n][0]):
    fc("function")(fc("code")(0,0,0,0,"KABOOM",(),(),(),"","",0,""),{})()
)()
"""

printc('\n{by}Test0')
test_sandbox(break0)

printc('\n{by}Test1')
test_sandbox(break1)

printc('\n{by}Test2')
test_sandbox(break2)

printc('\n{by}Test3')
test_sandbox(break3)

printc('\n{by}Test4')
test_sandbox(break4)

printc('\n{by}Test5')
test_sandbox(break5)

printc('\n{by}Test6')
test_sandbox(break6)



printc('\n{by}Test break_segmentatation_fault')
test_sandbox(break_segmentatation_fault)


printc('\n{by}Test break_segmentatation_fault2')
test_sandbox(break_segmentation_fault2)
