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
        self.globalInputs = []
        self.validationError = False
        self.generator = Generator()
        
        self.errorString = StringVar()
        Label(self.frame, textvariable = self.errorString, fg = 'red').grid(row = 0)
        
        field = InputWrapper(self.frame, "Podaj globalne mu: ", self.validFloat, self.returnFloat)
        field.draw(1,0,1,1)
        self.globalInputs.append(field)
        
        field = InputWrapper(self.frame, "Podaj globalne sigma: ", self.validFloat, self.returnFloat)
        field.draw(1,2,1,3)
        self.globalInputs.append(field)
        
        field = InputWrapper(self.frame, "Podaj globalna liczebnosc grup: ", self.validPositiveInt, self.returnInt)
        field.draw(2,0,2,1)
        self.globalInputs.append(field)
        
        field = InputWrapper(self.frame, "Podaj liczbe grup: ", lambda i: i != "" and self.validPositiveInt(i), self.returnInt)
        field.draw(2,2,2,3)
        self.globalInputs.append(field)
        
        field = InputWrapper(self.frame, "Podaj ilosc cech: ", lambda i: i != "" and self.validPositiveInt(i), self.returnInt)
        field.draw(3,0,3,1)
        self.globalInputs.append(field)
        
        self.button = Button(self.frame, text = "Waliduj", command = self.setGlobal)
        self.button.grid(row = 3, column = 2, sticky = W)
    
    def setGlobal(self):
        self.validateGlobal()
        if self.validationError == True: return
        
        self.generator.gloabalMu = self.globalInputs[0].returnFormatted()
        self.generator.gloabalSigma = self.globalInputs[1].returnFormatted()
        self.generator.gloabalClassSize = self.globalInputs[2].returnFormatted()
        self.generator.numberOfClasses = self.globalInputs[3].returnFormatted()
        self.generator.featureVectorLength = self.globalInputs[4].returnFormatted()
        for i in self.globalInputs:
            i.dataField.configure(state="disable")
        self.showClassInput()
    
    def validateGlobal(self):
        self.validationError = False
        self.errorString.set("")
        for i in self.globalInputs:
            if i.validate() == False:
                self.errorString.set("Wystapil problem walidacji pola: '"+i.labelText+"'. Wartosc '"+i.dataField.get()+"' posiada zly format.")
                self.validationError = True
                break
        
    def validPositiveInt(self, value):
        if value == "": return True
        return value.isdigit() and (int(value)>0)
    
    def validFloat(self, value):
        if value == "": return True
        try:
            float(value)
            return True
        except ValueError:
            return False
        
    def returnInt(self, value):
        if value == "": return None
        return int(value)
    
    def returnFloat(self, value):
        if value == "": return None
        return float(value)
    
    def returnString(self, value):
        return value
    
    def showClassInput(self):
        self.currentFeatureNumber = 1
        self.classCount = StringVar()
        self.classCount.set("Utworzono: 0")
        Label(self.frame, textvariable = self.classCount).grid(row = 4, sticky = W)
        self.classSize = InputWrapper(self.frame, "Liczebnosc grupy:", 
                                      self.validPositiveInt, self.returnInt)
        self.classSizedraw(5,0,5,1)
        self.addClassButton = Button(self.frame, text = "Dodaj grupe", command = self.performAddClass, state = 'disabled')
        self.addClassButton.grid(row = 5, column = 2, sticky = W)
        
        self.featureCount = StringVar()
        self.featureCount.set("Utworzono cech: 0")
        Label(self.frame, textvariable = self.featureCount).grid(row = 6, sticky = W)
        self.classMu = InputWrapper(self.frame, "Mu:", self.validPositiveInt, self.returnInt)
        self.classMu.draw(7,0,7,1)
        self.classSigma = InputWrapper(self.frame, "Sigma:", self.validPositiveInt, self.returnInt)
        self.classSigma.draw(7,2,7,3)
        self.addFeatureButton = Button(self.frame, text = "Dodaj ceche", command = self.performAddFeature)
        self.addFeatureButton.grid(row = 7, column = 4, sticky = W)
        
        self.classSigmaList = []
        self.classMuList = []
    
    def performAddFeature(self):
        self.errorString.set("")
        if self.classSigma.validate() and self.classMu.validate():
            self.classSigmaList.append(self.classSigma.returnFormatted())
            self.classMuList.append(self.classMu.returnFormatted())
            self.featureCount.set("Utworzono cech: "+str(self.currentFeatureNumber))
            self.classMu.clearInput()
            self.classSigma.clearInput()
            self.currentFeatureNumber += 1
            if self.currentFeatureNumber > self.generator.featureVectorSize: self.addFeatureButton.configure(state = 'disabled')
        else:
            self.errorString.set("Lokalne pole Mu lub Sigma dostalo nie numeryczna wartosc")
        
    def performAddClass(self):
        print "P"