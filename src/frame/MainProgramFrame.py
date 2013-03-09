'''
Created on 09-03-2013

@author: jakub
'''
from Tkinter import *


class MainProgramFrame:
    '''
    classdocs
    '''


    def __init__(self, master):
        '''
        Constructor
        '''
        frame = Frame(master)
        frame.pack()
        
        self.button = Button(frame, text="Quit", command=frame.quit)
        self.button.pack(side=LEFT)