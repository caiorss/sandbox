#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#REFERENCES
#   http://nedbatchelder.com/blog/201206/eval_really_is_dangerous.html
#   http://bot24.blogspot.com.br/2013/03/escaping-python-sandbox-ndh-2013-quals.html
#   http://blog.delroth.net/2013/03/escaping-a-python-sandbox-ndh-2013-quals-writeup/
#
#   http://shell.appspot.com/
#
import os
import sys
import pprint

from sandbox import SandBox
modules = ["random", "math", "numpy"]
#builtins_allowed = ["range", "xrange"]
objects = {'listdir': os.listdir, 'platform': sys.platform, 'pprint':pprint.pprint, 'dict': dict,
           'chr':chr, 'ord':ord, 'dir':dir}
#s = SandBox(modules=modules, builtins_allowed=builtins_allowed, objects=objects)

s = SandBox(modules=modules, builtins_allowed=[], objects=objects)
#s.disable_underscore()
s.set_verbose()

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
        return False
    else:
        #printc("Error: {c}", str(err))
        printc("{g}{bold}Test Passed - OK!")
        return True


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
#http://www.vnsecurity.net/2012/10/writeup-hacklu-2012-13/

def makenumsmall(d):
	gadget = "(''=='')"
	rs = gadget

	if (d==0): return rs+"-"+rs
	if (d==1): return rs+"*"+rs

	for i in range(1,d): rs += "+(''=='')"
	return rs

def makenum(d):
	if (d<5): return makenumsmall(d)
	a = bin(d)[2:]
	index = len(a) - 1
	s = ""
	for c in a:
		if c == '1':
			s+= "("+makenumsmall(1)+"<<"+makenumsmall(index)+")+"
		index-=1
	return s[0:-1]

def makechar(line):
	return "('%'+`'"+chr(0xcc)+"'`["+str(makenum(3))+"])["+str(makenum(0))+":"+str(makenum(4))+"]%(" + makenum(line) + ")"

gd = {}

gd['x'] = "`'"+chr(0xcc)+"'`["+makenum(2)+"]"
gd['a'] = "`'"+chr(0xaa)+"'`["+makenum(3)+"]"
gd['b'] = "`'"+chr(0xbb)+"'`["+makenum(3)+"]"
gd['c'] = "`'"+chr(0xcc)+"'`["+makenum(3)+"]"
gd['d'] = "`'"+chr(0xdd)+"'`["+makenum(3)+"]"
gd['e'] = "`'"+chr(0xee)+"'`["+makenum(3)+"]"
gd['f'] = "`'"+chr(0xff)+"'`["+makenum(3)+"]"

a = "+execfile('key')+"
solo = [ord(i) for i in a]
#print solo
_sum = ''
import re
for line in solo:
	if chr(line) in gd:
		_gad = gd[chr(line)]
	elif chr(line) == "'":
		_gad = "'\\''"
	elif re.match("\W",chr(line)):
		_gad = "'"+chr(line)+"'"
	else:
		_gad = makechar(line)
	_sum += "+" + _gad

_sum = _sum[1:]
print _sum
print len(_sum)

print eval(eval(_sum))
print "1\n1\n"+_sum

"""

break8 = """
auth(''.__class__.__class__('haxx2',(),{'__getitem__':
lambda self,*a:'','__len__':(lambda l:l('function')( l('code')(
1,1,6,67,'d\x01\x00i\x00\x00i\x00\x00d\x02\x00d\x08\x00h\x02\x00'
'd\x03\x00\x84\x00\x00d\x04\x006d\x05\x00\x84\x00\x00d\x06\x006\x83'
'\x03\x00\x83\x00\x00\x04i\x01\x00\x02i\x02\x00\x83\x00\x00\x01z\n'
'\x00d\x07\x00\x82\x01\x00Wd\x00\x00QXd\x00\x00S',(None,'','haxx',
l('code')(1,1,1,83,'d\x00\x00S',(None,),('None',),('self',),'stdin',
'enter-lam',1,''),'__enter__',l('code')(1,2,3,87,'d\x00\x00\x84\x00'
'\x00d\x01\x00\x84\x00\x00\x83\x01\x00|\x01\x00d\x02\x00\x19i\x00'
'\x00i\x01\x00i\x01\x00i\x02\x00\x83\x01\x00S',(l('code')(1,1,14,83,
'|\x00\x00d\x00\x00\x83\x01\x00|\x00\x00d\x01\x00\x83\x01\x00d\x02'
'\x00d\x02\x00d\x02\x00d\x03\x00d\x04\x00d\n\x00d\x0b\x00d\x0c\x00d'
'\x06\x00d\x07\x00d\x02\x00d\x08\x00\x83\x0c\x00h\x00\x00\x83\x02'
'\x00S',('function','code',1,67,'|\x00\x00GHd\x00\x00S','s','stdin',
'f','',None,(None,),(),('s',)),('None',),('l',),'stdin','exit2-lam',
1,''),l('code')(1,3,4,83,'g\x00\x00\x04}\x01\x00d\x01\x00i\x00\x00i'
'\x01\x00d\x00\x00\x19i\x02\x00\x83\x00\x00D]!\x00}\x02\x00|\x02'
'\x00i\x03\x00|\x00\x00j\x02\x00o\x0b\x00\x01|\x01\x00|\x02\x00\x12'
'q\x1b\x00\x01q\x1b\x00~\x01\x00d\x00\x00\x19S',(0, ()),('__class__',
'__bases__','__subclasses__','__name__'),('n','_[1]','x'),'stdin',
'locator',1,''),2),('tb_frame','f_back','f_globals'),('self','a'),
'stdin','exit-lam',1,''),'__exit__',42,()),('__class__','__exit__',
'__enter__'),('self',),'stdin','f',1,''),{}))(lambda n:[x for x in
().__class__.__bases__[0].__subclasses__() if x.__name__ == n][0])})())

"""

break9 = """
__builtins__=([x for x in (1).__class__.__base__.__subclasses__() if x.__name__ == 'catch_warnings'][0]()._module.__builtins__)
import sys; print open(sys.argv[0]).read()
"""

# http://nedbatchelder.com/blog/201206/eval_really_is_dangerous.html
break10 = """
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

break11 = """
(lambda fc=(lambda n: [c for c in ().__class__.__bases__[0].__subclasses__() if c.__name__ == n][0]):
    fc("function")(fc("code")(0,0,0,0,"KABOOM",(),(),(),"","",0,""),{})()
)()
"""

codes = [break0, break1, break2, break3, break5, break6,
         break7, break8, break9, break10, break11]

results = []

for idx, code  in  enumerate(codes):
    printc('\n{by}Test%s' % idx)
    results.append(test_sandbox(code))

print "\n---------- summary ----------------\n\n"
total = len(results)
score = 0.0

for idx, r in enumerate(results):
    if r:
        print "Test %s OK" % idx
        score+=1
    else:
        print "Test %s Failed" % idx

print "\n\nSCORE %s%%" % (100*total/score)



