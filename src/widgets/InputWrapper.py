'''
Created on 16-03-2013

@author: jakub
'''
from Tkinter import *

class InputWrapper:
    '''
    classdocs
    '''


    def __init__(self, parent, labelText, validateCondition, format):
        '''
        Constructor
        '''
        self.frame = Frame(parent)
        self.labelText = labelText
        self.labelField = Label(self.frame, text = labelText)
        self.labelField.pack(side = LEFT)
        self.dataField = Entry(self.frame)
        self.dataField.pack(side = LEFT)
        self.validate = lambda : self.executeValidator(validateCondition)
        self.returnFormatted = lambda : self.formatValue(format)
    
    def executeValidator(self, cond):
        return cond(self.dataField.get())
        
    def formatValue(self, format):
        return format(self.dataField.get())
    
    def clearInput(self):
        self.dataField.delete(0, END)