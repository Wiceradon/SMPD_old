'''
Created on 16-03-2013

@author: jakub
'''
from Tkinter import *

class InputWrapper:
    '''
    classdocs
    '''


    def __init__(self, parent, labelText, validateCondition):
        '''
        Constructor
        '''
        self.frame = Frame(parent)
        self.labelField = Label(self.frame, text = labelText)
        self.labelField.pack(side = LEFT)
        self.dataField = Entry(self.frame)
        self.dataField.pack(side = LEFT)
        self.validator = lambda : self.executeValidator(validateCondition)
    
    def executeValidator(self, cond):
        cond(self.dataField.get())