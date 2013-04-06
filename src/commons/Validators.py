'''
Created on 02-04-2013

@author: jakub
'''

def isIntOrEmpty(value):
    if value == "": return True
    return value.isdigit()

def isPositiveIntOrEmpty(value):
    if isIntOrEmpty(value): return (int(value) > 0)
    else: return False
    
def isFloatOrEmpty(value):
    if value == "": return True
    try:
        float(value)
        return True
    except ValueError:
        return False

isPositiveInt = lambda i: i != "" and isPositiveIntOrEmpty(i)
