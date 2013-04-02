'''
Created on 16-03-2013

@author: jakub
'''
from Tkinter import *

class InputWrapper:
    '''
    classdocs
    '''


    def __init__(self, parent, labelText, validateCondition, formatt):
        '''
        Constructor
        '''
        self.labelText = labelText
        self.labelField = Label(parent, text = labelText)
        self.dataField = Entry(parent)
        self.validateCondition = validateCondition
        self.formatt = formatt
    
    def validate(self):
        return self.validateCondition(self.dataField.get())
        
    def returnFormatted(self):
        return self.formatt(self.dataField.get())
    
    def clearInput(self):
        self.dataField.delete(0, END)
        
    def draw(self, labelRow, labelCol, entryRow, entryCol):
        self.labelField.grid(row = labelRow, column = labelCol, sticky = W)
        self.dataField.grid(row = entryRow, column = entryCol, sticky = W)