#!/usr/bin/python3

# Code based in http://stackoverflow.com/questions/5194057/better-way-to-convert-file-sizes-in-python

import math

def filesize(size):
   if (size == 0):
       return '0B'
   size_name = ("b", "Kb", "Mb", "Gb", "Tb", "Pb", "Eb", "Zb", "Yb")
   i = int(math.floor(math.log(size,1024)))
   p = math.pow(1024,i)
   s = round(size/p,2)
   return '%s %s' % (s,size_name[i])
