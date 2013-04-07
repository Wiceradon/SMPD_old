'''
Created on 09-03-2013

@author: jakub
'''
from commons.Point import Point
import numpy as np

class Generator(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.globalMu, self.globalSigma, self.globalClassSize, self.numberOfClasses, self.featureVectorSize = None, None, None, None, None
        self.classCenters = set()
        self.points = set()
        self.localMu, self.localSigma, self.localClassSize = [], [], []
        self.ERRORS = {-1: "Brak zmiennej Mu", -2: "Brak zmiennej Sigma", -3: "Brak lub zbyt mala liczba klas"}
        self.lastError = ""
        self.lastErrorId = None
    
    def _conditionalAdd(self, var1, var2):
        '''
        Method return first variable if not None, second otherwise
        '''
        return var1 if var1 != None else var2 # Conditional expression ( doTrue if condition else doFalse )

    def _createTuple(self, var1, var2):
        '''
        Return tuple full of var2 if var1 list is None or tuple containing values returned from _conditionalAdd
        '''
        if var1 == None: return tuple([var2 for i in range(self.featureVectorSize)])
        else: return tuple([self._conditionalAdd(x, var2) for x in var1])

    def addMu(self, value):
        '''
        Add value or globalMu to list
        '''
        self.localMu.append(self._createTuple(value, self.globalMu))
    
    def addSigma(self, value):
        '''
        Add value or globalSigma to list
        '''
        self.localSigma.append(self._createTuple(value, self.globalSigma))
    
    def addClassSize(self, value):
        '''
        Add value or globalClassSize to list
        '''
        self.localClassSize.append(self._conditionalAdd(value, self.globalClassSize))
        
    def addClassCenter(self, coord, label):
        '''
        Add coordinates representing center of a class. Point is added iff coord and label != None
        '''
        if coord != None and label != None: self.classCenters.add(Point(label, list(coord)))
    
    def _setError(self, errorId, additionalString):
        '''
        Method for setting last occurrence of an error. Don't use it explicitly.
        '''
        self.lastErrorId = errorId
        self.lastError = self.ERRORS[errorId]+additionalString
        return errorId
    
    def _validateFields(self):
        # First we validate if there is specified #of classes
        if self.numberOfClasses == None or self.numberOfClasses < 1: return self._setError(-3, '')
        # Yes there is so we check number of feature representing our data. Can't be None or < 1
        if self.featureVectorSize == None or self.featureVectorSize < 1: return self._setError(-4, '')
        # Now check if there is enough centers
        if len(self.classCenters) != self.numberOfClasses: return self._setError(-5, '')
        # Now check if every point has long enough vector to proper represent class in dataset
        for i in self.classCenters:
            if len(i.FEATURES) != self.featureVectorSize: return self._setError(-6, ' Dla klasy '+str(i.label))
        # Check if localMu, localSigma and localClassSize is proper length
        if len(self.localMu) != self.numberOfClasses: return self._setError(-7, '')
        if len(self.localSigma) != self.numberOfClasses: return self._setError(-8, '')
        if len(self.localClassSize) != self.numberOfClasses: return self._setError(-9, '')
        # Check if every value in localMu, localSigma and localClassSize is properly defined (not None and in case of localClassSize >0)
        for i in self.localMu:
            if (i == None) or (None in i) or (len(i)!=self.featureVectorSize): return self._setError(-1, '')
        for i in self.localSigma:
            if (i == None) or (None in i) or (0 in i) or (len(i)!=self.featureVectorSize): return self._setError(-2, '')
        for i in self.localClassSize:
            if (i == None) or (i < 1): return self._setError(-10, '')
        # Everything is fine
        return 0
    
    def generatePoints(self):
        # Generate points representing classes for validation
        for idn, c in zip(range(self.numberOfClasses), self.localSigma):
            self.addClassCenter(c, idn)
        # Validate fields before generating
        if self._validateFields() != 0: return self.lastErrorId
        # Generate points
        for i in range(self.numberOfClasses):
            oldSize = len(self.points)
            while (len(self.points) - oldSize) < self.localClassSize[i]:
                coordToGenerate = oldSize+self.localClassSize[i] - len(self.points)
                tmp = [[float("%.2f"%x) for x in np.random.normal(mu,sigma**2,size)] for (sigma, mu, size) in 
                       zip(self.localSigma[i], self.localMu[i], [coordToGenerate]*self.featureVectorSize)]
                for coord in zip(*tmp):
                    self.points.add(Point(i+1,coord))
        return 0
    
    def getGenCoord(self, label, dimmension):
        if len(self.points) == 0: return []
        return [ x.FEATURES[dimmension] for x in self.points if x.LABEL == label+1 ]
            