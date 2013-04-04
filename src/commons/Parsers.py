'''
Created on 04-04-2013

@author: jakub
'''

def parseIntOrNone(value):
    if value in ("", None): return None
    return int(value)

def parseFloatOrNone(value):
    if value in ("", None): return None
    return float(value)

def parseSimpleString(value):
    if value == None: return ""
    return value