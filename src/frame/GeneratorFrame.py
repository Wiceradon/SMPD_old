'''
Created on 16-03-2013

@author: jakub
'''
from Tkinter import *
from points_generator.Generator import Generator
from widgets.InputWrapper import InputWrapper

class GeneratorFrame:
    '''
    classdocs
    '''


    def __init__(self, frame):
        '''
        Constructor
        '''
        
        self.frame = frame
        self.field = InputWrapper(self.frame, "Podaj int: ", self.validFloat)
        self.field.frame.pack(side = TOP)
        self.button = Button(self.frame, text = "Waliduj", command = self.field.validator)
        self.button.pack(side = BOTTOM)
    
    def a(self):
        self.field.validate  
        
    def validInt(self, value):
        print value.isdigit()
    
    def validFloat(self, value):
        print float(value)