'''
Created on 09-03-2013

@author: jakub
'''
from frame.MainProgramFrame import *
from frame.GeneratorFrame import *
from Tkinter import *
from points_generator.Generator import Generator
from commons.Point import Point 

def a(self,f):
    print f

if __name__ == '__main__':
    root = Tk()
    root.wm_title("SMPD")
    app = MainProgramFrame(root)
    app.addButton("A", GeneratorFrame)
    
    root.mainloop()
    
    
    