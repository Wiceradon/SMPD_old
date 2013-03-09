'''
Created on 09-03-2013

@author: jakub
'''

class Point:
    '''
    classdocs
    '''


    def __init__(self, label, features):
        '''
        Constructor
        '''
        self.LABEL = label
        self.FEATURES = tuple([i for i in features])
    
    def __eq__(self, other):
        return self.FEATURES == other.FEATURES
    
    def __str__(self):
        return "Class: " + str(self.LABEL) + ", coordinates: " + ";".join([str(i) for i in self.FEATURES])
    
    def __ne__(self, other):
        return not self.__eq__(other)
    
    def __hash__(self):
        return hash(self.FEATURES)