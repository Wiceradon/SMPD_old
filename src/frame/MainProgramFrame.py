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
        self.frame = master
        #self.frame.pack()
        self.hasChild = False
        self.button = Button(self.frame, text = "Quit", command = self.frame.quit)
        self.button.pack(side = BOTTOM)
    
    def addButton(self, name, frameClass):
        self.button = Button(self.frame, text = name, command = lambda i=frameClass: self.handleClick(i))
        self.button.pack()
        
    def handleClick(self, frameClass):
        if self.hasChild == True: return
        self.hasChild = True
        child = Toplevel()
        child.protocol("WM_DELETE_WINDOW", lambda i=child: self.childKilled(i))
        obj = frameClass(child)
        
        
    def childKilled(self, frame):
        self.hasChild = False
        frame.destroy()