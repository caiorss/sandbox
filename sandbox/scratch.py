#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

"""



colors = {"WHITE"   : "\033[1;37m",
          "GREEN"   : "\033[0;32m",
          "CYAN"    : "\033[0;36m",
          "GRAY"    : "\033[0;37m",
          "BLUE"    : "\033[0;34m",
          "RED"     : "\033[0;31m",
          "YELLOW"  : "\033[0;33m",
          "MAGNETA" : "\033[0;35m",
}



# print colors["WHITE"], "White"
# print colors["GREEN"], "Green"
# print colors["CYAN"],  "Cyan"
# print colors["GRAY"],  "Gray"
# print colors["BLUE"],  "Blue"
# print colors["RED"],   "Red"
# print colors["YELLOW"],"Yellow"
# print colors["MAGNETA"],  "Magneta"



def printc(*args):
    import re
    txt = "".join(args)
    txt = re.sub(r'{w}', r"\033[0;37m", txt)  # WHITE
    txt = re.sub(r'{ge}', r"\033[0;32m", txt) # GREEN
    txt = re.sub(r'{c}', r"\033[0;36m", txt)  # CYAN
    txt = re.sub(r'{g}', r"\033[0;37m", txt)  # GRAY
    txt = re.sub(r'{r}', r"\033[0;31m", txt)  # RED
    txt = re.sub(r'{y}', r"\033[0;33m", txt)  # YELLOW
    txt = re.sub(r'{m}', r"\033[0;35m", txt)  # MAGNETA
    print(txt)


printc(" {w}Colors {r}red {c}cyan {ge}green {r}red {y}yellow {m}magneta {g}gray ")