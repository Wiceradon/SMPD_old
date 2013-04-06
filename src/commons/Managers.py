'''
Created on 07-04-2013

@author: jakub
'''
import time
from commons import Parsers

def pointsFileWrite(data, labelDelimeter = " ", featureDelimeter = ";", pointDelimiter = "\n"):
    name = "generatedPoints"+str(time.time())+".data"
    with open(name, 'w') as file:
        file.write(pointDelimiter.join([ Parsers.parsePointToString(p, labelDelimeter, featureDelimeter) for p in data ]))